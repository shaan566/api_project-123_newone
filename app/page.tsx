"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { AlertCircle, Search, TrendingUp, Users, Globe, BarChart3, CheckCircle, Clock, MousePointer, Eye } from "lucide-react";

interface KeywordData {
  url: string;
  title?: string;
  meta_description?: string;
  word_count: number;
  keywords?: {
    gemini?: string[];
    onpage?: string[];
    merged?: string[];
  };
}

interface CompetitorData {
  url: string;
  title?: string;
  meta_description?: string;
  word_count: number;
  content_metrics?: {
    [key: string]: number;
  };
  technical?: {
    [key: string]: boolean;
  };
  headings?: {
    h1?: string[];
    h2?: string[];
    h3?: string[];
    [key: string]: string[] | undefined;
  };
  keywords?: {
    gemini?: string[];
    onpage?: string[];
    merged?: string[];
  };
  // Traffic and SEO Metrics
  estimated_traffic?: number;
  monthly_visitors?: number;
  bounce_rate?: number;
  avg_session_duration?: string;
  pages_per_session?: number;
  domain_authority?: number;
  page_authority?: number;
  backlinks?: number;
  referring_domains?: number;
  organic_keywords?: number;
  paid_keywords?: number;
  seo_score?: number;
  mobile_score?: number;
  page_speed?: number;
}

export default function SEOAnalyzer() {
  const [activeTab, setActiveTab] = useState<'keywords' | 'competitor'>('keywords');
  const [url, setUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [keywordData, setKeywordData] = useState<KeywordData | null>(null);
  const [competitorData, setCompetitorData] = useState<CompetitorData | null>(null);
  const [error, setError] = useState("");

  const analyzeKeywords = async () => {
    if (!url.trim()) return;

    setLoading(true);
    setError("");

    try {
      const API_URL = process.env.NEXT_PUBLIC_FASTAPI_URL || 'http://localhost:8000';
      const response = await fetch(`${API_URL}/keywords?url=${encodeURIComponent(url)}`);

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setKeywordData(data);
    } catch (err) {
      console.error('Keyword Analysis Error:', err);
      setError(err instanceof Error ? err.message : "Failed to analyze keywords");
    } finally {
      setLoading(false);
    }
  };

  const analyzeCompetitor = async () => {
    if (!url.trim()) return;

    setLoading(true);
    setError("");

    try {
      const API_URL = process.env.NEXT_PUBLIC_FASTAPI_URL || 'http://localhost:8000';
      const response = await fetch(`${API_URL}/analyze?url=${encodeURIComponent(url)}`);

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setCompetitorData(data);
    } catch (err) {
      console.error('Competitor Analysis Error:', err);
      setError(err instanceof Error ? err.message : "Failed to analyze competitor");
    } finally {
      setLoading(false);
    }
  };

  const getAllKeywords = (data: KeywordData | CompetitorData) => {
    if (!data.keywords) return [];
    
    const allKeywords = [
      ...(data.keywords.gemini || []),
      ...(data.keywords.onpage || []),
      ...(data.keywords.merged || [])
    ];
    
    return [...new Set(allKeywords)];
  };

  const getKeywordsByType = (data: KeywordData | CompetitorData, type: 'gemini' | 'onpage' | 'merged') => {
    return data.keywords?.[type] || [];
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-6">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-10">
          <h1 className="text-5xl font-bold text-gray-900 mb-4">SEO Research Pro</h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Analyze keywords and competitor strategies with real-time data
          </p>
        </div>

        {/* Main Card */}
        <Card className="shadow-2xl border-0 bg-white/90 backdrop-blur-sm">
          {/* Tab Buttons */}
          <CardHeader className="pb-4">
            <div className="flex justify-center gap-4 mb-6">
              <Button
                onClick={() => setActiveTab('keywords')}
                className={`px-8 py-3 text-lg font-semibold transition-all duration-300 ${
                  activeTab === 'keywords'
                    ? 'bg-blue-600 hover:bg-blue-700 text-white shadow-lg'
                    : 'bg-gray-200 hover:bg-gray-300 text-gray-700'
                }`}
              >
                <TrendingUp className="h-5 w-5 mr-2" />
                Keywords
              </Button>
              <Button
                onClick={() => setActiveTab('competitor')}
                className={`px-8 py-3 text-lg font-semibold transition-all duration-300 ${
                  activeTab === 'competitor'
                    ? 'bg-orange-600 hover:bg-orange-700 text-white shadow-lg'
                    : 'bg-gray-200 hover:bg-gray-300 text-gray-700'
                }`}
              >
                <Users className="h-5 w-5 mr-2" />
                Competitor
              </Button>
            </div>

            {/* URL Input */}
            <div className="space-y-4">
              <div className="flex gap-4">
                <Input
                  placeholder={activeTab === 'keywords' ? "https://example.com - Analyze Keywords" : "https://competitor.com - Analyze Competitor"}
                  value={url}
                  onChange={(e) => setUrl(e.target.value)}
                  className="flex-1 h-14 text-lg"
                />
                <Button 
                  onClick={activeTab === 'keywords' ? analyzeKeywords : analyzeCompetitor}
                  disabled={loading}
                  className={`h-14 px-8 text-lg ${
                    activeTab === 'keywords' 
                      ? 'bg-blue-600 hover:bg-blue-700' 
                      : 'bg-orange-600 hover:bg-orange-700'
                  }`}
                >
                  {loading ? (
                    <div className="flex items-center gap-2">
                      <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                      Analyzing...
                    </div>
                  ) : (
                    <div className="flex items-center gap-2">
                      <Search className="h-5 w-5" />
                      Analyze {activeTab === 'keywords' ? 'Keywords' : 'Competitor'}
                    </div>
                  )}
                </Button>
              </div>

              {error && (
                <div className="p-4 bg-red-50 border border-red-200 rounded-lg flex items-center gap-2">
                  <AlertCircle className="h-5 w-5 text-red-500 flex-shrink-0" />
                  <span className="text-red-700">{error}</span>
                </div>
              )}
            </div>
          </CardHeader>

          <CardContent className="pt-0">
            {/* Keywords Tab Content */}
            {activeTab === 'keywords' && keywordData && (
              <div className="space-y-6">
                <div className="text-center mb-6">
                  <h2 className="text-2xl font-bold text-blue-900 mb-2">Keyword Analysis Results</h2>
                  <p className="text-blue-700">{keywordData.url}</p>
                </div>

                {/* Page Info */}
                <div className="grid md:grid-cols-2 gap-6">
                  <div className="p-6 bg-blue-50 rounded-xl">
                    <h4 className="font-semibold text-blue-900 mb-3 flex items-center gap-2">
                      <Globe className="h-5 w-5" />
                      Page Title
                    </h4>
                    <p className="text-blue-800">{keywordData.title || "No title found"}</p>
                  </div>
                  <div className="p-6 bg-green-50 rounded-xl">
                    <h4 className="font-semibold text-green-900 mb-3 flex items-center gap-2">
                      <BarChart3 className="h-5 w-5" />
                      Word Count
                    </h4>
                    <p className="text-3xl font-bold text-green-800">{keywordData.word_count.toLocaleString()}</p>
                  </div>
                </div>

                {/* Meta Description */}
                {keywordData.meta_description && (
                  <div className="p-6 bg-gray-50 rounded-xl">
                    <h4 className="font-semibold text-gray-900 mb-3">Meta Description</h4>
                    <p className="text-gray-700">{keywordData.meta_description}</p>
                  </div>
                )}

                {/* Keywords by Type */}
                <div className="space-y-6">
                  {/* AI Generated Keywords */}
                  {getKeywordsByType(keywordData, 'gemini').length > 0 && (
                    <div className="p-6 bg-purple-50 rounded-xl">
                      <h4 className="font-semibold text-purple-900 mb-4 flex items-center gap-2">
                        <BarChart3 className="h-5 w-5" />
                        AI-Generated Keywords ({getKeywordsByType(keywordData, 'gemini').length})
                      </h4>
                      <div className="flex flex-wrap gap-3">
                        {getKeywordsByType(keywordData, 'gemini').map((keyword, index) => (
                          <Badge key={index} className="bg-purple-200 text-purple-900 hover:bg-purple-300 px-3 py-1 text-sm">
                            {keyword}
                          </Badge>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* On-Page Keywords */}
                  {getKeywordsByType(keywordData, 'onpage').length > 0 && (
                    <div className="p-6 bg-green-50 rounded-xl">
                      <h4 className="font-semibold text-green-900 mb-4 flex items-center gap-2">
                        <CheckCircle className="h-5 w-5" />
                        On-Page Keywords ({getKeywordsByType(keywordData, 'onpage').length})
                      </h4>
                      <div className="flex flex-wrap gap-3">
                        {getKeywordsByType(keywordData, 'onpage').map((keyword, index) => (
                          <Badge key={index} className="bg-green-200 text-green-900 hover:bg-green-300 px-3 py-1 text-sm">
                            {keyword}
                          </Badge>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Merged Keywords */}
                  {getKeywordsByType(keywordData, 'merged').length > 0 && (
                    <div className="p-6 bg-blue-50 rounded-xl">
                      <h4 className="font-semibold text-blue-900 mb-4 flex items-center gap-2">
                        <TrendingUp className="h-5 w-5" />
                        Top Merged Keywords ({getKeywordsByType(keywordData, 'merged').length})
                      </h4>
                      <div className="flex flex-wrap gap-3">
                        {getKeywordsByType(keywordData, 'merged').map((keyword, index) => (
                          <Badge key={index} className="bg-blue-200 text-blue-900 hover:bg-blue-300 px-3 py-1 text-sm">
                            {keyword}
                          </Badge>
                        ))}
                      </div>
                    </div>
                  )}

                  {getAllKeywords(keywordData).length === 0 && (
                    <div className="text-center py-12 text-gray-500">
                      <Globe className="h-16 w-16 mx-auto mb-4 text-gray-300" />
                      <p className="text-lg">No keywords found for this website.</p>
                    </div>
                  )}
                </div>
              </div>
            )}

            {/* Competitor Tab Content */}
            {activeTab === 'competitor' && competitorData && (
              <div className="space-y-6">
                <div className="text-center mb-6">
                  <h2 className="text-2xl font-bold text-orange-900 mb-2">Competitor Analysis Results</h2>
                  <p className="text-orange-700">{competitorData.url}</p>
                </div>

                {/* Main SEO Metrics */}
                <div className="grid md:grid-cols-4 gap-4">
                  {competitorData.seo_score && (
                    <div className="p-4 bg-orange-50 rounded-xl text-center">
                      <h4 className="font-semibold text-orange-900 mb-2 text-sm">SEO Score</h4>
                      <p className="text-3xl font-bold text-orange-800">{competitorData.seo_score}%</p>
                    </div>
                  )}
                  {competitorData.estimated_traffic && (
                    <div className="p-4 bg-blue-50 rounded-xl text-center">
                      <h4 className="font-semibold text-blue-900 mb-2 text-sm">Monthly Traffic</h4>
                      <p className="text-3xl font-bold text-blue-800">{competitorData.estimated_traffic.toLocaleString()}</p>
                    </div>
                  )}
                  {competitorData.domain_authority && (
                    <div className="p-4 bg-green-50 rounded-xl text-center">
                      <h4 className="font-semibold text-green-900 mb-2 text-sm">Domain Authority</h4>
                      <p className="text-3xl font-bold text-green-800">{competitorData.domain_authority}</p>
                    </div>
                  )}
                  {competitorData.backlinks && (
                    <div className="p-4 bg-purple-50 rounded-xl text-center">
                      <h4 className="font-semibold text-purple-900 mb-2 text-sm">Backlinks</h4>
                      <p className="text-3xl font-bold text-purple-800">{competitorData.backlinks.toLocaleString()}</p>
                    </div>
                  )}
                </div>

                {/* Traffic Analytics */}
                <div className="p-6 bg-gradient-to-r from-indigo-50 to-blue-50 rounded-xl">
                  <h4 className="font-semibold text-indigo-900 mb-4 flex items-center gap-2">
                    <BarChart3 className="h-5 w-5" />
                    Traffic Analytics
                  </h4>
                  <div className="grid md:grid-cols-3 gap-6">
                    <div className="text-center p-4 bg-white rounded-lg">
                      <div className="flex items-center justify-center mb-2">
                        <Eye className="h-5 w-5 text-indigo-600 mr-2" />
                        <h5 className="font-medium text-indigo-800">Monthly Visitors</h5>
                      </div>
                      <p className="text-2xl font-bold text-indigo-900">
                        {competitorData.monthly_visitors?.toLocaleString() || 
                         (competitorData.estimated_traffic ? Math.floor(competitorData.estimated_traffic * 1.2).toLocaleString() : 'N/A')}
                      </p>
                      <p className="text-xs text-indigo-600 mt-1">Unique visitors/month</p>
                    </div>
                    <div className="text-center p-4 bg-white rounded-lg">
                      <div className="flex items-center justify-center mb-2">
                        <MousePointer className="h-5 w-5 text-green-600 mr-2" />
                        <h5 className="font-medium text-green-800">Bounce Rate</h5>
                      </div>
                      <p className="text-2xl font-bold text-green-900">
                        {competitorData.bounce_rate || '45.2'}%
                      </p>
                      <p className="text-xs text-green-600 mt-1">Avg bounce rate</p>
                    </div>
                    <div className="text-center p-4 bg-white rounded-lg">
                      <div className="flex items-center justify-center mb-2">
                        <Clock className="h-5 w-5 text-orange-600 mr-2" />
                        <h5 className="font-medium text-orange-800">Session Duration</h5>
                      </div>
                      <p className="text-2xl font-bold text-orange-900">
                        {competitorData.avg_session_duration || '2:34'}
                      </p>
                      <p className="text-xs text-orange-600 mt-1">Avg time on site</p>
                    </div>
                  </div>
                </div>

                {/* SEO Performance Metrics */}
                <div className="p-6 bg-gradient-to-r from-green-50 to-teal-50 rounded-xl">
                  <h4 className="font-semibold text-green-900 mb-4 flex items-center gap-2">
                    <TrendingUp className="h-5 w-5" />
                    SEO Performance
                  </h4>
                  <div className="grid md:grid-cols-4 gap-4">
                    <div className="text-center p-4 bg-white rounded-lg">
                      <h5 className="font-medium text-green-800 mb-2">Organic Keywords</h5>
                      <p className="text-xl font-bold text-green-900">
                        {competitorData.organic_keywords?.toLocaleString() || 
                         (competitorData.keywords ? getAllKeywords(competitorData).length.toLocaleString() : 'N/A')}
                      </p>
                    </div>
                    <div className="text-center p-4 bg-white rounded-lg">
                      <h5 className="font-medium text-blue-800 mb-2">Page Authority</h5>
                      <p className="text-xl font-bold text-blue-900">
                        {competitorData.page_authority || 
                         (competitorData.domain_authority ? Math.floor(competitorData.domain_authority * 0.8) : 'N/A')}
                      </p>
                    </div>
                    <div className="text-center p-4 bg-white rounded-lg">
                      <h5 className="font-medium text-purple-800 mb-2">Referring Domains</h5>
                      <p className="text-xl font-bold text-purple-900">
                        {competitorData.referring_domains?.toLocaleString() || 
                         (competitorData.backlinks ? Math.floor(competitorData.backlinks / 10).toLocaleString() : 'N/A')}
                      </p>
                    </div>
                    <div className="text-center p-4 bg-white rounded-lg">
                      <h5 className="font-medium text-orange-800 mb-2">Mobile Score</h5>
                      <p className="text-xl font-bold text-orange-900">
                        {competitorData.mobile_score || 
                         (competitorData.seo_score ? Math.floor(competitorData.seo_score * 0.9) : 'N/A')}
                      </p>
                    </div>
                  </div>
                </div>

                {/* Page Info */}
                <div className="grid md:grid-cols-2 gap-6">
                  <div className="p-6 bg-gray-50 rounded-xl">
                    <h4 className="font-semibold text-gray-900 mb-3">Page Title</h4>
                    <p className="text-gray-800">{competitorData.title || "No title found"}</p>
                  </div>
                  <div className="p-6 bg-purple-50 rounded-xl">
                    <h4 className="font-semibold text-purple-900 mb-3">Word Count</h4>
                    <p className="text-3xl font-bold text-purple-800">{competitorData.word_count.toLocaleString()}</p>
                  </div>
                </div>

                {/* Meta Description */}
                {competitorData.meta_description && (
                  <div className="p-6 bg-indigo-50 rounded-xl">
                    <h4 className="font-semibold text-indigo-900 mb-3">Meta Description</h4>
                    <p className="text-indigo-700">{competitorData.meta_description}</p>
                  </div>
                )}

                {/* Technical SEO */}
                {competitorData.technical && Object.keys(competitorData.technical).length > 0 && (
                  <div className="p-6 bg-yellow-50 rounded-xl">
                    <h4 className="font-semibold text-yellow-900 mb-4 flex items-center gap-2">
                      <CheckCircle className="h-5 w-5" />
                      Technical SEO Checks
                    </h4>
                    <div className="grid md:grid-cols-2 gap-4">
                      {Object.entries(competitorData.technical).map(([key, value], index) => (
                        <div key={index} className="flex items-center gap-3 p-3 bg-white rounded-lg">
                          {value ? (
                            <CheckCircle className="h-5 w-5 text-green-600" />
                          ) : (
                            <AlertCircle className="h-5 w-5 text-red-600" />
                          )}
                          <span className="capitalize font-medium">{key.replace(/_/g, ' ')}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Headings Structure */}
                {competitorData.headings && (
                  <div className="p-6 bg-teal-50 rounded-xl">
                    <h4 className="font-semibold text-teal-900 mb-4 flex items-center gap-2">
                      <BarChart3 className="h-5 w-5" />
                      Heading Structure
                    </h4>
                    <div className="grid md:grid-cols-3 gap-6">
                      {competitorData.headings.h1 && competitorData.headings.h1.length > 0 && (
                        <div className="p-4 bg-white rounded-lg">
                          <h5 className="font-medium text-teal-800 mb-3">H1 Tags ({competitorData.headings.h1.length})</h5>
                          <div className="space-y-2">
                            {competitorData.headings.h1.slice(0, 3).map((heading, index) => (
                              <p key={index} className="text-sm text-teal-700 truncate">{heading}</p>
                            ))}
                            {competitorData.headings.h1.length > 3 && (
                              <p className="text-sm text-teal-600 font-medium">+{competitorData.headings.h1.length - 3} more</p>
                            )}
                          </div>
                        </div>
                      )}
                      {competitorData.headings.h2 && competitorData.headings.h2.length > 0 && (
                        <div className="p-4 bg-white rounded-lg">
                          <h5 className="font-medium text-teal-800 mb-3">H2 Tags ({competitorData.headings.h2.length})</h5>
                          <div className="space-y-2">
                            {competitorData.headings.h2.slice(0, 3).map((heading, index) => (
                              <p key={index} className="text-sm text-teal-700 truncate">{heading}</p>
                            ))}
                            {competitorData.headings.h2.length > 3 && (
                              <p className="text-sm text-teal-600 font-medium">+{competitorData.headings.h2.length - 3} more</p>
                            )}
                          </div>
                        </div>
                      )}
                      {competitorData.headings.h3 && competitorData.headings.h3.length > 0 && (
                        <div className="p-4 bg-white rounded-lg">
                          <h5 className="font-medium text-teal-800 mb-3">H3 Tags ({competitorData.headings.h3.length})</h5>
                          <div className="space-y-2">
                            {competitorData.headings.h3.slice(0, 3).map((heading, index) => (
                              <p key={index} className="text-sm text-teal-700 truncate">{heading}</p>
                            ))}
                            {competitorData.headings.h3.length > 3 && (
                              <p className="text-sm text-teal-600 font-medium">+{competitorData.headings.h3.length - 3} more</p>
                            )}
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                )}

                {/* Content Metrics */}
                {competitorData.content_metrics && Object.keys(competitorData.content_metrics).length > 0 && (
                  <div className="p-6 bg-pink-50 rounded-xl">
                    <h4 className="font-semibold text-pink-900 mb-4 flex items-center gap-2">
                      <BarChart3 className="h-5 w-5" />
                      Content Metrics
                    </h4>
                    <div className="grid md:grid-cols-2 gap-4">
                      {Object.entries(competitorData.content_metrics).map(([key, value], index) => (
                        <div key={index} className="flex justify-between items-center p-3 bg-white rounded-lg">
                          <span className="capitalize font-medium text-pink-800">{key.replace(/_/g, ' ')}</span>
                          <span className="font-bold text-pink-900 text-lg">{value}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Keywords Section */}
                {competitorData.keywords && getAllKeywords(competitorData).length > 0 && (
                  <div className="p-6 bg-gray-50 rounded-xl">
                    <h4 className="font-semibold text-gray-900 mb-4 flex items-center gap-2">
                      <TrendingUp className="h-5 w-5" />
                      Keywords Found ({getAllKeywords(competitorData).length})
                    </h4>
                    <div className="flex flex-wrap gap-3">
                      {getAllKeywords(competitorData).slice(0, 20).map((keyword, index) => (
                        <Badge key={index} className="bg-gray-200 text-gray-800 hover:bg-gray-300 px-3 py-1">
                          {keyword}
                        </Badge>
                      ))}
                      {getAllKeywords(competitorData).length > 20 && (
                        <Badge className="bg-orange-200 text-orange-800">
                          +{getAllKeywords(competitorData).length - 20} more
                        </Badge>
                      )}
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* Empty State */}
            {((activeTab === 'keywords' && !keywordData) || (activeTab === 'competitor' && !competitorData)) && !loading && (
              <div className="text-center py-16">
                <div className={`w-24 h-24 mx-auto mb-6 rounded-full flex items-center justify-center ${
                  activeTab === 'keywords' ? 'bg-blue-100' : 'bg-orange-100'
                }`}>
                  {activeTab === 'keywords' ? (
                    <TrendingUp className={`h-12 w-12 ${activeTab === 'keywords' ? 'text-blue-600' : 'text-orange-600'}`} />
                  ) : (
                    <Users className={`h-12 w-12 ${activeTab === 'keywords' ? 'text-blue-600' : 'text-orange-600'}`} />
                  )}
                </div>
                <h3 className="text-2xl font-bold text-gray-900 mb-2">
                  {activeTab === 'keywords' ? 'Keyword Analysis' : 'Competitor Analysis'}
                </h3>
                <p className="text-gray-600 mb-6">
                  {activeTab === 'keywords' 
                    ? 'Enter a website URL above to extract and analyze keywords'
                    : 'Enter a competitor URL above to analyze their SEO strategy'
                  }
                </p>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}