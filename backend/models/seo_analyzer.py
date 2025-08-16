
from typing import Dict

class SEOAnalyzer:
    def analyze(self, page: Dict) -> Dict:
        content = page.get("content_text","")
        meta = page.get("meta",{})
        headings = page.get("headings",{})
        technical = {
            "has_meta_description": bool(meta.get("description")),
            "has_canonical": bool(meta.get("canonical")),
            "has_og": bool(meta.get("og_title") or meta.get("og_description"))
        }
        content_metrics = {
            "word_count": page.get("word_count",0),
            "h1": len(headings.get("h1",[])),
            "h2": len(headings.get("h2",[])),
        }
        return {
            "technical": technical,
            "content_metrics": content_metrics
        }
