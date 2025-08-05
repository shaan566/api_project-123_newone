"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { AlertCircle, CheckCircle, Search, TrendingUp, Users, Zap } from "lucide-react";

interface SEOData {
  url: string;
  title: string;
  meta_description: string;
  content: string;
  word_count: number;
  seo_score: number;
  keywords: Array<{
    keyword: string;
    relevance_score: number;
    search_volume: number;
    keyword_difficulty: number;
    cpc: number;
    competition: string;
    trend: number[];
  }>;
  headings: {
    h1: string[];
    h2: string[];
    h3: string[];
  };
  readability: {
    flesch_reading_ease: number;
    reading_level: string;
    readability_score: number;
  };
  recommendations: Array<{
    type: string;
    category: string;
    title: string;
    description: string;
    impact: string;
  }>;
}

export default function SEOAnalyzer() {
  const [url, setUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [seoData, setSeoData] = useState<SEOData | null>(null);
  const [error, setError] = useState("");

  const analyzeSEO = async () => {
    if (!url) return;

    setLoading(true);
    setError("");
    
    try {
      const response = await fetch(`/api/crawl?url=${encodeURIComponent(url)}`);
      
      if (!response.ok) {
        throw new Error("Failed to analyze website");
      }
      
      const data = await response.json();
      setSeoData(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Analysis failed");
    } finally {
      setLoading(false);
    }
  };

  const getScoreColor = (score: number) => {
    if (score >= 80) return "text-green-600";
    if (score >= 60) return "text-yellow-600";
    return "text-red-600";
  };

  const getCompetitionColor = (competition: string) => {
    switch (competition.toLowerCase()) {
      case "low": return "bg-green-100 text-green-800";
      case "medium": return "bg-yellow-100 text-yellow-800";
      case "high": return "bg-orange-100 text-orange-800";
      case "very high": return "bg-red-100 text-red-800";
      default: return "bg-gray-100 text-gray-800";
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">SEO Research Pro</h1>
          <p className="text-xl text-gray-600">Professional SEO Analysis & Keyword Research Tool</p>
        </div>

        <Card className="mb-8">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Search className="h-5 w-5" />
              Website Analysis
            </CardTitle>
            <CardDescription>
              Enter a URL to get comprehensive SEO analysis and keyword insights
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex gap-4">
              <Input
                placeholder="https://example.com"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                className="flex-1"
              />
              <Button onClick={analyzeSEO} disabled={loading}>
                {loading ? "Analyzing..." : "Analyze SEO"}
              </Button>
            </div>
            {error && (
              <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg flex items-center gap-2">
                <AlertCircle className="h-5 w-5 text-red-500" />
                <span className="text-red-700">{error}</span>
              </div>
            )}
          </CardContent>
        </Card>

        {seoData && (
          <div className="space-y-8">
            {/* Overall Score */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center justify-between">
                  <span>SEO Score</span>
                  <span className={`text-3xl font-bold ${getScoreColor(seoData.seo_score)}`}>
                    {seoData.seo_score}%
                  </span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <Progress value={seoData.seo_score} className="mb-4" />
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div className="text-center">
                    <div className="text-2xl font-bold text-blue-600">{seoData.word_count}</div>
                    <div className="text-sm text-gray-600">Words</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-green-600">{seoData.keywords.length}</div>
                    <div className="text-sm text-gray-600">Keywords Found</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-purple-600">{seoData.readability.readability_score}</div>
                    <div className="text-sm text-gray-600">Readability Score</div>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Tabs defaultValue="keywords" className="w-full">
              <TabsList className="grid w-full grid-cols-4">
                <TabsTrigger value="keywords">Keywords</TabsTrigger>
                <TabsTrigger value="content">Content</TabsTrigger>
                <TabsTrigger value="technical">Technical</TabsTrigger>
                <TabsTrigger value="recommendations">Recommendations</TabsTrigger>
              </TabsList>

              <TabsContent value="keywords" className="space-y-4">
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <TrendingUp className="h-5 w-5" />
                      Keyword Analysis
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="grid gap-4">
                      {seoData.keywords.slice(0, 10).map((keyword, index) => (
                        <div key={index} className="flex items-center justify-between p-4 border rounded-lg">
                          <div className="flex-1">
                            <h3 className="font-semibold">{keyword.keyword}</h3>
                            <div className="flex items-center gap-4 mt-2 text-sm text-gray-600">
                              <span>Volume: {keyword.search_volume.toLocaleString()}</span>
                              <span>Difficulty: {keyword.keyword_difficulty}/100</span>
                              <span>CPC: ${keyword.cpc}</span>
                            </div>
                          </div>
                          <div className="flex items-center gap-2">
                            <Badge className={getCompetitionColor(keyword.competition)}>
                              {keyword.competition}
                            </Badge>
                            <div className="text-right">
                              <div className="text-sm font-medium">{(keyword.relevance_score * 100).toFixed(1)}%</div>
                              <div className="text-xs text-gray-500">Relevance</div>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>

              <TabsContent value="content" className="space-y-4">
                <div className="grid gap-4 md:grid-cols-2">
                  <Card>
                    <CardHeader>
                      <CardTitle>Page Information</CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-4">
                      <div>
                        <h4 className="font-semibold mb-2">Title</h4>
                        <p className="text-sm text-gray-700">{seoData.title}</p>
                      </div>
                      <div>
                        <h4 className="font-semibold mb-2">Meta Description</h4>
                        <p className="text-sm text-gray-700">
                          {seoData.meta_description || "No meta description found"}
                        </p>
                      </div>
                      <div>
                        <h4 className="font-semibold mb-2">Reading Level</h4>
                        <p className="text-sm text-gray-700">{seoData.readability.reading_level}</p>
                      </div>
                    </CardContent>
                  </Card>

                  <Card>
                    <CardHeader>
                      <CardTitle>Heading Structure</CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-4">
                      <div>
                        <h4 className="font-semibold mb-2">H1 Tags ({seoData.headings.h1.length})</h4>
                        {seoData.headings.h1.map((heading, index) => (
                          <p key={index} className="text-sm text-gray-700 mb-1">{heading}</p>
                        ))}
                      </div>
                      <div>
                        <h4 className="font-semibold mb-2">H2 Tags ({seoData.headings.h2.length})</h4>
                        {seoData.headings.h2.slice(0, 5).map((heading, index) => (
                          <p key={index} className="text-sm text-gray-700 mb-1">{heading}</p>
                        ))}
                      </div>
                    </CardContent>
                  </Card>
                </div>
              </TabsContent>

              <TabsContent value="technical" className="space-y-4">
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <Zap className="h-5 w-5" />
                      Technical SEO
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="grid gap-4 md:grid-cols-2">
                      <div className="space-y-4">
                        <div className="flex items-center justify-between">
                          <span>Page Title</span>
                          <CheckCircle className="h-5 w-5 text-green-500" />
                        </div>
                        <div className="flex items-center justify-between">
                          <span>Meta Description</span>
                          {seoData.meta_description ? (
                            <CheckCircle className="h-5 w-5 text-green-500" />
                          ) : (
                            <AlertCircle className="h-5 w-5 text-red-500" />
                          )}
                        </div>
                        <div className="flex items-center justify-between">
                          <span>H1 Tag Present</span>
                          {seoData.headings.h1.length > 0 ? (
                            <CheckCircle className="h-5 w-5 text-green-500" />
                          ) : (
                            <AlertCircle className="h-5 w-5 text-red-500" />
                          )}
                        </div>
                      </div>
                      <div className="space-y-4">
                        <div className="flex items-center justify-between">
                          <span>Content Length</span>
                          {seoData.word_count > 300 ? (
                            <CheckCircle className="h-5 w-5 text-green-500" />
                          ) : (
                            <AlertCircle className="h-5 w-5 text-yellow-500" />
                          )}
                        </div>
                        <div className="flex items-center justify-between">
                          <span>Readability</span>
                          {seoData.readability.readability_score > 60 ? (
                            <CheckCircle className="h-5 w-5 text-green-500" />
                          ) : (
                            <AlertCircle className="h-5 w-5 text-yellow-500" />
                          )}
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>

              <TabsContent value="recommendations" className="space-y-4">
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <Users className="h-5 w-5" />
                      SEO Recommendations
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      {seoData.recommendations.map((rec, index) => (
                        <div key={index} className="p-4 border rounded-lg">
                          <div className="flex items-center justify-between mb-2">
                            <h4 className="font-semibold">{rec.title}</h4>
                            <Badge variant={rec.impact === "high" ? "destructive" : "secondary"}>
                              {rec.impact} impact
                            </Badge>
                          </div>
                          <p className="text-sm text-gray-700">{rec.description}</p>
                          <div className="mt-2">
                            <Badge variant="outline" className="text-xs">
                              {rec.category}
                            </Badge>
                          </div>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>
            </Tabs>
          </div>
        )}
      </div>
    </div>
  );
}