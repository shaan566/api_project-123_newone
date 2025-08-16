# SEO Research Pro

## Overview

SEO Research Pro is a comprehensive SEO keyword research and competitor analysis tool built with a modern microservices architecture. The application provides real-time keyword research, competitor analysis, and URL content extraction capabilities. It features a Next.js frontend for user interaction and a FastAPI backend for data processing and analysis.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Next.js 14 with App Router for modern React development
- **Language**: TypeScript for type safety and better development experience
- **Styling**: Tailwind CSS with shadcn/ui component library for consistent design
- **UI Components**: Extensive use of Radix UI primitives through shadcn/ui for accessibility and consistency
- **State Management**: React hooks and form handling with react-hook-form
- **Theme Support**: Built-in dark/light mode switching with next-themes

### Backend Architecture
- **Framework**: FastAPI for high-performance async API development
- **Language**: Python 3.8+ with modern async/await patterns
- **API Design**: RESTful endpoints with comprehensive request/response models using Pydantic
- **Async Processing**: Background tasks for long-running operations like web scraping
- **Service Layer**: Modular service architecture with separate concerns:
  - `WebScraper`: URL content extraction and parsing
  - `SEOAnalyzer`: Page optimization analysis and scoring
  - `KeywordExtractor`: Keyword research and extraction
  - `CompetitorAnalyzer`: Competitive intelligence and analysis
- **Error Handling**: Comprehensive logging and error tracking with request statistics
- **CORS**: Cross-origin resource sharing enabled for frontend integration
 ```bash
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

### Data Processing Architecture
- **Content Extraction**: Multi-layered approach using trafilatura, BeautifulSoup, and Selenium
- **SEO Analysis**: Custom scoring algorithms for page optimization metrics
- **Keyword Research**: Advanced NLP processing with KeyBERT and YAKE for keyword extraction
- **Text Analysis**: NLTK for natural language processing and readability scoring

### Request Flow
1. Frontend sends requests to FastAPI backend
2. Backend validates input using Pydantic models
3. Service layer processes requests with specialized analyzers
4. Results are formatted and returned as structured JSON responses
5. Frontend displays results in interactive UI components

## External Dependencies

### Frontend Dependencies
- **Next.js Ecosystem**: React 18, Next.js 15 for core framework
- **UI Libraries**: Radix UI components, Lucide React icons, class-variance-authority for styling
- **Form Handling**: react-hook-form with resolvers for validation
- **Date Utilities**: date-fns for date manipulation
- **Carousel**: embla-carousel-react for image/content carousels

### Backend Dependencies
- **Web Framework**: FastAPI with uvicorn ASGI server
- **HTTP Clients**: aiohttp for async requests, requests for synchronous operations
- **Web Scraping**: 
  - trafilatura for content extraction
  - BeautifulSoup4 and lxml for HTML parsing
  - Selenium with webdriver-manager for dynamic content
  - fake-useragent for request headers
- **NLP and Text Analysis**:
  - NLTK for natural language processing
  - KeyBERT for keyword extraction
  - YAKE for automated keyword extraction
  - textstat for readability analysis
- **Data Processing**: pandas and numpy for data manipulation, scikit-learn for machine learning features
- **Utilities**: python-whois for domain analysis, asyncio-throttle for rate limiting

### Development Tools
- **TypeScript**: Type checking and development tooling
- **ESLint**: Code linting and formatting
- **Tailwind CSS**: Utility-first CSS framework
- **PostCSS/Autoprefixer**: CSS processing and vendor prefixing

### External Services Integration
- **Search Engines**: Web scraping capabilities for search result analysis
- **Domain Analysis**: WHOIS data integration for competitor research
- **Content APIs**: Trafilatura for reliable content extraction across various websites