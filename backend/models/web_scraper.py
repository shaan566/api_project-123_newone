
import asyncio
from typing import Dict, List
from urllib.parse import urljoin, urlparse

import aiohttp
from bs4 import BeautifulSoup

class WebScraper:
    def __init__(self, timeout: int = 30):
        self.timeout = timeout
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.7",
        }

    async def fetch_html(self, url: str) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers, timeout=self.timeout) as resp:
                resp.raise_for_status()
                return await resp.text(errors="ignore")

    async def scrape(self, url: str) -> Dict:
        html = await self.fetch_html(url)
        soup = BeautifulSoup(html, "html.parser")

        meta = self._meta(soup)
        headings = self._headings(soup)
        links = self._links(soup, url)
        images = self._images(soup, url)
        onpage_keywords = self._keywords_from_page(soup)

        content_text = soup.get_text("\n", strip=True)
        word_count = len(content_text.split())

        return {
            "url": url,
            "title": meta.get("title",""),
            "meta_description": meta.get("description",""),
            "word_count": word_count,
            "meta": meta,
            "headings": headings,
            "links": links,
            "images": images,
            "onpage_keywords": onpage_keywords,
            "content_text": content_text[:200000]  # cap to avoid huge payloads
        }

    def _meta(self, soup: BeautifulSoup) -> Dict[str, str]:
        m = {}
        t = soup.find("title")
        if t:
            m["title"] = t.get_text(strip=True)
        for tag in soup.find_all("meta"):
            name = (tag.get("name") or "").lower()
            prop = (tag.get("property") or "").lower()
            content = tag.get("content") or ""
            if name == "description":
                m["description"] = content
            elif name == "keywords":
                m["keywords"] = content
            elif prop == "og:title":
                m["og_title"] = content
            elif prop == "og:description":
                m["og_description"] = content
        link_canonical = soup.find("link", rel="canonical")
        if link_canonical and link_canonical.get("href"):
            m["canonical"] = link_canonical.get("href")
        return m

    def _headings(self, soup: BeautifulSoup) -> Dict[str, List[str]]:
        out = {f"h{i}": [] for i in range(1,7)}
        for i in range(1,7):
            seen = set()
            for tag in soup.find_all(f"h{i}"):
                txt = tag.get_text(" ", strip=True)
                if txt and txt not in seen:
                    seen.add(txt)
                    out[f"h{i}"].append(txt)
        return out

    def _links(self, soup: BeautifulSoup, base_url: str) -> Dict[str, List[Dict]]:
        base_domain = urlparse(base_url).netloc
        internal, external = [], []
        seen_int, seen_ext = set(), set()

        for a in soup.find_all("a", href=True):
            href = a["href"]
            abs_url = urljoin(base_url, href)
            domain = urlparse(abs_url).netloc
            item = {"url": abs_url, "text": a.get_text(" ", strip=True), "title": a.get("title","")}
            if domain == base_domain:
                if abs_url not in seen_int:
                    seen_int.add(abs_url); internal.append(item)
            else:
                if abs_url not in seen_ext:
                    seen_ext.add(abs_url); external.append(item)
        return {"internal": internal, "external": external}

    def _images(self, soup: BeautifulSoup, base_url: str) -> List[Dict]:
        imgs, seen = [], set()
        for img in soup.find_all("img"):
            src = img.get("src")
            if not src: 
                continue
            abs_url = urljoin(base_url, src)
            if abs_url in seen: 
                continue
            seen.add(abs_url)
            imgs.append({
                "url": abs_url,
                "alt": img.get("alt",""),
                "title": img.get("title","")
            })
        return imgs

    def _keywords_from_page(self, soup: BeautifulSoup) -> List[str]:
        # Collect short phrases from headings, bold/strong, and list items
        phrases = []
        for tag in soup.find_all(["h1","h2","h3","strong","b","li"]):
            txt = tag.get_text(" ", strip=True)
            if txt and 3 <= len(txt) <= 60 and len(txt.split()) <= 8:
                phrases.append(txt)
        # Also parse meta keywords
        mk = soup.find("meta", attrs={"name":"keywords"})
        if mk and mk.get("content"):
            phrases.extend([p.strip() for p in mk["content"].split(",") if p.strip()])
        return phrases
