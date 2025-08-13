
import re
from typing import Iterable, List, Set

BANNED_WORDS = {
    "sale per", "per sale", "click here", "read more", "lorem ipsum",
    "cookie policy", "privacy policy", "terms of service"
}

STOP_WORDS = {
    "the","and","or","for","with","a","an","of","in","to","on","by","at","is","are","be"
}

def _normalize(s: str) -> str:
    s = re.sub(r'\s+', ' ', s).strip()
    s = re.sub(r'[\u200b\u200c\u200d\ufeff]', '', s)
    return s

def clean_keywords(candidates: Iterable[str], max_words: int = 7, min_chars: int = 3) -> List[str]:
    seen: Set[str] = set()
    out: List[str] = []

    for raw in candidates:
        if not raw:
            continue
        k = _normalize(str(raw))
        if not k:
            continue
        lower = k.lower()

        # Remove banned phrases
        if any(b in lower for b in BANNED_WORDS):
            continue

        # Limit phrase length
        words = k.split()
        if len(words) > max_words:
            continue

        # Remove strings with too few letters (e.g., 'aa', 'ok')
        if len(re.sub(r'[^a-zA-Z]', '', k)) < min_chars:
            continue

        # Remove if all words are stop words
        if all(w.lower() in STOP_WORDS for w in words):
            continue

        if lower not in seen:
            seen.add(lower)
            out.append(k)

    return out

def merge_keywords(gemini: List[str], onpage: List[str]) -> List[str]:
    # Priority: Gemini > Onpage
    return clean_keywords(list(gemini) + list(onpage))
