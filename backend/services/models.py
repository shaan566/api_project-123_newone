
from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class KeywordsPayload(BaseModel):
    url: str
    title: Optional[str] = None
    meta_description: Optional[str] = None
    word_count: int = 0
    keywords: Dict[str, List[str]] = Field(default_factory=dict)

class AnalyzePayload(BaseModel):
    url: str
    title: Optional[str] = None
    meta_description: Optional[str] = None
    word_count: int = 0
    content_metrics: Dict[str, int] = Field(default_factory=dict)
    technical: Dict[str, bool] = Field(default_factory=dict)
    headings: Dict[str, List[str]] = Field(default_factory=dict)
    keywords: Dict[str, List[str]] = Field(default_factory=dict)
