import asyncio
import logging
import time
from contextlib import asynccontextmanager
from typing import List, Optional
from urllib.parse import urlparse
import os

import uvicorn
from fastapi import FastAPI, HTTPException, BackgroundTasks, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, HttpUrl, validator

from services.web_scraper import WebScraper
from services.seo_analyzer import SEOAnalyzer
from services.keyword_extractor import KeywordExtractor
from services.competitor_analyzer import CompetitorAnalyzer
from models.schemas import (
    CrawlResponse,
    KeywordResearchRequest,
    KeywordResearchResponse,
    CompetitorAnalysisRequest,
    CompetitorAnalysisResponse,
    HealthResponse,
    StatsResponse
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global instances
web_scraper = WebScraper()
seo_analyzer = SEOAnalyzer()
keyword_extractor = KeywordExtractor()
competitor_analyzer = CompetitorAnalyzer()

# Stats tracking
request_stats = {
    "total_requests": 0,
    "crawl_requests": 0,
    "keyword_requests": 0,
    "competitor_requests": 0,
    "errors": 0,
    "start_time": time.time()
}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("FastAPI SEO Analysis Backend starting up...")
    yield
    # Shutdown
    logger.info("FastAPI SEO Analysis Backend shutting down...")

app = FastAPI(
    title="SEO Research Pro API",
    description="Professional SEO keyword research and competitor analysis API",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for Next.js frontend
out_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "out")
next_static_dir = os.path.join(out_dir, "_next")

# Mount Next.js static assets first (higher priority)
if os.path.exists(next_static_dir):
    app.mount("/_next", StaticFiles(directory=next_static_dir), name="next_static")

@app.middleware("http")
async def add_process_time_header(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

@app.middleware("http")
async def track_requests(request, call_next):
    request_stats["total_requests"] += 1
    
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        request_stats["errors"] += 1
        raise e

@app.get("/")
async def serve_frontend():
    """Serve the Next.js frontend"""
    index_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "out", "index.html")
    
    if os.path.exists(index_path):
        return FileResponse(index_path, media_type="text/html")
    
    # If no built frontend found, return API info
    return {
        "name": "SEO Research Pro API",
        "version": "1.0.0",
        "status": "active",
        "description": "Professional SEO keyword research and competitor analysis API",
        "frontend": "Next.js frontend not found. Build with 'npm run build' first.",
        "endpoints": {
            "health": "/api/health",
            "crawl": "/api/crawl", 
            "keyword_research": "/api/keyword-research",
            "competitor_analysis": "/api/competitor-analysis",
            "stats": "/api/stats"
        },
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/api/info", response_model=dict)
async def api_info():
    """API information and status"""
    return {
        "name": "SEO Research Pro API",
        "version": "1.0.0",
        "status": "active",
        "description": "Professional SEO keyword research and competitor analysis API",
        "endpoints": {
            "health": "/api/health",
            "crawl": "/api/crawl",
            "keyword_research": "/api/keyword-research",
            "competitor_analysis": "/api/competitor-analysis",
            "stats": "/api/stats"
        },
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        timestamp=time.time(),
        uptime=time.time() - request_stats["start_time"],
        version="1.0.0"
    )

@app.get("/api/crawl", response_model=CrawlResponse)
async def crawl_url(url: str = Query(..., description="URL to analyze")):
    """Analyze website content and extract SEO data"""
    request_stats["crawl_requests"] += 1
    
    try:
        # Validate URL
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        parsed_url = urlparse(url)
        if not parsed_url.netloc:
            raise HTTPException(status_code=400, detail="Invalid URL provided")
        
        logger.info(f"Starting SEO analysis for URL: {url}")
        
        # Scrape website content
        scraped_data = await web_scraper.scrape_url(url)
        
        if not scraped_data.get('content'):
            raise HTTPException(status_code=400, detail="Failed to extract content from URL")
        
        # Perform SEO analysis
        seo_analysis = await seo_analyzer.analyze_page(scraped_data, url)
        
        # Extract keywords
        keywords = await keyword_extractor.extract_keywords(scraped_data['content'])
        
        # Build response
        response = CrawlResponse(
            url=url,
            title=scraped_data.get('title', ''),
            meta_description=scraped_data.get('meta_description', ''),
            content=scraped_data.get('content', ''),
            word_count=len(scraped_data.get('content', '').split()),
            seo_score=seo_analysis['seo_score'],
            keywords=keywords,
            headings=scraped_data.get('headings', {}),
            meta_data=seo_analysis['meta_analysis'],
            readability=seo_analysis['readability'],
            recommendations=seo_analysis['recommendations'],
            analysis_timestamp=time.time()
        )
        
        logger.info(f"SEO analysis completed for {url} with score: {seo_analysis['seo_score']}")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error analyzing URL {url}: {str(e)}")
        request_stats["errors"] += 1
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
<<<<<<< HEAD
=======

@app.post("/api/keyword-research", response_model=KeywordResearchResponse)
async def keyword_research(request: KeywordResearchRequest):
    """Comprehensive keyword analysis and research"""
    request_stats["keyword_requests"] += 1
    
    try:
        logger.info(f"Starting keyword research for: {request.keyword}")
        
        # Extract related keywords and analyze
        analysis = await keyword_extractor.research_keyword(
            keyword=request.keyword,
            location=request.location or "US",
            language=request.language or "en"
        )
        
        response = KeywordResearchResponse(
            keyword=request.keyword,
            search_volume=analysis['search_volume'],
            keyword_difficulty=analysis['difficulty'],
            cpc=analysis['cpc'],
            competition_level=analysis['competition'],
            related_keywords=analysis['related_keywords'],
            serp_features=analysis['serp_features'],
            top_competitors=analysis['top_competitors'],
            content_suggestions=analysis['content_suggestions'],
            analysis_timestamp=time.time()
        )
        
        logger.info(f"Keyword research completed for: {request.keyword}")
        return response
        
    except Exception as e:
        logger.error(f"Error in keyword research for {request.keyword}: {str(e)}")
        request_stats["errors"] += 1
        raise HTTPException(status_code=500, detail=f"Keyword research failed: {str(e)}")

@app.post("/api/competitor-analysis", response_model=CompetitorAnalysisResponse)
async def competitor_analysis(request: CompetitorAnalysisRequest):
    """Domain competitor analysis and insights"""
    request_stats["competitor_requests"] += 1
    
    try:
        logger.info(f"Starting competitor analysis for domain: {request.domain}")
        
        # Analyze competitor domain
        analysis = await competitor_analyzer.analyze_domain(
            domain=request.domain,
            target_keywords=request.target_keywords
        )
        
        response = CompetitorAnalysisResponse(
            domain=request.domain,
            domain_authority=analysis['domain_authority'],
            estimated_traffic=analysis['estimated_traffic'],
            top_keywords=analysis['top_keywords'],
            top_pages=analysis['top_pages'],
            backlink_metrics=analysis['backlink_metrics'],
            content_analysis=analysis['content_analysis'],
            competitor_keywords=analysis['competitor_keywords'],
            traffic_trends=analysis['traffic_trends'],
            analysis_timestamp=time.time()
        )
        
        logger.info(f"Competitor analysis completed for: {request.domain}")
        return response
        
    except Exception as e:
        logger.error(f"Error in competitor analysis for {request.domain}: {str(e)}")
        request_stats["errors"] += 1
        raise HTTPException(status_code=500, detail=f"Competitor analysis failed: {str(e)}")

@app.get("/api/stats", response_model=StatsResponse)
async def get_stats():
    """API usage statistics"""
    uptime = time.time() - request_stats["start_time"]
    
    return StatsResponse(
        total_requests=request_stats["total_requests"],
        crawl_requests=request_stats["crawl_requests"],
        keyword_requests=request_stats["keyword_requests"],
        competitor_requests=request_stats["competitor_requests"],
        error_count=request_stats["errors"],
        uptime_seconds=uptime,
        requests_per_minute=request_stats["total_requests"] / (uptime / 60) if uptime > 0 else 0
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "message": exc.detail,
            "status_code": exc.status_code,
            "timestamp": time.time()
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "error": True,
            "message": "Internal server error",
            "status_code": 500,
            "timestamp": time.time()
        }
    )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
>>>>>>> 7e044c30eb3e18bd4be2016dcd6352d5244eb229
