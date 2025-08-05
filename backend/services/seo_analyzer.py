import logging
import re
import math
from typing import Dict, List, Optional
import textstat
from collections import Counter

logger = logging.getLogger(__name__)

class SEOAnalyzer:
    def __init__(self):
        self.optimal_title_length = (30, 60)
        self.optimal_description_length = (120, 160)
        self.optimal_keyword_density = (0.5, 3.0)
        
    async def analyze_page(self, scraped_data: Dict, url: str, target_keyword: Optional[str] = None) -> Dict:
        """Perform comprehensive SEO analysis of a page"""
        try:
            content = scraped_data.get('content', '')
            title = scraped_data.get('title', '')
            meta_description = scraped_data.get('meta_description', '')
            headings = scraped_data.get('headings', {})
            
            # Analyze different aspects
            meta_analysis = self._analyze_metadata(title, meta_description, url)
            content_analysis = self._analyze_content(content, headings)
            keyword_analysis = self._analyze_keywords(content, title, meta_description, headings, target_keyword)
            readability_analysis = self._analyze_readability(content)
            technical_analysis = self._analyze_technical_aspects(scraped_data)
            
            # Calculate overall SEO score
            seo_score = self._calculate_seo_score(
                meta_analysis, content_analysis, keyword_analysis, 
                readability_analysis, technical_analysis
            )
            
            # Generate recommendations
            recommendations = self._generate_recommendations(
                meta_analysis, content_analysis, keyword_analysis,
                readability_analysis, technical_analysis
            )
            
            return {
                'seo_score': seo_score,
                'meta_analysis': meta_analysis,
                'content_analysis': content_analysis,
                'keyword_analysis': keyword_analysis,
                'readability': readability_analysis,
                'technical_analysis': technical_analysis,
                'recommendations': recommendations
            }
            
        except Exception as e:
            logger.error(f"Error in SEO analysis: {str(e)}")
            raise Exception(f"SEO analysis failed: {str(e)}")
    
    def _analyze_metadata(self, title: str, meta_description: str, url: str) -> Dict:
        """Analyze page metadata"""
        analysis = {
            'title': {
                'text': title,
                'length': len(title),
                'optimal_length': self.optimal_title_length,
                'is_optimal': self.optimal_title_length[0] <= len(title) <= self.optimal_title_length[1],
                'score': 0
            },
            'meta_description': {
                'text': meta_description,
                'length': len(meta_description),
                'optimal_length': self.optimal_description_length,
                'is_optimal': self.optimal_description_length[0] <= len(meta_description) <= self.optimal_description_length[1],
                'score': 0
            },
            'url_analysis': self._analyze_url(url)
        }
        
        # Score title
        if analysis['title']['is_optimal']:
            analysis['title']['score'] = 100
        elif len(title) == 0:
            analysis['title']['score'] = 0
        elif len(title) < self.optimal_title_length[0]:
            analysis['title']['score'] = 60
        else:
            analysis['title']['score'] = 80
        
        # Score meta description
        if analysis['meta_description']['is_optimal']:
            analysis['meta_description']['score'] = 100
        elif len(meta_description) == 0:
            analysis['meta_description']['score'] = 0
        elif len(meta_description) < self.optimal_description_length[0]:
            analysis['meta_description']['score'] = 60
        else:
            analysis['meta_description']['score'] = 80
        
        return analysis
    
    def _analyze_url(self, url: str) -> Dict:
        """Analyze URL structure"""
        # Remove protocol and www
        clean_url = re.sub(r'^https?://(www\.)?', '', url)
        
        return {
            'length': len(clean_url),
            'has_hyphens': '-' in clean_url,
            'has_underscores': '_' in clean_url,
            'depth': clean_url.count('/'),
            'has_parameters': '?' in clean_url,
            'is_readable': not bool(re.search(r'[0-9]{3,}|[^a-zA-Z0-9\-/._]', clean_url))
        }
    
    def _analyze_content(self, content: str, headings: Dict) -> Dict:
        """Analyze page content structure and quality"""
        if not content:
            return {
                'word_count': 0,
                'paragraph_count': 0,
                'sentences_count': 0,
                'headings_analysis': {'total': 0, 'structure_score': 0},
                'content_score': 0
            }
        
        # Basic content metrics
        words = content.split()
        sentences = re.split(r'[.!?]+', content)
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
        
        # Analyze heading structure
        headings_analysis = self._analyze_heading_structure(headings)
        
        # Calculate content score
        content_score = self._calculate_content_score(len(words), len(sentences), len(paragraphs), headings_analysis)
        
        return {
            'word_count': len(words),
            'paragraph_count': len(paragraphs),
            'sentences_count': len([s for s in sentences if s.strip()]),
            'average_words_per_sentence': len(words) / max(len(sentences), 1),
            'average_sentences_per_paragraph': len(sentences) / max(len(paragraphs), 1),
            'headings_analysis': headings_analysis,
            'content_score': content_score
        }
    
    def _analyze_heading_structure(self, headings: Dict) -> Dict:
        """Analyze the heading structure of the page"""
        total_headings = sum(len(headings.get(f'h{i}', [])) for i in range(1, 7))
        
        h1_count = len(headings.get('h1', []))
        h2_count = len(headings.get('h2', []))
        
        # Calculate structure score
        structure_score = 100
        if h1_count == 0:
            structure_score -= 30
        elif h1_count > 1:
            structure_score -= 20
        
        if h2_count == 0 and total_headings > 1:
            structure_score -= 15
        
        return {
            'total': total_headings,
            'h1_count': h1_count,
            'h2_count': h2_count,
            'h3_count': len(headings.get('h3', [])),
            'h4_count': len(headings.get('h4', [])),
            'h5_count': len(headings.get('h5', [])),
            'h6_count': len(headings.get('h6', [])),
            'structure_score': max(0, structure_score),
            'has_proper_h1': h1_count == 1,
            'has_h2': h2_count > 0
        }
    
    def _calculate_content_score(self, word_count: int, sentence_count: int, paragraph_count: int, headings_analysis: Dict) -> int:
        """Calculate overall content quality score"""
        score = 0
        
        # Word count scoring
        if word_count >= 300:
            score += 30
        elif word_count >= 150:
            score += 20
        else:
            score += 10
        
        # Paragraph structure
        if paragraph_count >= 3:
            score += 20
        elif paragraph_count >= 1:
            score += 15
        
        # Heading structure
        score += (headings_analysis['structure_score'] * 0.3)
        
        # Sentence structure
        if sentence_count > 0:
            avg_words_per_sentence = word_count / sentence_count
            if 10 <= avg_words_per_sentence <= 20:
                score += 20
            else:
                score += 10
        
        return min(100, int(score))
    
    def _analyze_keywords(self, content: str, title: str, meta_description: str, headings: Dict, target_keyword: Optional[str]) -> Dict:
        """Analyze keyword usage and density"""
        if not target_keyword:
            # Extract potential keywords from content
            words = re.findall(r'\b[a-zA-Z]{3,}\b', content.lower())
            word_freq = Counter(words)
            most_common = word_freq.most_common(5)
            target_keyword = most_common[0][0] if most_common else "content"
        
        target_keyword = target_keyword.lower()
        content_lower = content.lower()
        title_lower = title.lower()
        meta_desc_lower = meta_description.lower()
        
        # Count keyword occurrences
        content_occurrences = content_lower.count(target_keyword)
        title_occurrences = title_lower.count(target_keyword)
        meta_desc_occurrences = meta_desc_lower.count(target_keyword)
        
        # Check headings
        h1_has_keyword = any(target_keyword in h1.lower() for h1 in headings.get('h1', []))
        h2_has_keyword = any(target_keyword in h2.lower() for h2 in headings.get('h2', []))
        
        # Calculate keyword density
        total_words = len(content.split()) if content else 1
        keyword_density = (content_occurrences / total_words) * 100
        
        # Score keyword usage
        keyword_score = self._calculate_keyword_score(
            content_occurrences, title_occurrences, meta_desc_occurrences,
            h1_has_keyword, h2_has_keyword, keyword_density
        )
        
        return {
            'target_keyword': target_keyword,
            'content_occurrences': content_occurrences,
            'title_occurrences': title_occurrences,
            'meta_description_occurrences': meta_desc_occurrences,
            'h1_has_keyword': h1_has_keyword,
            'h2_has_keyword': h2_has_keyword,
            'keyword_density': round(keyword_density, 2),
            'optimal_density_range': self.optimal_keyword_density,
            'is_optimal_density': self.optimal_keyword_density[0] <= keyword_density <= self.optimal_keyword_density[1],
            'keyword_score': keyword_score
        }
    
    def _calculate_keyword_score(self, content_occ: int, title_occ: int, meta_occ: int, 
                               h1_has: bool, h2_has: bool, density: float) -> int:
        """Calculate keyword optimization score"""
        score = 0
        
        # Title keyword presence
        if title_occ > 0:
            score += 25
        
        # Meta description keyword presence
        if meta_occ > 0:
            score += 15
        
        # H1 keyword presence
        if h1_has:
            score += 20
        
        # H2 keyword presence
        if h2_has:
            score += 10
        
        # Keyword density optimization
        if self.optimal_keyword_density[0] <= density <= self.optimal_keyword_density[1]:
            score += 30
        elif density > 0:
            score += 15
        
        return min(100, score)
    
    def _analyze_readability(self, content: str) -> Dict:
        """Analyze content readability"""
        if not content or len(content.strip()) < 100:
            return {
                'flesch_reading_ease': 0,
                'flesch_kincaid_grade': 0,
                'gunning_fog': 0,
                'automated_readability_index': 0,
                'readability_score': 0,
                'reading_level': 'Unknown'
            }
        
        try:
            flesch_ease = textstat.flesch_reading_ease(content)
            flesch_grade = textstat.flesch_kincaid_grade(content)
            gunning_fog = textstat.gunning_fog(content)
            ari = textstat.automated_readability_index(content)
            
            # Determine reading level
            if flesch_ease >= 90:
                reading_level = "Very Easy"
            elif flesch_ease >= 80:
                reading_level = "Easy"
            elif flesch_ease >= 70:
                reading_level = "Fairly Easy"
            elif flesch_ease >= 60:
                reading_level = "Standard"
            elif flesch_ease >= 50:
                reading_level = "Fairly Difficult"
            elif flesch_ease >= 30:
                reading_level = "Difficult"
            else:
                reading_level = "Very Difficult"
            
            # Calculate readability score (0-100)
            readability_score = max(0, min(100, flesch_ease))
            
            return {
                'flesch_reading_ease': round(flesch_ease, 1),
                'flesch_kincaid_grade': round(flesch_grade, 1),
                'gunning_fog': round(gunning_fog, 1),
                'automated_readability_index': round(ari, 1),
                'readability_score': int(readability_score),
                'reading_level': reading_level
            }
            
        except Exception as e:
            logger.error(f"Error calculating readability: {str(e)}")
            return {
                'flesch_reading_ease': 0,
                'flesch_kincaid_grade': 0,
                'gunning_fog': 0,
                'automated_readability_index': 0,
                'readability_score': 50,
                'reading_level': 'Standard'
            }
    
    def _analyze_technical_aspects(self, scraped_data: Dict) -> Dict:
        """Analyze technical SEO aspects"""
        meta_data = scraped_data.get('meta_data', {})
        images = scraped_data.get('images', [])
        links = scraped_data.get('links', {})
        
        # Check for essential meta tags
        has_meta_description = bool(meta_data.get('description'))
        has_canonical = bool(meta_data.get('canonical'))
        has_og_tags = any(key.startswith('og_') for key in meta_data.keys())
        has_twitter_tags = any(key.startswith('twitter_') for key in meta_data.keys())
        
        # Analyze images
        images_without_alt = sum(1 for img in images if not img.get('alt'))
        
        # Analyze internal/external links
        internal_links = len(links.get('internal', []))
        external_links = len(links.get('external', []))
        
        technical_score = self._calculate_technical_score(
            has_meta_description, has_canonical, has_og_tags, has_twitter_tags,
            len(images), images_without_alt, internal_links, external_links
        )
        
        return {
            'has_meta_description': has_meta_description,
            'has_canonical_url': has_canonical,
            'has_open_graph': has_og_tags,
            'has_twitter_cards': has_twitter_tags,
            'total_images': len(images),
            'images_without_alt': images_without_alt,
            'internal_links': internal_links,
            'external_links': external_links,
            'technical_score': technical_score
        }
    
    def _calculate_technical_score(self, has_meta_desc: bool, has_canonical: bool,
                                 has_og: bool, has_twitter: bool, total_images: int,
                                 images_without_alt: int, internal_links: int,
                                 external_links: int) -> int:
        """Calculate technical SEO score"""
        score = 0
        
        if has_meta_desc:
            score += 20
        if has_canonical:
            score += 15
        if has_og:
            score += 15
        if has_twitter:
            score += 10
        
        # Image optimization
        if total_images > 0:
            alt_ratio = (total_images - images_without_alt) / total_images
            score += int(alt_ratio * 20)
        else:
            score += 10  # No images is fine
        
        # Link structure
        if internal_links > 0:
            score += 10
        if external_links > 0:
            score += 5
        
        # Bonus for good link ratio
        total_links = internal_links + external_links
        if total_links > 0 and internal_links / total_links >= 0.7:
            score += 5
        
        return min(100, score)
    
    def _calculate_seo_score(self, meta_analysis: Dict, content_analysis: Dict,
                           keyword_analysis: Dict, readability_analysis: Dict,
                           technical_analysis: Dict) -> int:
        """Calculate overall SEO score weighted by importance"""
        weights = {
            'meta': 0.25,      # 25% - Title, meta description
            'content': 0.25,   # 25% - Content quality and structure
            'keywords': 0.20,  # 20% - Keyword optimization
            'technical': 0.20, # 20% - Technical SEO
            'readability': 0.10 # 10% - Readability
        }
        
        # Get individual scores
        meta_score = (meta_analysis['title']['score'] + meta_analysis['meta_description']['score']) / 2
        content_score = content_analysis['content_score']
        keyword_score = keyword_analysis['keyword_score']
        technical_score = technical_analysis['technical_score']
        readability_score = readability_analysis['readability_score']
        
        # Calculate weighted average
        total_score = (
            meta_score * weights['meta'] +
            content_score * weights['content'] +
            keyword_score * weights['keywords'] +
            technical_score * weights['technical'] +
            readability_score * weights['readability']
        )
        
        return int(total_score)
    
    def _generate_recommendations(self, meta_analysis: Dict, content_analysis: Dict,
                                keyword_analysis: Dict, readability_analysis: Dict,
                                technical_analysis: Dict) -> List[Dict]:
        """Generate actionable SEO recommendations"""
        recommendations = []
        
        # Title recommendations
        if meta_analysis['title']['score'] < 80:
            if len(meta_analysis['title']['text']) == 0:
                recommendations.append({
                    'type': 'critical',
                    'category': 'metadata',
                    'title': 'Missing Page Title',
                    'description': 'Add a descriptive title tag to your page',
                    'impact': 'high'
                })
            elif not meta_analysis['title']['is_optimal']:
                recommendations.append({
                    'type': 'warning',
                    'category': 'metadata',
                    'title': 'Optimize Title Length',
                    'description': f'Title should be between {self.optimal_title_length[0]}-{self.optimal_title_length[1]} characters. Current: {meta_analysis["title"]["length"]}',
                    'impact': 'medium'
                })
        
        # Meta description recommendations
        if meta_analysis['meta_description']['score'] < 80:
            if len(meta_analysis['meta_description']['text']) == 0:
                recommendations.append({
                    'type': 'warning',
                    'category': 'metadata',
                    'title': 'Missing Meta Description',
                    'description': 'Add a compelling meta description to improve click-through rates',
                    'impact': 'medium'
                })
            elif not meta_analysis['meta_description']['is_optimal']:
                recommendations.append({
                    'type': 'info',
                    'category': 'metadata',
                    'title': 'Optimize Meta Description Length',
                    'description': f'Meta description should be between {self.optimal_description_length[0]}-{self.optimal_description_length[1]} characters. Current: {meta_analysis["meta_description"]["length"]}',
                    'impact': 'low'
                })
        
        # Content recommendations
        if content_analysis['word_count'] < 300:
            recommendations.append({
                'type': 'warning',
                'category': 'content',
                'title': 'Increase Content Length',
                'description': f'Consider adding more content. Current word count: {content_analysis["word_count"]}. Aim for at least 300 words.',
                'impact': 'medium'
            })
        
        if not content_analysis['headings_analysis']['has_proper_h1']:
            recommendations.append({
                'type': 'critical',
                'category': 'content',
                'title': 'Add H1 Heading',
                'description': 'Every page should have exactly one H1 heading that describes the main topic',
                'impact': 'high'
            })
        
        # Keyword recommendations
        if keyword_analysis['keyword_score'] < 60:
            if not keyword_analysis['title_occurrences']:
                recommendations.append({
                    'type': 'warning',
                    'category': 'keywords',
                    'title': 'Include Keyword in Title',
                    'description': f'Include your target keyword "{keyword_analysis["target_keyword"]}" in the page title',
                    'impact': 'high'
                })
            
            if not keyword_analysis['h1_has_keyword']:
                recommendations.append({
                    'type': 'warning',
                    'category': 'keywords',
                    'title': 'Include Keyword in H1',
                    'description': f'Include your target keyword "{keyword_analysis["target_keyword"]}" in the H1 heading',
                    'impact': 'medium'
                })
            
            if not keyword_analysis['is_optimal_density']:
                if keyword_analysis['keyword_density'] < self.optimal_keyword_density[0]:
                    recommendations.append({
                        'type': 'info',
                        'category': 'keywords',
                        'title': 'Increase Keyword Density',
                        'description': f'Current keyword density is {keyword_analysis["keyword_density"]}%. Consider increasing usage to {self.optimal_keyword_density[0]}-{self.optimal_keyword_density[1]}%',
                        'impact': 'low'
                    })
                else:
                    recommendations.append({
                        'type': 'warning',
                        'category': 'keywords',
                        'title': 'Reduce Keyword Density',
                        'description': f'Keyword density of {keyword_analysis["keyword_density"]}% may be too high. Consider reducing to {self.optimal_keyword_density[0]}-{self.optimal_keyword_density[1]}%',
                        'impact': 'medium'
                    })
        
        # Readability recommendations
        if readability_analysis['readability_score'] < 60:
            recommendations.append({
                'type': 'info',
                'category': 'readability',
                'title': 'Improve Readability',
                'description': f'Content readability is {readability_analysis["reading_level"]}. Consider using simpler language and shorter sentences.',
                'impact': 'low'
            })
        
        # Technical recommendations
        if technical_analysis['images_without_alt'] > 0:
            recommendations.append({
                'type': 'warning',
                'category': 'technical',
                'title': 'Add Alt Text to Images',
                'description': f'{technical_analysis["images_without_alt"]} images are missing alt text. Add descriptive alt attributes for accessibility and SEO.',
                'impact': 'medium'
            })
        
        if not technical_analysis['has_canonical_url']:
            recommendations.append({
                'type': 'info',
                'category': 'technical',
                'title': 'Add Canonical URL',
                'description': 'Add a canonical URL tag to prevent duplicate content issues',
                'impact': 'low'
            })
        
        return recommendations
