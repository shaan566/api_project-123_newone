
import os
from typing import List
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("AIzaSyA5JT5v7VuGVNPAdEyh6jUjYrifVSFbJ9Q", "").strip()

def _fallback_keywords(content: str, num_keywords: int = 30) -> List[str]:
    # Simple fallback: extract capitalized phrases and frequent short phrases
    import re
    from collections import Counter
    words = re.findall(r"[A-Za-z][A-Za-z\-']+", content)[:5000]
    phrases = []
    # short n-grams up to 4 words
    for n in (1,2,3,4):
        for i in range(len(words)-n+1):
            phrase = ' '.join(words[i:i+n])
            if 3 <= len(phrase) <= 50:
                phrases.append(phrase)
    common = [p for p,_ in Counter(phrases).most_common(num_keywords*3)]
    # light cleaning
    uniq = []
    seen = set()
    for p in common:
        lp = p.lower()
        if lp not in seen:
            seen.add(lp)
            uniq.append(p)
    return uniq[:num_keywords]

def suggest_keywords_with_gemini(content: str, num_keywords: int = 30) -> List[str]:
    """Return high-quality SEO-focused keywords via Gemini; fallback if not available."""
    if not content or len(content.strip()) < 20:
        return []

    if not GEMINI_API_KEY:
        return _fallback_keywords(content, num_keywords=num_keywords)

    try:
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = f"""You are an advanced SEO keyword strategist.
From the content below, extract {num_keywords} HIGH-VALUE, SEARCH-INTENT keywords that are:
- Long-tail when possible (3+ words)
- Highly relevant to the main topic
- Include synonyms, related terms, and semantic variations
- No brand names unless central to the topic
- Output ONLY keywords, one per line, no numbering, no bullets, no extra text.

CONTENT START
{content[:12000]}
CONTENT END
"""
        resp = model.generate_content(prompt)
        text = resp.text or ""
        # split lines
        kws = [line.strip("-• ").strip() for line in text.splitlines() if line.strip()]
        # basic post-filter; detailed cleaning happens later
        return [k for k in kws if 3 <= len(k) <= 80][:num_keywords]
    except Exception:
        # safe fallback
        return _fallback_keywords(content, num_keywords=num_keywords)
