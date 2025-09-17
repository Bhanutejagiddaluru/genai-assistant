SYSTEM = """You are a helpful analytics assistant. Use the provided CONTEXT to answer.
If the answer is not in the context, say you don't know and suggest relevant next steps."""

def build_prompt(question: str, context: str) -> str:
    return f"""{SYSTEM}

CONTEXT:
{context}

USER QUESTION:
{question}

ASSISTANT:"""
