from typing import List, Dict, Optional, Any, Tuple
from pydantic import BaseModel, HttpUrl, validator
import time

class HealthResponse(BaseModel):
    status: str
    timestamp: float
    uptime: float
    version: str

class StatsResponse(BaseModel):
    total_requests: int
    crawl_requests: int
    keyword_requests: int
    competitor_requests: int
    error_count: int
    uptime_seconds: float
    requests_per_minute: float

class KeywordData(BaseModel):
    keyword: str
    relevance_score: float
    search_volume: int
    keyword_difficulty: int
    cpc: float
    competition: str
    trend: List[int]

class MetaAnalysis(BaseModel):
    title: Dict[str, Any]
    meta_description: Dict[str, Any]
    url_analysis: Dict[str, Any]

class ContentAnalysis(BaseModel):
    word_count: int
    paragraph_count: int
    sentences_count: int
    average_words_per_sentence: float
    average_sentences_per_paragraph: float
    headings_analysis: Dict[str, Any]
    content_score: int

class KeywordAnalysis(BaseModel):
    target_keyword: str
    content_occurrences: int
    title_occurrences: int
    meta_description_occurrences: int
    h1_has_keyword: bool
    h2_has_keyword: bool
    keyword_density: float
    optimal_density_range: Tuple[float, float]
    is_optimal_density: bool
    keyword_score: int

class ReadabilityAnalysis(BaseModel):
    flesch_reading_ease: float
    flesch_kincaid_grade: float
    gunning_fog: float
    automated_readability_index: float
    readability_score: int
    reading_level: str

class TechnicalAnalysis(BaseModel):
    has_meta_description: bool
    has_canonical_url: bool
    has_open_graph: bool
    has_twitter_cards: bool
    total_images: int
    images_without_alt: int
    internal_links: int
    external_links: int
    technical_score: int

class Recommendation(BaseModel):
    type: str
    category: str
    title: str
    description: str
    impact: str

class CrawlResponse(BaseModel):
    url: str
    title: str
    meta_description: str
    content: str
    word_count: int
    seo_score: int
    keywords: List[KeywordData]
    headings: Dict[str, List[str]]
    meta_data: Dict[str, Any]
    readability: ReadabilityAnalysis
    recommendations: List[Recommendation]
    analysis_timestamp: float

class KeywordResearchRequest(BaseModel):
    keyword: str
    location: Optional[str] = "US"
    language: Optional[str] = "en"

class RelatedKeyword(BaseModel):
    keyword: str
    search_volume: int
    keyword_difficulty: int
    cpc: float
    competition: str

class SerpFeature(BaseModel):
    feature: str
    likelihood: float

class TopCompetitor(BaseModel):
    position: int
    url: str
    domain: str
    title: str
    estimated_traffic: int
    domain_authority: int
    word_count: int

class ContentSuggestion(BaseModel):
    type: str
    title: str
    suggested_length: str
    content_type: str

class KeywordResearchResponse(BaseModel):
    keyword: str
    search_volume: int
    keyword_difficulty: int
    cpc: float
    competition_level: str
    related_keywords: List[RelatedKeyword]
    serp_features: List[str]
    top_competitors: List[TopCompetitor]
    content_suggestions: List[ContentSuggestion]
    analysis_timestamp: float

class CompetitorAnalysisRequest(BaseModel):
    domain: str
    target_keywords: Optional[List[str]] = []

class TopKeyword(BaseModel):
    keyword: str
    position: int
    search_volume: int
    keyword_difficulty: int
    cpc: float
    estimated_traffic: int
    competition: str
    trend: str

class TopPage(BaseModel):
    url: str
    title: str
    monthly_traffic: int
    traffic_value: float
    top_keyword: str
    keyword_count: int
    backlinks: int
    page_authority: int

class BacklinkMetrics(BaseModel):
    total_backlinks: int
    referring_domains: int
    dofollow_links: int
    nofollow_links: int
    high_authority_domains: int
    anchor_text_diversity: float
    toxic_links_ratio: float
    link_velocity: int
    lost_links: int

class ContentAnalysisCompetitor(BaseModel):
    average_content_length: int
    content_frequency: str
    content_structure_score: int
    total_headings: int
    main_content_topics: List[str]
    content_quality_score: int
    estimated_posts_per_month: int

class KeywordGap(BaseModel):
    keyword: str
    opportunity_score: int
    estimated_difficulty: int

class OverlappingKeyword(BaseModel):
    keyword: str
    competitor_position: str
    search_volume: int
    difficulty: int

class CompetitorAdvantage(BaseModel):
    keyword: str
    position: str
    search_volume: int
    estimated_traffic: int

class OpportunityKeyword(BaseModel):
    keyword: str
    search_volume: int
    difficulty: int
    opportunity_score: int
    estimated_cpc: float

class CompetitorKeywords(BaseModel):
    keyword_gaps: List[KeywordGap]
    overlapping_keywords: List[OverlappingKeyword]
    competitor_advantages: List[CompetitorAdvantage]
    opportunity_keywords: List[OpportunityKeyword]

class TrafficTrends(BaseModel):
    monthly_traffic: List[int]
    overall_trend: str
    growth_rate: float
    peak_month: int
    lowest_month: int
    average_monthly_traffic: int

class CompetitorAnalysisResponse(BaseModel):
    domain: str
    domain_authority: int
    estimated_traffic: Dict[str, Any]
    top_keywords: List[TopKeyword]
    top_pages: List[TopPage]
    backlink_metrics: BacklinkMetrics
    content_analysis: ContentAnalysisCompetitor
    competitor_keywords: CompetitorKeywords
    traffic_trends: TrafficTrends
    analysis_timestamp: float
