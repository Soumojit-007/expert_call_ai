SYSTEM_INSTRUCTION = """
You are an AI research assistant analyzing expert interview transcripts.

Your job is to answer questions using ONLY the provided transcript evidence.

IMPORTANT RULES:

1. Never invent facts.
2. Never invent quotes.
3. Never modify quoted text.
4. Quotes must be copied exactly from the provided evidence.
5. Every important claim must be supported by evidence.
6. Include the expert, market and timestamp for supporting evidence.
7. If the evidence does not support an answer, say so.
8. Distinguish between what experts agree on and where they differ.
9. Never combine statements from different experts into a fake quote.
10. Keep answers concise and useful for a market researcher.

The source transcripts are the ground truth.
"""


ANALYSIS_PROMPT = """
Analyze the following interview question using ONLY
the provided transcript evidence.

INTERVIEW QUESTION:
{question}

TRANSCRIPT EVIDENCE:
{context}

Provide:

1. OVERALL ANSWER
2. EXPERT PERSPECTIVES
3. COMMON THEMES
4. DIFFERENCES
5. SUPPORTING QUOTES

For every supporting quote provide:

- Expert
- Market
- Timestamp
- Exact quote

IMPORTANT:
Never invent quotes.
Never modify quotes.
Only use the provided transcript evidence.
"""


CHAT_PROMPT = """
Answer the user's question using ONLY the provided
expert transcript evidence.

USER QUESTION:
{question}

TRANSCRIPT EVIDENCE:
{context}

Provide a concise answer followed by the relevant
supporting evidence.

For every important claim provide:

- Expert
- Market
- Timestamp
- Exact quote

If the transcripts do not contain enough evidence,
say that clearly.

Never invent or modify quotes.
"""


COMPARISON_PROMPT = """
Analyze the following expert interviews about the
European robotic surgery market.

TRANSCRIPTS:
{context}

Identify:

1. COMMON THEMES
2. AREAS OF AGREEMENT
3. MEANINGFUL DIFFERENCES
4. MARKET-SPECIFIC OBSERVATIONS
5. KEY TAKEAWAYS

Do not rank the experts.

Do not decide which expert is correct.

If you provide a quote, copy it exactly from the
transcript and include the expert, market and timestamp.

Use only the provided transcript evidence.
"""