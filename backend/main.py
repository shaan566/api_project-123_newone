
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List

from models.web_scraper import WebScraper
from models.seo_analyzer import SEOAnalyzer
from services.api_key import suggest_keywords_with_gemini
from services.cleaning import clean_keywords, merge_keywords
from services.models import KeywordsPayload, AnalyzePayload

app = FastAPI(title="SEO Keyword Backend", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

scraper = WebScraper()
analyzer = SEOAnalyzer()

@app.get("/health")
async def health():
    return {"ok": True}

@app.get("/keywords", response_model=KeywordsPayload)
async def keywords(url: str = Query(..., description="Page URL to analyze"),
                   gemini_top_n: int = 30):
    try:
        page = await scraper.scrape(url)
        # Gemini keywords (SEO-focused)
        gemini_kws = suggest_keywords_with_gemini(page.get("content_text",""), num_keywords=gemini_top_n)
        # On-page phrases
        onpage_kws = page.get("onpage_keywords", [])
        # Merge with priority
        merged = merge_keywords(gemini_kws, onpage_kws)

        return KeywordsPayload(
            url=url,
            title=page.get("title"),
            meta_description=page.get("meta_description"),
            word_count=page.get("word_count", 0),
            keywords={
                "gemini": clean_keywords(gemini_kws),
                "onpage": clean_keywords(onpage_kws),
                "merged": merged
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/analyze", response_model=AnalyzePayload)
async def analyze(url: str = Query(..., description="Page URL to analyze"),
                  gemini_top_n: int = 20):
    try:
        page = await scraper.scrape(url)
        audit = analyzer.analyze(page)
        gemini_kws = suggest_keywords_with_gemini(page.get("content_text",""), num_keywords=gemini_top_n)
        onpage_kws = page.get("onpage_keywords", [])
        merged = merge_keywords(gemini_kws, onpage_kws)

        return AnalyzePayload(
            url=url,
            title=page.get("title"),
            meta_description=page.get("meta_description"),
            word_count=page.get("word_count", 0),
            content_metrics=audit["content_metrics"],
            technical=audit["technical"],
            headings=page.get("headings", {}),
            keywords={
                "gemini": clean_keywords(gemini_kws),
                "onpage": clean_keywords(onpage_kws),
                "merged": merged
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
