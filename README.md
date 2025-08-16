# SEO Research Pro

A comprehensive SEO analysis tool with keyword research and competitor analysis capabilities.

## Features

- 🔍 **Keyword Analysis**: Extract and analyze keywords from any website
- 🏢 **Competitor Analysis**: Comprehensive SEO and traffic analysis
- 📊 **Traffic Metrics**: Monthly visitors, bounce rate, session duration
- 📈 **SEO Performance**: Domain authority, backlinks, mobile scores
- 🎨 **Modern UI**: Clean, responsive design with real-time data

## Tech Stack

- **Frontend**: Next.js 15, React 18, TypeScript
- **UI**: Tailwind CSS, Radix UI components
- **Backend**: FastAPI (Python)
- **Deployment**: Vercel (Frontend), Custom hosting (Backend)

## Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/shaan566/api_project-123_newone.git
   cd api_project-123_newone
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env.local
   ```
   
   Update `.env.local` with your backend URL:
   ```env
   NEXT_PUBLIC_FASTAPI_URL=http://localhost:8000
   ```

4. **Start the development server**
   ```bash
   npm run dev
   ```

### Vercel Deployment

1. **Connect to Vercel**
   - Go to [vercel.com](https://vercel.com)
   - Import your GitHub repository
   - Configure environment variables

2. **Environment Variables**
   Set the following in Vercel dashboard:
   ```
   NEXT_PUBLIC_FASTAPI_URL=https://your-backend-domain.com
   ```

3. **Deploy**
   - Vercel will automatically build and deploy
   - Your app will be available at `https://your-app.vercel.app`

## API Endpoints

The application connects to a FastAPI backend with these endpoints:

- `GET /keywords?url={url}` - Extract keywords from a website
- `GET /analyze?url={url}` - Comprehensive SEO analysis

## Project Structure

```
├── app/                 # Next.js app directory
│   └── page.tsx        # Main application component
├── components/         # Reusable UI components
├── lib/               # Utility functions
├── backend/           # FastAPI backend (separate deployment)
��── public/            # Static assets
└── styles/            # Global styles
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support, please open an issue on GitHub or contact the maintainers.

---

**Status**: ✅ Production Ready