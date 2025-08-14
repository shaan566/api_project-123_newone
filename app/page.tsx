"use client";

import { useMemo, useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { AlertCircle, CheckCircle, Loader2, Search, TrendingUp, Zap } from "lucide-react";

// Match backend AnalyzePayload response
interface AnalyzePayload {
  url: string;
  title?: string | null;
  meta_description?: string | null;
  word_count: number;
  content_metrics: Record<string, number>;
  technical: Record<string, boolean>;
  headings: Record<string, string[]>;
  keywords: Record<string, string[]>; // { gemini: string[], onpage: string[], merged: string[] }
}

const isValidUrl = (value: string) => {
  try {
    const u = new URL(value);
    return !!u.protocol && !!u.host;
  } catch {
    return false;
  }
};

export default function SEOAnalyzer() {
  const [url, setUrl] = useState("");
  const [geminiTopN, setGeminiTopN] = useState<number>(20);
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState<AnalyzePayload | null>(null);
  const [error, setError] = useState<string>("");
  const [copied, setCopied] = useState<boolean>(false);

  const valid = useMemo(() => isValidUrl(url), [url]);

  const analyzeSEO = async () => {
    if (!url || !valid) return;

    setLoading(true);
    setError("");
    setCopied(false);

    try {
      const API_URL = process.env.NEXT_PUBLIC_FASTAPI_URL || "http://localhost:8000";
      const params = new URLSearchParams({ url, gemini_top_n: String(geminiTopN) });
      const response = await fetch(`${API_URL}/analyze?${params.toString()}`);

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        const message = errorData?.detail || errorData?.message || `HTTP error! status: ${response.status}`;
        throw new Error(message);
      }

      const payload: AnalyzePayload = await response.json();
      setData(payload);
    } catch (err) {
      console.error("SEO Analysis Error:", err);
      setData(null);
      setError(err instanceof Error ? err.message : "Failed to analyze website");
    } finally {
      setLoading(false);
    }
  };

  const BoolIndicator = ({ ok }: { ok: boolean }) => (
    ok ? <CheckCircle className="h-5 w-5 text-green-500" /> : <AlertCircle className="h-5 w-5 text-red-500" />
  );

  const headings = data?.headings || {};
  const h1s = headings["h1"] || [];
  const h2s = headings["h2"] || [];

  
  const copyMerged = async () => {
    const merged = data?.keywords?.["merged"] || [];
    if (merged.length === 0) return;
    try {
      await navigator.clipboard.writeText(merged.join("\n"));
      setCopied(true);
      setTimeout(() => setCopied(false), 1500);
    } catch {}
  };

  const downloadCSV = () => {
    const rows: string[] = ["source,keyword"]; // header
    const pushRows = (source: string, words: string[]) => {
      words.forEach((kw) => rows.push(`${source},"${kw.replace(/"/g, '""')}"`));
    };
    pushRows("merged", data?.keywords?.["merged"] || []);
    pushRows("gemini", data?.keywords?.["gemini"] || []);
    pushRows("onpage", data?.keywords?.["onpage"] || []);

    const csv = "\ufeff" + rows.join("\n");
    const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
    const urlBlob = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = urlBlob;
    a.download = "keywords.csv";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(urlBlob);
  };

  const LoadingSkeleton = () => (
    <div className="animate-pulse space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="h-24 rounded-lg bg-gray-200" />
        <div className="h-24 rounded-lg bg-gray-200" />
        <div className="h-24 rounded-lg bg-gray-200" />
      </div>
      <div className="h-64 rounded-lg bg-gray-200" />
      <div className="h-64 rounded-lg bg-gray-200" />
    </div>
  );

  return (
    <div className="min-h-screen bg-gradient-to-b from-white to-gray-50">
      {/* Hero */}
      <div className="relative overflow-hidden">
        <div className="absolute inset-0 -z-10 opacity-30 bg-[radial-gradient(80%_60%_at_50%_-20%,rgba(14,165,233,0.35)_0,rgba(255,255,255,0)_70%)]" />
        <div className="max-w-7xl mx-auto px-6 pt-10 pb-6 text-center">
          <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-emerald-600">
            SEO Research Pro
          </h1>
          <p className="mt-3 text-lg text-gray-600">
            Analyze on-page content, technical health, and get AI-suggested keywords.
          </p>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-6 pb-12">
        {/* Search Panel */}
        <Card className="mb-8 shadow-sm border border-gray-200">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Search className="h-5 w-5 text-blue-600" />
              Website Analysis
            </CardTitle>
            <CardDescription>
              Enter a URL, adjust AI keyword suggestions, and start analyzing.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid gap-3 md:grid-cols-[1fr_auto_auto]">
              <div className="flex items-center gap-3">
                <Input
                  placeholder="https://your-website.com"
                  value={url}
                  onChange={(e) => setUrl(e.target.value)}
                  className="flex-1"
                  type="url"
                />
              </div>
              <div className="flex items-center gap-2">
                <label htmlFor="topn" className="text-sm text-gray-600 whitespace-nowrap">AI keywords</label>
                <Input
                  id="topn"
                  type="number"
                  min={5}
                  max={100}
                  value={geminiTopN}
                  onChange={(e) => setGeminiTopN(Number(e.target.value || 0))}
                  className="w-24"
                />
              </div>
              <Button onClick={analyzeSEO} disabled={!valid || loading} className="justify-center">
                {loading ? (
                  <span className="inline-flex items-center gap-2">
                    <Loader2 className="h-4 w-4 animate-spin" /> Analyzing
                  </span>
                ) : (
                  "Analyze SEO"
                )}
              </Button>
            </div>

            {!valid && url.length > 0 && (
              <div className="text-sm text-red-600 flex items-center gap-2">
                <AlertCircle className="h-4 w-4" /> Enter a valid URL including https://
              </div>
            )}

            
            {error && (
              <div className="mt-2 p-3 bg-red-50 border border-red-200 rounded-lg flex items-center gap-2 justify-between">
                <div className="flex items-center gap-2">
                  <AlertCircle className="h-5 w-5 text-red-500" />
                  <span className="text-red-700 text-sm">{error}</span>
                </div>
                <button onClick={() => setError("") } className="text-sm text-red-600 hover:underline">Dismiss</button>
              </div>
            )}
          </CardContent>
        </Card>

        {loading && <LoadingSkeleton />}

        {data && !loading && (
          <div className="space-y-8">
            {/* Summary */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <Card className="shadow-sm">
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm text-gray-600">Words</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-3xl font-bold text-blue-600">{data.word_count}</div>
                  <p className="text-xs text-gray-500 mt-1">Total content word count</p>
                </CardContent>
              </Card>
              <Card className="shadow-sm">
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm text-gray-600">H1 Tags</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-3xl font-bold text-purple-600">{h1s.length}</div>
                  <p className="text-xs text-gray-500 mt-1">Main headings on page</p>
                </CardContent>
              </Card>
              <Card className="shadow-sm">
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm text-gray-600">H2 Tags</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-3xl font-bold text-emerald-600">{h2s.length}</div>
                  <p className="text-xs text-gray-500 mt-1">Section headings on page</p>
                </CardContent>
              </Card>
            </div>

            <Tabs defaultValue="keywords" className="w-full">
              <TabsList className="grid w-full grid-cols-3">
                <TabsTrigger value="keywords">Keywords</TabsTrigger>
                <TabsTrigger value="content">Content</TabsTrigger>
                <TabsTrigger value="technical">Technical</TabsTrigger>
              </TabsList>

              <TabsContent value="keywords" className="space-y-4">
                <Card className="shadow-sm">
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <TrendingUp className="h-5 w-5" />
                      Keyword Suggestions
                    </CardTitle>
                    <CardDescription>Combined signals from page content and AI suggestions</CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-6">
                    <div className="flex flex-wrap gap-2">
                      <Button variant="secondary" onClick={copyMerged} className="h-8">
                        {copied ? "Copied" : "Copy merged"}
                      </Button>
                      <Button variant="outline" onClick={downloadCSV} className="h-8">
                        Export CSV
                      </Button>
                    </div>

                    <div>
                      <h4 className="font-semibold mb-2">Merged ({data.keywords?.["merged"]?.length || 0})</h4>
                      <div className="flex flex-wrap gap-2">
                        {(data.keywords?.["merged"] || []).map((kw, i) => (
                          <Badge key={`merged-${i}`} className="bg-blue-50 text-blue-800 border border-blue-200">{kw}</Badge>
                        ))}
                        {(data.keywords?.["merged"] || []).length === 0 && (
                          <p className="text-sm text-gray-500">No suggestions</p>
                        )}
                      </div>
                    </div>
                    <div>
                      <h4 className="font-semibold mb-2">AI (Gemini) ({data.keywords?.["gemini"]?.length || 0})</h4>
                      <div className="flex flex-wrap gap-2">
                        {(data.keywords?.["gemini"] || []).map((kw, i) => (
                          <Badge key={`gem-${i}`} variant="outline">{kw}</Badge>
                        ))}
                        {(data.keywords?.["gemini"] || []).length === 0 && (
                          <p className="text-sm text-gray-500">No AI keywords available</p>
                        )}
                      </div>
                    </div>
                    <div>
                      <h4 className="font-semibold mb-2">On-page Phrases ({data.keywords?.["onpage"]?.length || 0})</h4>
                      <div className="flex flex-wrap gap-2">
                        {(data.keywords?.["onpage"] || []).map((kw, i) => (
                          <Badge key={`on-${i}`}>{kw}</Badge>
                        ))}
                        {(data.keywords?.["onpage"] || []).length === 0 && (
                          <p className="text-sm text-gray-500">No on-page phrases found</p>
                        )}
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>

              <TabsContent value="content" className="space-y-4">
                <div className="grid gap-4 md:grid-cols-2">
                  <Card className="shadow-sm">
                    <CardHeader>
                      <CardTitle>Page Information</CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-4">
                      <div>
                        <h4 className="font-semibold mb-2">Title</h4>
                        <p className="text-sm text-gray-700">{data.title || "No title detected"}</p>
                      </div>
                      <div>
                        <h4 className="font-semibold mb-2">Meta Description</h4>
                        <p className="text-sm text-gray-700">{data.meta_description || "No meta description found"}</p>
                      </div>
                    </CardContent>
                  </Card>

                  <Card className="shadow-sm">
                    <CardHeader>
                      <CardTitle>Heading Structure</CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-4">
                      <div>
                        <h4 className="font-semibold mb-2">H1 Tags ({h1s.length})</h4>
                        {h1s.map((heading, index) => (
                          <p key={index} className="text-sm text-gray-700 mb-1">{heading}</p>
                        ))}
                        {h1s.length === 0 && <p className="text-sm text-gray-500">No H1 tags found</p>}
                      </div>
                      <div>
                        <h4 className="font-semibold mb-2">H2 Tags ({h2s.length})</h4>
                        {h2s.slice(0, 10).map((heading, index) => (
                          <p key={index} className="text-sm text-gray-700 mb-1">{heading}</p>
                        ))}
                        {h2s.length === 0 && <p className="text-sm text-gray-500">No H2 tags found</p>}
                      </div>
                    </CardContent>
                  </Card>
                </div>
              </TabsContent>

              <TabsContent value="technical" className="space-y-4">
                <Card className="shadow-sm">
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <Zap className="h-5 w-5" />
                      Technical SEO
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="grid gap-4 md:grid-cols-2">
                      <div className="space-y-4">
                        <div className="flex items-center justify-between p-3 rounded-lg border bg-white">
                          <span>Meta Description Present</span>
                          <BoolIndicator ok={!!data.meta_description || !!data.technical?.has_meta_description} />
                        </div>
                        <div className="flex items-center justify-between p-3 rounded-lg border bg-white">
                          <span>H1 Tag Present</span>
                          <BoolIndicator ok={h1s.length > 0} />
                        </div>
                      </div>
                      <div className="space-y-4">
                        <div className="flex items-center justify-between p-3 rounded-lg border bg-white">
                          <span>Canonical Tag</span>
                          <BoolIndicator ok={!!data.technical?.has_canonical} />
                        </div>
                        <div className="flex items-center justify-between p-3 rounded-lg border bg-white">
                          <span>Open Graph Tags</span>
                          <BoolIndicator ok={!!data.technical?.has_og} />
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>
            </Tabs>
          </div>
        )}

        {!data && !loading && (
          <div className="text-center text-sm text-gray-500 pt-6">
            Enter a URL above and click Analyze to get started.
          </div>
        )}
      </div>
    </div>
  );
}
