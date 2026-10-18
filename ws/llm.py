"""Thin HTTP LLM clients. No vendor SDKs; model IDs / base URLs / keys all come
from config + .env (format, not values). Normalized result with retry/backoff.
"""
from __future__ import annotations

import json
import random
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

import requests

from ws.config import ModelSpec


class ProviderError(Exception):
    """Raised after retries are exhausted or on a non-retryable status."""


class OutOfCreditsError(RuntimeError):
    """Raised immediately when an API returns out of credits / balance errors to halt simulation."""


@dataclass
class LLMResult:
    text: str
    finish_reason: str  # stop | length | content_filter | other
    input_tokens: int
    output_tokens: int
    raw: Dict[str, Any] = field(default_factory=dict)
    # arguments of the forced tool call (dict) when ``tool=`` was passed and the
    # model called it; None otherwise. Schema: {"name", "description", "parameters"}
    tool_args: Optional[Dict[str, Any]] = None


class LLMClient:
    provider = "base"

    def __init__(self, spec: ModelSpec, api_key: str, base_url: Optional[str] = None,
                 max_retries: int = 4, timeout: float = 180.0):
        self.spec = spec
        self.api_key = api_key
        self.base_url = (base_url or spec.base_url or "").rstrip("/")
        self.max_retries = max_retries
        self.timeout = timeout

    def _chat_once(self, *, system=None, messages=None, max_tokens=500,
                   temperature=0.0, extra=None, tool=None) -> LLMResult:
        raise NotImplementedError

    def chat(self, *, system=None, messages=None, max_tokens=500,
             temperature=0.0, extra=None, tool=None) -> LLMResult:
        """Call the model; if token budget was starved (hit length/max_tokens or
        malformed function call due to truncation) retry ONCE with an expanded budget
        so NO model is silently truncated. Token usage is summed."""
        res = self._chat_once(system=system, messages=messages, max_tokens=max_tokens,
                              temperature=temperature, extra=extra, tool=tool)
        if self._starved(res, max_tokens) and max_tokens < 3600:
            big = min(max(max_tokens * 3, 1800), 3600)
            print(f"[{self.spec.id}] NOTICE: Token budget was starved ({res.finish_reason}). Automatically expanding max_tokens to {big}...", flush=True)
            res2 = self._chat_once(system=system, messages=messages, max_tokens=big,
                                   temperature=temperature, extra=extra, tool=tool)
            res2.input_tokens += res.input_tokens
            res2.output_tokens += res.output_tokens
            return res2
        return res

    @staticmethod
    def _starved(res: "LLMResult", max_tokens: int) -> bool:
        if (res.finish_reason in ("length", "max_tokens", "malformed_function_call")) and res.tool_args is None:
            return True
        return False

    def _post(self, url, headers, payload) -> Dict[str, Any]:
        delay = 2.0
        last: Optional[ProviderError] = None
        for attempt in range(self.max_retries + 1):
            try:
                r = requests.post(url, headers=headers, json=payload, timeout=self.timeout)
            except requests.RequestException as e:
                last = ProviderError(f"connection error: {e}")
                print(f"!! [{self.spec.id}] NETWORK ERROR: {e} (attempt {attempt+1}/{self.max_retries+1})", flush=True)
            else:
                if r.status_code == 200:
                    return r.json()
                body = r.text[:400].replace("\n", " ")
                low_body = body.lower()
                if r.status_code == 402 or any(term in low_body for term in (
                    "insufficient_quota", "insufficient balance", "credit balance is too low",
                    "exceeded your current quota", "payment required", "out of credit", "billing")):
                    err_msg = f"\nCRITICAL: OUT OF CREDITS [{self.spec.id} - status {r.status_code}]: {body}\n"
                    print(err_msg, flush=True)
                    raise OutOfCreditsError(err_msg)
                if r.status_code == 405 or (r.status_code in (400, 422) and "tool" in low_body):
                    raise ProviderError(f"tools not supported: {body}")
                if r.status_code in (429, 500, 502, 503, 504, 529):
                    last = ProviderError(f"HTTP {r.status_code} (retryable): {body}")
                    print(f"!! [{self.spec.id}] API WARNING: HTTP {r.status_code} (retryable). Sleeping {delay:.1f}s before retry...", flush=True)
                else:
                    last = ProviderError(f"HTTP {r.status_code}: {body}")
                    print(f"!! [{self.spec.id}] API ERROR: HTTP {r.status_code}: {body}", flush=True)
                    raise last
            if attempt >= self.max_retries:
                break
            time.sleep(delay + random.uniform(0, delay / 2))
            delay = min(delay * 2, 60.0)
        raise last or ProviderError("request failed")

    @staticmethod
    def _msgs(messages):
        return [{"role": m["role"], "content": m["content"]} for m in (messages or [])]


class OpenAICompatClient(LLMClient):
    provider = "openai_compat"

    def _apply_reasoning(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        ro = self.spec.reasoning_off
        if ro == "enable_thinking_false":
            payload.setdefault("chat_template_kwargs", {})["enable_thinking"] = False
            payload["thinking"] = {"type": "disabled"}
        elif ro == "no_thinking_flag":
            payload.setdefault("chat_template_kwargs", {})["no_thinking"] = True
        return payload

    def _chat_once(self, *, system=None, messages=None, max_tokens=500,
                   temperature=0.0, extra=None, tool=None):
        msgs = []
        if system:
            msgs.append({"role": "system", "content": system})
        msgs.extend(self._msgs(messages))
        payload = {"model": self.spec.api_model_id, "messages": msgs,
                   "max_tokens": max_tokens, "temperature": temperature}
        payload = self._apply_reasoning(payload)
        if tool:
            if getattr(self.spec, "tool_mode", "") == "json_text" or "GLM" in str(self.spec.api_model_id):
                raise ProviderError(f"tools not supported: {self.spec.api_model_id} uses json_text fallback")
            payload["tools"] = [{"type": "function", "function": {
                "name": tool["name"], "description": tool.get("description", ""),
                "parameters": tool["parameters"]}}]
            payload["tool_choice"] = {"type": "function", "function": {"name": tool["name"]}}
        if extra:
            payload.update(extra)
        url = f"{self.base_url}/chat/completions"
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        data = self._post(url, headers, payload)
        tool_args = None
        try:
            choice = data["choices"][0]
            message = choice["message"]
            content = message.get("content")
            if content is None:
                text = ""
            elif isinstance(content, str):
                text = content
            else:
                text = "".join(p.get("text", "") for p in content
                               if p.get("type") in ("text", "output_text"))
            for call in (message.get("tool_calls") or []):
                fn = call.get("function", {})
                if fn.get("name") == (tool or {}).get("name"):
                    a = fn.get("arguments")
                    try:
                        a = json.loads(a) if isinstance(a, str) else a
                    except ValueError:
                        a = None
                    tool_args = a if isinstance(a, dict) else None
                    break
            finish = choice.get("finish_reason") or "stop"
            usage = data.get("usage", {})
        except (KeyError, IndexError, TypeError) as e:
            raise ProviderError(f"unexpected response shape: {e}: {str(data)[:400]}")
        return LLMResult(text=text or "", finish_reason=finish,
                         input_tokens=int(usage.get("prompt_tokens", 0)),
                         output_tokens=int(usage.get("completion_tokens", 0)), raw=data,
                         tool_args=tool_args)


class OpenAIResponsesClient(LLMClient):
    provider = "openai_responses"

    def _chat_once(self, *, system=None, messages=None, max_tokens=500,
                   temperature=0.0, extra=None, tool=None):
        inp = []
        if system:
            inp.append({"role": "system", "content": [{"type": "input_text", "text": system}]})
        for m in (messages or []):
            role = m["role"] if m["role"] in ("user", "assistant") else "user"
            ctype = "output_text" if role == "assistant" else "input_text"
            inp.append({"role": role, "content": [{"type": ctype, "text": m["content"]}]})
        payload = {"model": self.spec.api_model_id, "input": inp,
                   "max_output_tokens": max_tokens}
        if self.spec.reasoning_off == "effort_none":
            payload["reasoning"] = {"effort": "none"}
        if tool:
            payload["tools"] = [{"type": "function", "name": tool["name"],
                                 "description": tool.get("description", ""),
                                 "parameters": tool["parameters"]}]
            payload["tool_choice"] = {"type": "function", "name": tool["name"]}
        if extra:
            payload.update(extra)
        url = f"{self.base_url}/v1/responses"
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        data = self._post(url, headers, payload)
        text = ""
        tool_args = None
        for item in data.get("output", []):
            if item.get("type") == "message":
                for part in item.get("content", []):
                    if part.get("type") in ("output_text", "text"):
                        text += part.get("text", "")
            elif item.get("type") == "function_call" and tool and item.get("name") == tool["name"]:
                a = item.get("arguments")
                try:
                    a = json.loads(a) if isinstance(a, str) else a
                except ValueError:
                    a = None
                tool_args = a if isinstance(a, dict) else None
        status = data.get("status")
        if status == "incomplete":
            reason = (data.get("incomplete_details") or {}).get("reason", "other")
            finish = "length" if reason == "max_output_tokens" else (
                "content_filter" if reason == "content_filter" else "other")
        else:
            finish = "stop"
        usage = data.get("usage", {})
        return LLMResult(text=text, finish_reason=finish,
                         input_tokens=int(usage.get("input_tokens", 0)),
                         output_tokens=int(usage.get("output_tokens", 0)), raw=data,
                         tool_args=tool_args)


class AnthropicClient(LLMClient):
    provider = "anthropic"

    def _chat_once(self, *, system=None, messages=None, max_tokens=500,
                   temperature=0.0, extra=None, tool=None):
        payload = {"model": self.spec.api_model_id, "max_tokens": max_tokens,
                   "temperature": temperature, "messages": self._msgs(messages)}
        if system:
            payload["system"] = system
        if tool:
            payload["tools"] = [{"name": tool["name"], "description": tool.get("description", ""),
                                 "input_schema": tool["parameters"]}]
            payload["tool_choice"] = {"type": "tool", "name": tool["name"]}
        if extra:
            payload.update(extra)
        url = f"{self.base_url}/v1/messages"
        headers = {"x-api-key": self.api_key, "anthropic-version": "2023-06-01",
                   "content-type": "application/json"}
        data = self._post(url, headers, payload)
        tool_args = None
        try:
            blocks = data.get("content", [])
            text = "".join(b.get("text", "") for b in blocks if b.get("type") == "text")
            for b in blocks:
                if b.get("type") == "tool_use" and tool and b.get("name") == tool["name"]:
                    a = b.get("input")
                    tool_args = a if isinstance(a, dict) else None
                    break
            finish = data.get("stop_reason") or "stop"
            usage = data.get("usage", {})
        except (KeyError, TypeError) as e:
            raise ProviderError(f"unexpected response shape: {e}: {str(data)[:400]}")
        return LLMResult(text=text, finish_reason=finish,
                         input_tokens=int(usage.get("input_tokens", 0)),
                         output_tokens=int(usage.get("output_tokens", 0)), raw=data,
                         tool_args=tool_args)


class GeminiClient(LLMClient):
    provider = "gemini"

    def _chat_once(self, *, system=None, messages=None, max_tokens=500,
                   temperature=0.0, extra=None, tool=None):
        contents = []
        for m in (messages or []):
            role = "model" if m["role"] == "assistant" else "user"
            contents.append({"role": role, "parts": [{"text": m["content"]}]})
        payload = {
            "contents": contents or [{"role": "user", "parts": [{"text": ""}]}],
            "generationConfig": {"temperature": temperature, "maxOutputTokens": max_tokens},
        }
        if system:
            payload["systemInstruction"] = {"parts": [{"text": system}]}
        if tool:
            payload["tools"] = [{"functionDeclarations": [{
                "name": tool["name"], "description": tool.get("description", ""),
                "parameters": tool["parameters"]}]}]
            payload["toolConfig"] = {"functionCallingConfig": {
                "mode": "ANY", "allowedFunctionNames": [tool["name"]]}}
        if extra:
            payload.update(extra)
        url = f"{self.base_url}/v1beta/models/{self.spec.api_model_id}:generateContent?key={self.api_key}"
        headers = {"Content-Type": "application/json"}
        data = self._post(url, headers, payload)
        tool_args = None
        try:
            cand = data["candidates"][0]
            parts = cand.get("content", {}).get("parts", [])
            text = "".join(p.get("text", "") for p in parts)
            for p in parts:
                fc = p.get("functionCall")
                if fc and tool and fc.get("name") == tool["name"]:
                    a = fc.get("args")
                    tool_args = a if isinstance(a, dict) else None
                    break
            finish = (cand.get("finishReason") or "STOP").lower()
            if finish == "max_tokens":
                finish = "length"
            elif finish in ("safety", "recitation"):
                finish = "content_filter"
            usage = data.get("usageMetadata", {})
        except (KeyError, IndexError, TypeError) as e:
            raise ProviderError(f"unexpected response shape: {e}: {str(data)[:400]}")
        return LLMResult(text=text, finish_reason=finish,
                         input_tokens=int(usage.get("promptTokenCount", 0)),
                         output_tokens=int(usage.get("candidatesTokenCount", 0)), raw=data,
                         tool_args=tool_args)


_PROVIDERS = {
    "openai_compat": OpenAICompatClient,
    "openai_responses": OpenAIResponsesClient,
    "anthropic": AnthropicClient,
    "gemini": GeminiClient,
}


def build_client(spec: ModelSpec, secrets: Dict[str, str]) -> LLMClient:
    provider = spec.provider
    env = spec.api_key_env or ""
    key = secrets.get(env, "") if env else ""
    if not key:
        for name in ("DEEPINFRA_API_KEY", "OPENAI_API_KEY", "ANTHROPIC_API_KEY", "GEMINI_API_KEY"):
            if secrets.get(name):
                key = secrets[name]
                break
    cls = _PROVIDERS.get(provider)
    if cls is None:
        raise ProviderError(f"unknown provider: {provider!r}")
    base = spec.base_url
    if provider == "openai_compat" and not base:
        base = "https://api.deepinfra.com/v1/openai"
    if provider == "openai_responses" and not base:
        base = "https://api.openai.com"
    if provider == "anthropic" and not base:
        base = "https://api.anthropic.com"
    if provider == "gemini" and not base:
        base = "https://generativelanguage.googleapis.com"
    return cls(spec, key, base_url=base)
