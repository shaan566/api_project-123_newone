import asyncio
import logging
import re
import time
from typing import Dict, Optional, List
from urllib.parse import urljoin, urlparse
import aiohttp
import requests
from bs4 import BeautifulSoup
import trafilatura
from fake_useragent import UserAgent

logger = logging.getLogger(__name__)

class WebScraper:
    def __init__(self):
        self.ua = UserAgent()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': self.ua.random
        })
        
    def _get_headers(self) -> Dict[str, str]:
        """Get randomized headers for requests"""
        return {
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Referer': 'https://www.google.com/',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
    
    async def scrape_url(self, url: str, timeout: int = 30) -> Dict:
        """Scrape a URL and extract all relevant SEO data"""
        try:
            logger.info(f"Scraping URL: {url}")
            
            # Use trafilatura for content extraction
            downloaded = trafilatura.fetch_url(url, config=trafilatura.settings.use_config())
            if not downloaded:
                raise Exception("Failed to download page content")
            
            # Extract main content
            text_content = trafilatura.extract(downloaded, include_comments=False, include_tables=True)
            if not text_content:
                raise Exception("Failed to extract text content")
            
            # Parse HTML with BeautifulSoup for detailed analysis
            soup = BeautifulSoup(downloaded, 'html.parser')
            
            # Extract metadata
            meta_data = self._extract_metadata(soup)
            
            # Extract headings structure
            headings = self._extract_headings(soup)
            
            # Extract links
            links = self._extract_links(soup, url)
            
            # Extract images
            images = self._extract_images(soup, url)
            
            # Extract structured data
            structured_data = self._extract_structured_data(soup)
            
            result = {
                'url': url,
                'title': meta_data.get('title', ''),
                'meta_description': meta_data.get('description', ''),
                'meta_keywords': meta_data.get('keywords', ''),
                'content': text_content,
                'raw_html': str(soup),
                'headings': headings,
                'meta_data': meta_data,
                'links': links,
                'images': images,
                'structured_data': structured_data,
                'word_count': len(text_content.split()) if text_content else 0,
                'scraped_at': time.time()
            }
            
            logger.info(f"Successfully scraped {url} - {result['word_count']} words extracted")
            return result
            
        except Exception as e:
            logger.error(f"Error scraping {url}: {str(e)}")
            raise Exception(f"Failed to scrape URL: {str(e)}")
    
    def _extract_metadata(self, soup: BeautifulSoup) -> Dict:
        """Extract all metadata from the page"""
        meta_data = {}
        
        # Title
        title_tag = soup.find('title')
        meta_data['title'] = title_tag.get_text().strip() if title_tag else ''
        
        # Meta tags
        meta_tags = soup.find_all('meta')
        for tag in meta_tags:
            name = tag.get('name', '').lower()
            property_attr = tag.get('property', '').lower()
            content = tag.get('content', '')
            
            if name == 'description':
                meta_data['description'] = content
            elif name == 'keywords':
                meta_data['keywords'] = content
            elif name == 'robots':
                meta_data['robots'] = content
            elif name == 'author':
                meta_data['author'] = content
            elif property_attr == 'og:title':
                meta_data['og_title'] = content
            elif property_attr == 'og:description':
                meta_data['og_description'] = content
            elif property_attr == 'og:image':
                meta_data['og_image'] = content
            elif property_attr == 'og:url':
                meta_data['og_url'] = content
            elif name == 'twitter:title':
                meta_data['twitter_title'] = content
            elif name == 'twitter:description':
                meta_data['twitter_description'] = content
            elif name == 'twitter:image':
                meta_data['twitter_image'] = content
        
        # Canonical URL
        canonical = soup.find('link', rel='canonical')
        if canonical:
            meta_data['canonical'] = canonical.get('href', '')
        
        return meta_data
    
    def _extract_headings(self, soup: BeautifulSoup) -> Dict:
        """Extract heading structure from the page"""
        headings = {'h1': [], 'h2': [], 'h3': [], 'h4': [], 'h5': [], 'h6': []}
        
        for level in range(1, 7):
            heading_tags = soup.find_all(f'h{level}')
            for tag in heading_tags:
                text = tag.get_text().strip()
                if text:
                    headings[f'h{level}'].append(text)
        
        return headings
    
    def _extract_links(self, soup: BeautifulSoup, base_url: str) -> Dict:
        """Extract all links from the page"""
        links = {'internal': [], 'external': []}
        base_domain = urlparse(base_url).netloc
        
        link_tags = soup.find_all('a', href=True)
        for tag in link_tags:
            href = tag.get('href')
            text = tag.get_text().strip()
            
            # Convert relative URLs to absolute
            absolute_url = urljoin(base_url, href)
            link_domain = urlparse(absolute_url).netloc
            
            link_data = {
                'url': absolute_url,
                'text': text,
                'title': tag.get('title', ''),
                'rel': tag.get('rel', [])
            }
            
            if link_domain == base_domain:
                links['internal'].append(link_data)
            else:
                links['external'].append(link_data)
        
        return links
    
    def _extract_images(self, soup: BeautifulSoup, base_url: str) -> List[Dict]:
        """Extract all images from the page"""
        images = []
        img_tags = soup.find_all('img')
        
        for tag in img_tags:
            src = tag.get('src')
            if src:
                absolute_url = urljoin(base_url, src)
                images.append({
                    'url': absolute_url,
                    'alt': tag.get('alt', ''),
                    'title': tag.get('title', ''),
                    'width': tag.get('width'),
                    'height': tag.get('height')
                })
        
        return images
    
    def _extract_structured_data(self, soup: BeautifulSoup) -> List[Dict]:
        """Extract structured data (JSON-LD, microdata, etc.)"""
        structured_data = []
        
        # JSON-LD
        json_ld_scripts = soup.find_all('script', type='application/ld+json')
        for script in json_ld_scripts:
            try:
                import json
                data = json.loads(script.string)
                structured_data.append({
                    'type': 'json-ld',
                    'data': data
                })
            except:
                pass
        
        # Microdata
        microdata_items = soup.find_all(attrs={'itemtype': True})
        for item in microdata_items:
            structured_data.append({
                'type': 'microdata',
                'itemtype': item.get('itemtype'),
                'properties': self._extract_microdata_properties(item)
            })
        
        return structured_data
    
    def _extract_microdata_properties(self, item) -> Dict:
        """Extract microdata properties from an item"""
        properties = {}
        prop_elements = item.find_all(attrs={'itemprop': True})
        
        for element in prop_elements:
            prop_name = element.get('itemprop')
            if element.name == 'meta':
                prop_value = element.get('content', '')
            else:
                prop_value = element.get_text().strip()
            properties[prop_name] = prop_value
        
        return properties
    
    async def get_page_speed_metrics(self, url: str) -> Dict:
        """Get basic page speed metrics"""
        try:
            start_time = time.time()
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=self._get_headers()) as response:
                    load_time = time.time() - start_time
                    
                    return {
                        'load_time': load_time,
                        'status_code': response.status,
                        'content_size': len(await response.read()),
                        'response_headers': dict(response.headers)
                    }
        except Exception as e:
            logger.error(f"Error getting page speed metrics for {url}: {str(e)}")
            return {}
