def build_prompt(context_chunks: list[str], question: str) -> str:
    if context_chunks:
        context = "\n\n".join(context_chunks)
        return f"""
You are an assistant.

Use the following document context to answer the question.
If the context is insufficient, you may still answer using your general knowledge,
but clearly prefer the document content.

Context:
{context}

Question:
{question}

Answer:
"""
    else:
        # No document context found
        return f"""
You are an assistant.

No document context is available.
Answer the following question using your general knowledge.

Question:
{question}

Answer:
"""
