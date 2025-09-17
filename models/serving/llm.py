import os
def _openai_generate(prompt):
    import httpx
    headers = {"Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}", "Content-Type":"application/json"}
    body = {"model": os.getenv("OPENAI_MODEL","gpt-4o-mini"),
            "messages":[{"role":"system","content":"You are helpful."},{"role":"user","content":prompt}]}
    r = httpx.post("https://api.openai.com/v1/chat/completions", headers=headers, json=body, timeout=60)
    r.raise_for_status(); return r.json()["choices"][0]["message"]["content"]

def _hf_generate(prompt):
    from transformers import pipeline
    pipe = pipeline("text-generation", model="sshleifer/tiny-gpt2")
    out = pipe(prompt, max_new_tokens=50, do_sample=False)[0]["generated_text"]
    return out[len(prompt):].strip()

class LocalOrOpenAI:
    def __init__(self): self.use_openai = bool(os.getenv("OPENAI_API_KEY"))
    def generate(self, prompt):
        if self.use_openai:
            try: return _openai_generate(prompt)
            except: return _hf_generate(prompt)
        else: return _hf_generate(prompt)

def get_llm(): return LocalOrOpenAI()
