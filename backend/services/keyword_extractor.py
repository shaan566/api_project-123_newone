import logging
import re
import asyncio
from typing import Dict, List, Optional, Tuple
from collections import Counter
import math
import random

try:
    from keybert import KeyBERT
    from yake import KeywordExtractor as YakeExtractor
    ADVANCED_EXTRACTION = True
except ImportError:
    ADVANCED_EXTRACTION = False
    logging.warning("KeyBERT or YAKE not available. Using basic keyword extraction.")

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag

logger = logging.getLogger(__name__)

class KeywordExtractor:
    def __init__(self):
        self._download_nltk_data()
        
        if ADVANCED_EXTRACTION:
            try:
                self.keybert_model = KeyBERT()
                self.yake_extractor = YakeExtractor()
            except Exception as e:
                logger.warning(f"Error initializing advanced extractors: {e}")
                self.keybert_model = None
                self.yake_extractor = None
        else:
            self.keybert_model = None
            self.yake_extractor = None
        
        try:
            self.stop_words = set(stopwords.words('english'))
        except:
            self.stop_words = set()
    
    def _download_nltk_data(self):
        """Download required NLTK data"""
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            try:
                nltk.download('punkt', quiet=True)
            except:
                pass
        
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            try:
                nltk.download('stopwords', quiet=True)
            except:
                pass
        
        try:
            nltk.data.find('taggers/averaged_perceptron_tagger')
        except LookupError:
            try:
                nltk.download('averaged_perceptron_tagger', quiet=True)
            except:
                pass
    
    async def extract_keywords(self, content: str, num_keywords: int = 20) -> List[Dict]:
        """Extract keywords from content using multiple methods"""
        if not content or len(content.strip()) < 50:
            return []
        
        try:
            # Use advanced extraction if available
            if self.keybert_model:
                advanced_keywords = await self._extract_with_keybert(content, num_keywords)
                if advanced_keywords:
                    return advanced_keywords
            
            # Fallback to basic extraction
            return await self._extract_basic_keywords(content, num_keywords)
            
        except Exception as e:
            logger.error(f"Error extracting keywords: {str(e)}")
            return await self._extract_basic_keywords(content, num_keywords)
    
    async def _extract_with_keybert(self, content: str, num_keywords: int) -> List[Dict]:
        """Extract keywords using KeyBERT"""
        try:
            # Extract keywords with KeyBERT
            keybert_keywords = self.keybert_model.extract_keywords(
                content, 
                keyphrase_ngram_range=(1, 3),
                stop_words='english',
                top_k=num_keywords
            )
            
            keywords = []
            for keyword, relevance_score in keybert_keywords:
                # Generate realistic SEO metrics
                search_volume = self._generate_search_volume(keyword, relevance_score)
                difficulty = self._calculate_keyword_difficulty(keyword, relevance_score)
                cpc = self._generate_cpc(keyword, search_volume, difficulty)
                
                keywords.append({
                    'keyword': keyword,
                    'relevance_score': round(relevance_score, 3),
                    'search_volume': search_volume,
                    'keyword_difficulty': difficulty,
                    'cpc': cpc,
                    'competition': self._get_competition_level(difficulty),
                    'trend': self._generate_trend_data()
                })
            
            return keywords
            
        except Exception as e:
            logger.error(f"KeyBERT extraction failed: {str(e)}")
            return []
    
    async def _extract_basic_keywords(self, content: str, num_keywords: int) -> List[Dict]:
        """Basic keyword extraction using NLTK and frequency analysis"""
        try:
            # Clean and tokenize content
            clean_content = re.sub(r'[^\w\s]', ' ', content.lower())
            words = word_tokenize(clean_content)
            
            # Remove stopwords and short words
            filtered_words = [
                word for word in words 
                if word not in self.stop_words and len(word) > 2 and word.isalpha()
            ]
            
            # Get POS tags to focus on nouns and adjectives
            try:
                pos_tags = pos_tag(filtered_words)
                relevant_words = [
                    word for word, pos in pos_tags 
                    if pos in ['NN', 'NNS', 'NNP', 'NNPS', 'JJ', 'JJR', 'JJS']
                ]
            except:
                relevant_words = filtered_words
            
            # Count word frequencies
            word_freq = Counter(relevant_words)
            
            # Generate n-grams (2 and 3 word phrases)
            bigrams = self._generate_ngrams(filtered_words, 2)
            trigrams = self._generate_ngrams(filtered_words, 3)
            
            # Combine and score keywords
            all_keywords = {}
            
            # Single words
            for word, freq in word_freq.most_common(num_keywords * 2):
                score = freq / len(filtered_words)
                all_keywords[word] = score
            
            # Bigrams
            for bigram, freq in Counter(bigrams).most_common(num_keywords):
                phrase = ' '.join(bigram)
                score = freq / len(bigrams) if bigrams else 0
                all_keywords[phrase] = score
            
            # Trigrams
            for trigram, freq in Counter(trigrams).most_common(num_keywords // 2):
                phrase = ' '.join(trigram)
                score = freq / len(trigrams) if trigrams else 0
                all_keywords[phrase] = score
            
            # Sort by score and create keyword objects
            sorted_keywords = sorted(all_keywords.items(), key=lambda x: x[1], reverse=True)
            
            keywords = []
            for keyword, relevance_score in sorted_keywords[:num_keywords]:
                search_volume = self._generate_search_volume(keyword, relevance_score)
                difficulty = self._calculate_keyword_difficulty(keyword, relevance_score)
                cpc = self._generate_cpc(keyword, search_volume, difficulty)
                
                keywords.append({
                    'keyword': keyword,
                    'relevance_score': round(relevance_score, 3),
                    'search_volume': search_volume,
                    'keyword_difficulty': difficulty,
                    'cpc': cpc,
                    'competition': self._get_competition_level(difficulty),
                    'trend': self._generate_trend_data()
                })
            
            return keywords
            
        except Exception as e:
            logger.error(f"Basic keyword extraction failed: {str(e)}")
            return []
    
    def _generate_ngrams(self, words: List[str], n: int) -> List[Tuple]:
        """Generate n-grams from word list"""
        ngrams = []
        for i in range(len(words) - n + 1):
            ngram = tuple(words[i:i + n])
            # Skip n-grams with too many common words
            if sum(1 for word in ngram if word in self.stop_words) < n // 2:
                ngrams.append(ngram)
        return ngrams
    
    def _generate_search_volume(self, keyword: str, relevance_score: float) -> int:
        """Generate realistic search volume based on keyword characteristics"""
        # Base volume calculation
        base_volume = int(relevance_score * 10000)
        
        # Adjust based on keyword length
        word_count = len(keyword.split())
        if word_count == 1:
            multiplier = random.uniform(0.8, 3.0)
        elif word_count == 2:
            multiplier = random.uniform(0.4, 1.5)
        else:
            multiplier = random.uniform(0.1, 0.8)
        
        # Adjust based on keyword type
        commercial_indicators = ['buy', 'price', 'cost', 'cheap', 'best', 'review', 'compare']
        if any(indicator in keyword.lower() for indicator in commercial_indicators):
            multiplier *= random.uniform(1.2, 2.0)
        
        # Add some randomness
        final_volume = int(base_volume * multiplier * random.uniform(0.7, 1.3))
        
        # Round to realistic numbers
        if final_volume < 10:
            return random.randint(0, 50)
        elif final_volume < 100:
            return round(final_volume, -1)
        elif final_volume < 1000:
            return round(final_volume, -2)
        else:
            return round(final_volume, -3)
    
    def _calculate_keyword_difficulty(self, keyword: str, relevance_score: float) -> int:
        """Calculate keyword difficulty score (0-100)"""
        # Base difficulty
        base_difficulty = 50
        
        # Adjust based on keyword length
        word_count = len(keyword.split())
        if word_count == 1:
            base_difficulty += random.randint(10, 30)
        elif word_count >= 3:
            base_difficulty -= random.randint(10, 25)
        
        # Adjust based on commercial intent
        commercial_indicators = ['buy', 'price', 'cost', 'cheap', 'best', 'review']
        if any(indicator in keyword.lower() for indicator in commercial_indicators):
            base_difficulty += random.randint(5, 20)
        
        # Adjust based on common terms
        common_terms = ['the', 'and', 'for', 'with', 'how', 'what', 'why', 'when']
        if any(term in keyword.lower() for term in common_terms):
            base_difficulty -= random.randint(5, 15)
        
        # Add relevance factor
        relevance_adjustment = (relevance_score - 0.5) * 20
        base_difficulty += relevance_adjustment
        
        # Ensure within bounds
        difficulty = max(1, min(100, int(base_difficulty + random.randint(-10, 10))))
        return difficulty
    
    def _generate_cpc(self, keyword: str, search_volume: int, difficulty: int) -> float:
        """Generate realistic CPC based on keyword characteristics"""
        # Base CPC
        base_cpc = 0.50
        
        # Adjust based on commercial intent
        commercial_indicators = ['buy', 'price', 'cost', 'cheap', 'best', 'review', 'compare']
        if any(indicator in keyword.lower() for indicator in commercial_indicators):
            base_cpc *= random.uniform(2.0, 8.0)
        
        # Adjust based on search volume
        if search_volume > 10000:
            base_cpc *= random.uniform(1.5, 3.0)
        elif search_volume > 1000:
            base_cpc *= random.uniform(1.2, 2.0)
        
        # Adjust based on difficulty
        difficulty_multiplier = 1 + (difficulty / 100) * random.uniform(0.5, 2.0)
        base_cpc *= difficulty_multiplier
        
        # Industry-specific adjustments
        high_value_terms = ['insurance', 'loan', 'mortgage', 'attorney', 'lawyer', 'credit']
        if any(term in keyword.lower() for term in high_value_terms):
            base_cpc *= random.uniform(3.0, 15.0)
        
        # Round to realistic cents
        final_cpc = round(base_cpc * random.uniform(0.7, 1.3), 2)
        return max(0.01, min(50.00, final_cpc))
    
    def _get_competition_level(self, difficulty: int) -> str:
        """Get competition level based on difficulty score"""
        if difficulty < 30:
            return "Low"
        elif difficulty < 60:
            return "Medium"
        elif difficulty < 80:
            return "High"
        else:
            return "Very High"
    
    def _generate_trend_data(self) -> List[int]:
        """Generate realistic trend data for the last 12 months"""
        # Start with a base value
        base_value = random.randint(40, 80)
        trend_data = [base_value]
        
        # Generate 11 more months with realistic variations
        for _ in range(11):
            # Add some seasonality and randomness
            change = random.randint(-15, 15)
            new_value = max(0, min(100, trend_data[-1] + change))
            trend_data.append(new_value)
        
        return trend_data
    
    async def research_keyword(self, keyword: str, location: str = "US", language: str = "en") -> Dict:
        """Comprehensive keyword research for a specific keyword"""
        try:
            logger.info(f"Researching keyword: {keyword}")
            
            # Generate base metrics
            search_volume = self._generate_search_volume(keyword, 0.7)
            difficulty = self._calculate_keyword_difficulty(keyword, 0.7)
            cpc = self._generate_cpc(keyword, search_volume, difficulty)
            competition = self._get_competition_level(difficulty)
            
            # Generate related keywords
            related_keywords = await self._generate_related_keywords(keyword)
            
            # Generate SERP features
            serp_features = self._generate_serp_features(keyword)
            
            # Generate top competitors
            top_competitors = self._generate_top_competitors(keyword)
            
            # Generate content suggestions
            content_suggestions = self._generate_content_suggestions(keyword)
            
            return {
                'search_volume': search_volume,
                'difficulty': difficulty,
                'cpc': cpc,
                'competition': competition,
                'related_keywords': related_keywords,
                'serp_features': serp_features,
                'top_competitors': top_competitors,
                'content_suggestions': content_suggestions,
                'trend_data': self._generate_trend_data(),
                'seasonal_trends': self._generate_seasonal_trends(),
                'location': location,
                'language': language
            }
            
        except Exception as e:
            logger.error(f"Error in keyword research: {str(e)}")
            raise Exception(f"Keyword research failed: {str(e)}")
    
    async def _generate_related_keywords(self, keyword: str, count: int = 15) -> List[Dict]:
        """Generate related keywords based on the target keyword"""
        related = []
        
        # Generate variations
        variations = [
            f"best {keyword}",
            f"{keyword} review",
            f"{keyword} guide",
            f"how to {keyword}",
            f"{keyword} tips",
            f"{keyword} cost",
            f"{keyword} near me",
            f"{keyword} online",
            f"free {keyword}",
            f"{keyword} comparison",
            f"{keyword} benefits",
            f"{keyword} problems",
            f"{keyword} alternatives",
            f"{keyword} vs",
            f"{keyword} software"
        ]
        
        # Add some single word variations
        words = keyword.split()
        if len(words) > 1:
            for word in words:
                if word not in self.stop_words:
                    variations.extend([
                        f"{word} tools",
                        f"{word} service",
                        f"{word} solution"
                    ])
        
        # Generate metrics for each variation
        for variation in variations[:count]:
            if variation != keyword:
                search_vol = self._generate_search_volume(variation, 0.6)
                diff = self._calculate_keyword_difficulty(variation, 0.6)
                
                related.append({
                    'keyword': variation,
                    'search_volume': search_vol,
                    'keyword_difficulty': diff,
                    'cpc': self._generate_cpc(variation, search_vol, diff),
                    'competition': self._get_competition_level(diff)
                })
        
        return sorted(related, key=lambda x: x['search_volume'], reverse=True)
    
    def _generate_serp_features(self, keyword: str) -> List[str]:
        """Generate likely SERP features for a keyword"""
        features = []
        
        # Commercial keywords likely have shopping results
        commercial_indicators = ['buy', 'price', 'cost', 'cheap', 'best', 'review']
        if any(indicator in keyword.lower() for indicator in commercial_indicators):
            features.extend(['Shopping Results', 'Ad Results'])
        
        # How-to keywords likely have featured snippets
        if any(term in keyword.lower() for term in ['how', 'what', 'why', 'guide']):
            features.extend(['Featured Snippet', 'People Also Ask'])
        
        # Local intent
        if 'near me' in keyword.lower() or 'local' in keyword.lower():
            features.extend(['Local Pack', 'Map Results'])
        
        # Common features
        if random.random() > 0.3:
            features.append('Knowledge Panel')
        if random.random() > 0.5:
            features.append('Related Searches')
        if random.random() > 0.4:
            features.append('Image Pack')
        if random.random() > 0.6:
            features.append('Video Results')
        
        return list(set(features))
    
    def _generate_top_competitors(self, keyword: str, count: int = 10) -> List[Dict]:
        """Generate top competitors for a keyword"""
        # Common domain patterns based on keyword type
        domain_patterns = [
            "wikipedia.org", "youtube.com", "amazon.com", "reddit.com",
            "quora.com", "medium.com", "forbes.com", "techcrunch.com",
            "hubspot.com", "moz.com", "semrush.com", "ahrefs.com"
        ]
        
        competitors = []
        for i in range(count):
            domain = random.choice(domain_patterns)
            
            competitors.append({
                'position': i + 1,
                'url': f"https://{domain}/article-about-{keyword.replace(' ', '-')}",
                'domain': domain,
                'title': f"Ultimate Guide to {keyword.title()}",
                'estimated_traffic': random.randint(100, 10000),
                'domain_authority': random.randint(30, 95),
                'word_count': random.randint(500, 3000)
            })
        
        return competitors
    
    def _generate_content_suggestions(self, keyword: str) -> List[Dict]:
        """Generate content suggestions for a keyword"""
        suggestions = [
            {
                'type': 'Blog Post',
                'title': f"The Complete Guide to {keyword.title()}",
                'suggested_length': "2000-3000 words",
                'content_type': 'Educational'
            },
            {
                'type': 'How-to Guide',
                'title': f"How to Get Started with {keyword.title()}",
                'suggested_length': "1500-2500 words",
                'content_type': 'Tutorial'
            },
            {
                'type': 'Comparison',
                'title': f"Best {keyword.title()} Tools in 2024",
                'suggested_length': "1000-2000 words",
                'content_type': 'Review'
            },
            {
                'type': 'FAQ',
                'title': f"Frequently Asked Questions About {keyword.title()}",
                'suggested_length': "800-1200 words",
                'content_type': 'FAQ'
            }
        ]
        
        return suggestions
    
    def _generate_seasonal_trends(self) -> Dict:
        """Generate seasonal trend information"""
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        
        # Generate seasonal pattern
        peak_months = random.sample(months, random.randint(1, 3))
        low_months = random.sample([m for m in months if m not in peak_months], random.randint(1, 2))
        
        return {
            'peak_months': peak_months,
            'low_months': low_months,
            'seasonality_score': random.randint(20, 80),
            'pattern': random.choice(['Steady', 'Seasonal', 'Trending Up', 'Trending Down'])
        }
