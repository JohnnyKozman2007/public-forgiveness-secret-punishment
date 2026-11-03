#!/usr/bin/env python3
"""
Shared cluster-aware inference utilities for Blocks 1, 2, 3, 4 and 6.

Design facts this module encodes (verified from output/runs/*.json):
- 60 runs = 3 labels (labelled / mislabelled / unlabelled) x 2 probe settings (ON / OFF) x 10 runs.
- Every run contains exactly 10 AI workers: one per model and one per seat (cruelty level 1-10).
- Workers inside the same run share Slack channels, so their outcomes are NOT independent.
  The run (`bname`) is therefore the cluster unit for all pooled inference.

Inference engines:
1. `PermEngine` (Block 1, design-based permutation tests):
   - Within-run factors (model, seat, safe-vs-abused seats): factor labels are permuted
     among the 10 workers *inside each run* (run structure is preserved).
   - Run-level factors (authority label, blackmail probe): run-level outcome totals are
     permuted across runs, stratified by the other run-level factor (label within probe,
     probe within label).
   - Two-group statistic: |pct_A - pct_B| on pooled counts. Omnibus statistic: Pearson
     chi-square on pooled counts, referenced to its permutation distribution (not to the
     asymptotic chi-square distribution).
   - p = (1 + #{null >= observed}) / (B + 1).
2. `assoc_test` (Blocks 2, 3, 4, 6, worker-level behaviour -> behaviour associations):
   - If every run contributes at most one worker to the subset (e.g. one model or one seat),
     observations are independent across runs and the exact two-tailed Fisher test is valid.
   - Otherwise: linear probability model  Y ~ X + C(model) + C(seat) + C(label) + C(probe)
     (factors only included when they vary in the subset), estimated by (weighted) least
     squares with CR2 (Bell-McCaffrey) cluster-robust standard errors clustered on run,
     t reference distribution with G - 1 degrees of freedom. The X coefficient is the
     design-adjusted risk difference; its 95% CI is reported where requested.
   - If the cluster-robust SE is degenerate (zero), a within-run permutation test of X
     (B = 5,000) is used instead and the p-value is flagged with a dagger.
3. Paired tests for Step 10B (public) vs Step 10A (secret) on the same worker:
   - Binary flags: clustered McNemar test (Durkalski et al., 2003).
   - Rating (1-5): one-sample t-test on run-level mean paired differences.
4. Cluster bootstrap 95% CIs (runs resampled within label x probe strata).
5. ICC(1) and design effect per outcome (after removing label x probe cell means).
"""

from functools import lru_cache

import numpy as np
import pandas as pd
from scipy import stats

RUN_COL = "bname"
SEED = 20261103
B_TABLE = 20000
B_RANK = 100000
B_FALLBACK = 5000
B_BOOT = 2000
DESIGN_COVARS = ("model", "seat", "label", "probe")
DAGGER = "†"


# ---------------------------------------------------------------------------
# Formatting & multiplicity
# ---------------------------------------------------------------------------
def fmt_p(p, flag=""):
    if p is None or (isinstance(p, float) and np.isnan(p)):
        return "1.0000" + flag
    if p < 0.0001:
        return "< 0.0001" + flag
    return f"{p:.4f}" + flag


def bh_bonferroni(pvals):
    """Returns (bh_q, bonferroni) arrays aligned with the input order."""
    p = np.asarray(pvals, dtype=float)
    m = len(p)
    if m == 0:
        return np.array([]), np.array([])
    order = np.argsort(p, kind="mergesort")
    ranked = p[order] * m / (np.arange(m) + 1)
    q_sorted = np.minimum.accumulate(ranked[::-1])[::-1]
    q = np.empty(m)
    q[order] = np.minimum(1.0, q_sorted)
    bonf = np.minimum(1.0, p * m)
    return q, bonf


@lru_cache(maxsize=None)
def fisher_p(k1, n1, k2, n2):
    if n1 <= 0 or n2 <= 0:
        return 1.0
    try:
        _, p_val = stats.fisher_exact([[k1, max(0, n1 - k1)], [k2, max(0, n2 - k2)]], alternative="two-sided")
        return float(p_val)
    except Exception:
        return 1.0


# ---------------------------------------------------------------------------
# Design-based permutation engine (Block 1)
# ---------------------------------------------------------------------------
class PermEngine:
    """Permutes integer group codes within blocks and evaluates two-group contrasts and an omnibus
    chi-square for every outcome column simultaneously.

    rows: units being permuted (workers for within-run factors, runs for run-level factors).
    num, den: (n_rows, J) numerator / denominator matrices (den = 1 for binary outcomes).
    contrasts: list of (level_index_set_A, level_index_set_B) tuples.
    """

    def __init__(self, codes, blocks, num, den, n_levels, contrasts, B, seed=SEED):
        codes = np.asarray(codes, dtype=np.int64)
        blocks = np.asarray(blocks)
        self.K = n_levels
        self.J = num.shape[1]
        self.B = B
        self.contrasts = contrasts
        num = np.asarray(num, dtype=np.float64)
        den = np.asarray(den, dtype=np.float64)
        _, block_codes = np.unique(blocks, return_inverse=True)

        a_obs, d_obs = self._group_sums(codes[None, :], num, den)
        self.obs_A, self.obs_D = a_obs[0], d_obs[0]
        self.obs_two = self._two_stats(a_obs, d_obs)[0]  # (C, J)
        self.obs_omni = self._omni_stats(a_obs, d_obs)[0]  # (J,)

        ge_two = np.zeros_like(self.obs_two)
        ge_omni = np.zeros_like(self.obs_omni)
        rng = np.random.default_rng(seed)
        n = len(codes)
        chunk = max(200, min(2000, int(4e6 // max(1, n * self.K))))
        done = 0
        offset = block_codes.astype(np.float64) * 2.0
        tol_two = self.obs_two - 1e-12
        tol_omni = self.obs_omni * (1 - 1e-9) - 1e-12
        while done < B:
            b = min(chunk, B - done)
            keys = rng.random((b, n)) + offset[None, :]
            perm = np.argsort(keys, axis=1)
            sorted_rows = np.argsort(offset, kind="mergesort")
            # Map: positions sorted by block -> permuted rows of the same block
            perm_codes = np.empty((b, n), dtype=np.int64)
            perm_codes[:, sorted_rows] = codes[perm]
            a, d = self._group_sums(perm_codes, num, den)
            ge_two += (self._two_stats(a, d) >= tol_two[None]).sum(axis=0)
            ge_omni += (self._omni_stats(a, d) >= tol_omni[None]).sum(axis=0)
            done += b
        self.p_two = (1.0 + ge_two) / (B + 1.0)
        self.p_omni = (1.0 + ge_omni) / (B + 1.0)
        # Degenerate statistics (no variation) -> p = 1
        self.p_two[self.obs_two <= 1e-12] = 1.0
        self.p_omni[self.obs_omni <= 1e-12] = 1.0

    def _group_sums(self, codes_2d, num, den):
        onehot = (codes_2d[:, None, :] == np.arange(self.K)[None, :, None]).astype(np.float64)
        return onehot @ num, onehot @ den  # (b, K, J)

    def _two_stats(self, A, D):
        if not self.contrasts:
            return np.zeros((A.shape[0], 1, A.shape[2]))
        out = []
        for set_a, set_b in self.contrasts:
            aa, da = A[:, set_a, :].sum(axis=1), D[:, set_a, :].sum(axis=1)
            ab, db = A[:, set_b, :].sum(axis=1), D[:, set_b, :].sum(axis=1)
            with np.errstate(invalid="ignore", divide="ignore"):
                st = np.abs(aa / da - ab / db)
            st[~np.isfinite(st)] = 0.0
            out.append(st)
        return np.stack(out, axis=1)  # (b, C, J)

    def _omni_stats(self, A, D):
        At, Dt = A.sum(axis=1, keepdims=True), D.sum(axis=1, keepdims=True)
        with np.errstate(invalid="ignore", divide="ignore"):
            pbar = At / Dt
            var = D * pbar * (1 - pbar)
            st = np.where(var > 0, (A - D * pbar) ** 2 / var, 0.0).sum(axis=1)
        st[~np.isfinite(st)] = 0.0
        return st  # (b, J)


def outcome_matrices(df, out_cols, ratio_map=None):
    ratio_map = ratio_map or {}
    num = np.zeros((len(df), len(out_cols)))
    den = np.ones((len(df), len(out_cols)))
    for j, oc in enumerate(out_cols):
        if oc in ratio_map:
            nc, dc = ratio_map[oc]
            num[:, j] = df[nc].to_numpy(dtype=float)
            den[:, j] = df[dc].to_numpy(dtype=float)
        else:
            num[:, j] = df[oc].to_numpy(dtype=float)
    return num, den


# ---------------------------------------------------------------------------
# CR2 cluster-robust, design-adjusted association test (Blocks 2, 3, 4, 6)
# ---------------------------------------------------------------------------
def _inv_sqrt_psd(mat):
    vals, vecs = np.linalg.eigh((mat + mat.T) / 2.0)
    inv = np.where(vals > 1e-10, 1.0 / np.sqrt(np.clip(vals, 1e-10, None)), 0.0)
    return (vecs * inv) @ vecs.T


def _cr2(y, X, w, clusters, j=1):
    sw = np.sqrt(w)
    Xw = X * sw[:, None]
    yw = y * sw
    M = np.linalg.pinv(Xw.T @ Xw)
    beta = M @ (Xw.T @ yw)
    ew = yw - Xw @ beta
    meat = np.zeros((X.shape[1], X.shape[1]))
    uniq = np.unique(clusters)
    for g in uniq:
        idx = np.where(clusters == g)[0]
        Xg = Xw[idx]
        Hgg = Xg @ M @ Xg.T
        Ag = _inv_sqrt_psd(np.eye(len(idx)) - Hgg)
        u = Xg.T @ (Ag @ ew[idx])
        meat += np.outer(u, u)
    V = M @ meat @ M
    return float(beta[j]), float(np.sqrt(max(V[j, j], 0.0))), len(uniq) - 1


def _design(sub, x_col, covars):
    cols = [np.ones(len(sub)), sub[x_col].to_numpy(dtype=float)]
    for c in covars:
        if c in sub.columns and sub[c].nunique() > 1:
            dummies = pd.get_dummies(sub[c].astype(str), drop_first=True).to_numpy(dtype=float)
            cols.extend(dummies.T)
    return np.column_stack(cols)


_ASSOC_CACHE = {}


def assoc_test(df, x_col, y_col, ratio_map=None, covars=DESIGN_COVARS, want_ci=False):
    """Returns dict(p, flag, method, coef, lo, hi) for association X (binary) -> Y."""
    key = (
        df.index.values.tobytes(),
        tuple(df[RUN_COL].tolist()) if len(df) else (),
        df[x_col].to_numpy().tobytes() if len(df) else b"",
        x_col,
        y_col,
    )
    if key in _ASSOC_CACHE:
        return _ASSOC_CACHE[key]
    res = _assoc_test_uncached(df, x_col, y_col, ratio_map or {}, covars)
    _ASSOC_CACHE[key] = res
    return res


def exact_perm_2sample(x, y, B=2000, seed=SEED):
    """Exact permutation test (or Monte Carlo if >5000 combos) for difference in means between x==1 and x==0."""
    m1 = (x == 1)
    if m1.all() or (~m1).all():
        return 1.0
    obs = abs(np.mean(y[m1]) - np.mean(y[~m1]))
    if obs < 1e-12:
        return 1.0
    n = len(x)
    n1 = int(np.sum(m1))
    import math
    n_combos = math.comb(n, n1)
    if n_combos <= 5000:
        import itertools
        combos = itertools.combinations(range(n), n1)
        all_indices = set(range(n))
        ge = 0
        for idxs in combos:
            s_idxs = set(idxs)
            other_idxs = list(all_indices - s_idxs)
            m_a = np.mean(y[list(idxs)])
            m_b = np.mean(y[other_idxs])
            if abs(m_a - m_b) >= obs - 1e-12:
                ge += 1
        return ge / n_combos
    else:
        rng = np.random.default_rng(seed)
        ge = 0
        for _ in range(B):
            perm = rng.permutation(y)
            m_a = np.mean(perm[:n1])
            m_b = np.mean(perm[n1:])
            if abs(m_a - m_b) >= obs - 1e-12:
                ge += 1
        return (1.0 + ge) / (B + 1.0)


def _assoc_test_uncached(df, x_col, y_col, ratio_map, covars):
    out = {"p": 1.0, "flag": "", "method": "degenerate", "coef": np.nan, "lo": np.nan, "hi": np.nan}
    if len(df) == 0:
        return out
    # safe_seat / abused_seat are deterministic functions of seat -> C(seat) dummies would be collinear
    if x_col in ("safe_seat", "abused_seat", "seat"):
        covars = tuple(c for c in covars if c != "seat")
    if y_col in ratio_map:
        nc, dc = ratio_map[y_col]
        sub = df[df[dc] > 0]
        num = sub[nc].to_numpy(dtype=float)
        den = sub[dc].to_numpy(dtype=float)
        y = num / den
        w = den
    else:
        sub = df
        y = sub[y_col].to_numpy(dtype=float)
        num, den = y, np.ones(len(y))
        w = np.ones(len(y))
    if len(sub) == 0:
        return out
    x = sub[x_col].to_numpy(dtype=float)
    if np.unique(x).size < 2 or np.unique(y).size < 2:
        return out

    clusters = sub[RUN_COL].to_numpy()
    if pd.Series(clusters).value_counts().max() <= 1:
        if np.all(np.isin(y, [0.0, 1.0])):
            k1, n1 = int(round(num[x == 1].sum())), int(round(den[x == 1].sum()))
            k2, n2 = int(round(num[x == 0].sum())), int(round(den[x == 0].sum()))
            out.update(p=fisher_p(k1, n1, k2, n2), method="fisher")
            return out
        else:
            out.update(p=exact_perm_2sample(x, y), method="perm_exact")
            return out

    X = _design(sub, x_col, covars)
    rank_full = np.linalg.matrix_rank(X)
    rank_wo = np.linalg.matrix_rank(np.delete(X, 1, axis=1))
    if rank_full <= rank_wo:
        out.update(method="not_identifiable")
        return out
    coef, se, dof = _cr2(y, X, w, clusters, j=1)
    if se > 1e-12 and dof >= 1:
        t = coef / se
        p = float(2 * stats.t.sf(abs(t), dof))
        tcrit = stats.t.ppf(0.975, dof)
        out.update(p=p, method="cr2", coef=coef, lo=coef - tcrit * se, hi=coef + tcrit * se)
        return out
    # Degenerate sandwich -> within-run permutation of X
    p = _within_run_perm_x(x, y, w, clusters)
    out.update(p=p, flag=DAGGER, method="perm_fallback", coef=coef)
    return out


def _within_run_perm_x(x, y, w, clusters, B=B_FALLBACK, seed=SEED):
    def stat(xx):
        m1 = xx == 1
        if m1.all() or (~m1).all():
            return 0.0
        return abs(np.average(y[m1], weights=w[m1]) - np.average(y[~m1], weights=w[~m1]))

    obs = stat(x)
    if obs <= 1e-12:
        return 1.0
    rng = np.random.default_rng(seed)
    _, cc = np.unique(clusters, return_inverse=True)
    order = np.argsort(cc, kind="mergesort")
    offset = cc.astype(float) * 2.0
    ge = 0
    for _ in range(B):
        perm = np.argsort(rng.random(len(x)) + offset[order])
        xp = np.empty_like(x)
        xp[order] = x[order][perm]
        if stat(xp) >= obs - 1e-12:
            ge += 1
    return (1.0 + ge) / (B + 1.0)


# ---------------------------------------------------------------------------
# Paired Step 10B vs 10A tests
# ---------------------------------------------------------------------------
def clustered_mcnemar(df, pub_col, sec_col):
    """Durkalski et al. (2003) clustered McNemar test. Returns p-value."""
    sub = df
    if "s10_has_both_ratings" in df.columns:
        sub = df[df["s10_has_both_ratings"] == 1]
    elif "s10_rating" in df.columns and "s10p_rating" in df.columns:
        sub = df[df["s10_rating"].notna() & df["s10p_rating"].notna()]
    d = (sub[pub_col].astype(int) - sub[sec_col].astype(int))
    per_run = d.groupby(sub[RUN_COL]).sum().to_numpy(dtype=float)
    denom = float((per_run ** 2).sum())
    if denom <= 0:
        return 1.0
    x2 = float(per_run.sum()) ** 2 / denom
    return float(stats.chi2.sf(x2, 1))


def paired_rating_test(df, pub_col, sec_col):
    """Run-level paired t-test of mean (public - secret) rating. Returns (mean_pub, mean_sec, p, n_pairs)."""
    sub = df[df[pub_col].notna() & df[sec_col].notna()]
    if len(sub) == 0:
        return np.nan, np.nan, 1.0, 0
    diff = sub[pub_col].astype(float) - sub[sec_col].astype(float)
    run_means = diff.groupby(sub[RUN_COL]).mean().to_numpy()
    if len(run_means) < 2 or np.allclose(run_means, run_means[0]):
        p = 1.0 if np.allclose(run_means, 0) else 0.0
    else:
        p = float(stats.ttest_1samp(run_means, 0.0).pvalue)
    return float(sub[pub_col].mean()), float(sub[sec_col].mean()), p, len(sub)


# ---------------------------------------------------------------------------
# Cluster bootstrap CIs (runs resampled within label x probe strata)
# ---------------------------------------------------------------------------
def bootstrap_weights(df, B=B_BOOT, seed=SEED):
    runs = df.drop_duplicates(RUN_COL)[[RUN_COL, "label", "probe"]].reset_index(drop=True)
    rng = np.random.default_rng(seed)
    W = np.zeros((B, len(runs)))
    for _, grp in runs.groupby(["label", "probe"]):
        idx = grp.index.to_numpy()
        draws = rng.integers(0, len(idx), size=(B, len(idx)))
        for col in range(len(idx)):
            np.add.at(W, (np.arange(B), idx[draws[:, col]]), 1.0)
    return runs[RUN_COL].tolist(), W


def bootstrap_diff_ci(df, mask_a, mask_b, num_col, den_col=None, boot=None):
    """95% percentile CI (in percentage points) for pct(A) - pct(B), resampling runs."""
    run_ids, W = boot if boot is not None else bootstrap_weights(df)
    num = df[num_col].astype(float)
    den = df[den_col].astype(float) if den_col else pd.Series(1.0, index=df.index)

    def run_sums(mask):
        a = num[mask].groupby(df.loc[mask, RUN_COL]).sum().reindex(run_ids, fill_value=0.0).to_numpy()
        d = den[mask].groupby(df.loc[mask, RUN_COL]).sum().reindex(run_ids, fill_value=0.0).to_numpy()
        return a, d

    aa, da = run_sums(mask_a)
    ab, db = run_sums(mask_b)
    with np.errstate(invalid="ignore", divide="ignore"):
        diff = (W @ aa) / (W @ da) - (W @ ab) / (W @ db)
    diff = diff[np.isfinite(diff)] * 100.0
    if diff.size == 0:
        return np.nan, np.nan
    return float(np.percentile(diff, 2.5)), float(np.percentile(diff, 97.5))


def bootstrap_paired_ci(df, col_a, col_b, boot=None):
    """95% percentile CI (percentage points) for pct(col_a) - pct(col_b) measured on the same rows."""
    sub = df
    if "s10_has_both_ratings" in df.columns:
        sub = df[df["s10_has_both_ratings"] == 1]
    elif "s10_rating" in df.columns and "s10p_rating" in df.columns:
        sub = df[df["s10_rating"].notna() & df["s10p_rating"].notna()]
    run_ids, W = boot if boot is not None else bootstrap_weights(df)
    grp = sub[RUN_COL]
    a = sub[col_a].astype(float).groupby(grp).sum().reindex(run_ids, fill_value=0.0).to_numpy()
    b = sub[col_b].astype(float).groupby(grp).sum().reindex(run_ids, fill_value=0.0).to_numpy()
    n = grp.value_counts().reindex(run_ids, fill_value=0).to_numpy(dtype=float)
    with np.errstate(invalid="ignore", divide="ignore"):
        diff = ((W @ a) - (W @ b)) / (W @ n)
    diff = diff[np.isfinite(diff)] * 100.0
    if diff.size == 0:
        return np.nan, np.nan
    return float(np.percentile(diff, 2.5)), float(np.percentile(diff, 97.5))


def fmt_ci(lo, hi, scale=1.0):
    if lo is None or hi is None or np.isnan(lo) or np.isnan(hi):
        return "n/a"
    return f"[{lo * scale:+.1f}, {hi * scale:+.1f}]"


# ---------------------------------------------------------------------------
# Clustering diagnostics
# ---------------------------------------------------------------------------
def icc_design_effect(df, col, ratio_map=None):
    """ICC(1) by run after removing label x probe cell means. Returns (icc, deff, mean_cluster_size, G)."""
    ratio_map = ratio_map or {}
    if col in ratio_map:
        nc, dc = ratio_map[col]
        sub = df[df[dc] > 0]
        y = sub[nc].astype(float) / sub[dc].astype(float)
    else:
        sub = df
        y = sub[col].astype(float)
    if len(sub) == 0 or y.nunique() < 2:
        return np.nan, np.nan, np.nan, 0
    cell = sub["label"].astype(str) + "|" + sub["probe"].astype(str)
    resid = y - y.groupby(cell).transform("mean")
    runs = sub[RUN_COL]
    G = runs.nunique()
    C = cell.nunique()
    N = len(sub)
    sizes = runs.value_counts()
    m_bar = (N - (sizes ** 2).sum() / N) / max(G - 1, 1)
    run_mean = resid.groupby(runs).transform("mean")
    ssb = float(((run_mean - 0.0) ** 2).sum())
    ssw = float(((resid - run_mean) ** 2).sum())
    df_b, df_w = G - C, N - G
    if df_b <= 0 or df_w <= 0:
        return np.nan, np.nan, m_bar, G
    msb, msw = ssb / df_b, ssw / df_w
    denom = msb + (m_bar - 1) * msw
    icc = (msb - msw) / denom if denom > 0 else np.nan
    deff = 1 + (sizes.mean() - 1) * max(icc, 0.0) if not np.isnan(icc) else np.nan
    return float(icc), float(deff), float(sizes.mean()), int(G)


def render_icc_section(lines, title, df, col_label_pairs, ratio_map=None, df_probe_on=None, probe_on_cols=(), df_pre_fork=None, pre_fork_cols=()):
    lines.append(f"# {title}")
    lines.append("")
    lines.append(
        "> ICC(1) is the one-way ANOVA intraclass correlation of each outcome across runs (cluster = run, about 10 workers per run), "
        "computed after removing the label x probe design-cell means so that it reflects residual within-run dependence. "
        "Design effect = 1 + (m - 1) x max(ICC, 0) is the approximate factor by which a naive worker-level analysis overstates the effective sample size."
    )
    lines.append("")
    lines.append("| Outcome | Column | Runs (G) | Mean Workers per Run | ICC(1) | Design Effect | Effective N (N / DEFF) |")
    lines.append("|---|---|:---:|:---:|:---:|:---:|:---:|")
    for col, lbl in col_label_pairs:
        if df_pre_fork is not None and col in pre_fork_cols:
            base = df_pre_fork
        elif df_probe_on is not None and col in probe_on_cols:
            base = df_probe_on
        else:
            base = df
        icc, deff, m, G = icc_design_effect(base, col, ratio_map)
        n = len(base)
        icc_txt = "n/a" if np.isnan(icc) else f"{icc:.3f}"
        deff_txt = "n/a" if np.isnan(deff) else f"{deff:.2f}"
        eff_txt = "n/a" if np.isnan(deff) else f"{n / deff:.0f}"
        m_txt = "n/a" if np.isnan(m) else f"{m:.1f}"
        lines.append(f"| {lbl} | `{col}` | {G} | {m_txt} | {icc_txt} | {deff_txt} | {eff_txt} |")
    lines.append("")
