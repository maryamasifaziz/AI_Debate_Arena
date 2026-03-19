import os
import requests
from django.conf import settings

GROQ_BASE = "https://api.groq.com/openai/v1/chat/completions"
OPENAI_BASE = "https://api.openai.com/v1/chat/completions"

def _provider_config():
    provider = getattr(settings, "AI_PROVIDER", "groq")
    if provider == "openai":
        return provider, OPENAI_BASE, os.environ.get("OPENAI_API_KEY", ""), getattr(settings, "OPENAI_MODEL", "gpt-5")
    return provider, GROQ_BASE, os.environ.get("GROQ_API_KEY",""), getattr(settings, "GROQ_MODEL", "openai/gpt-oss-20b")

def chat(messages, temperature=0.6, max_tokens=400):
    provider, url, key, model = _provider_config()
    if not key:
        raise RuntimeError(f"Missing API key for provider: {provider}")
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    
    payload = {"model": model, "messages": messages, "temperature": float(temperature), "max_tokens": int(max_tokens)}
    
    r = requests.post(url, headers=headers, json=payload, timeout=60)

    if r.status_code >= 400:
        raise RuntimeError(f"LLM error {r.status_code}: {r.text[:500]}")
    data = r.json()
    return data["choices"][0]["message"]["content"].strip()

def pro_agent(topic, history):
    system = (
        "You are ProAgent in a debate. Your job is to argue FOR the topic. "
        "Be clear, polite, and structured. "
        "Give 3 short arguments, then 1 short question to challenge the opponent. "
        "No markdown."
    )
    messages = [{"role": "system", "content": system}]
    messages += history
    messages.append({"role": "user", "content": f"Topic: {topic}Respond as ProAgent."})
    
    return chat(messages)

def con_agent(topic, history):
    system = (
        "You are ConAgent in a debate. Your job is to argue AGAINST the topic. "
        "Be clear, polite, and structured. "
        "Give 3 short counter-arguments, then 1 short question to challenge the opponent. "
        "No markdown."
    )
    messages = [{"role": "system", "content": system}]
    messages += history
    messages.append({"role": "user", "content": f"Topic: {topic} Respond as ConAgent."})
    return chat(messages)

def judge_agent(topic, pro_text, con_text):
    system = (
        "You are JudgeAgent. Evaluate a debate fairly. "
        "Give a score out of 10 to Pro and Con, then a 4-line summary, then 1 improvement tip for each side. "
        "No markdown."
    )
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": (
            f"Topic:{topic}\n\n"
            f"PRO:\n{pro_text}\n\n"
            f"CON:\n{con_text}\n\n"
            "Judge now."
            )},
    ]
    return chat(messages, temperature=0.3, max_tokens=350)
