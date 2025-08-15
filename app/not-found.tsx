import Link from 'next/link'
 
export default function NotFound() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-6">
      <div className="text-center">
        <h2 className="text-4xl font-bold text-gray-900 mb-4">404 - Page Not Found</h2>
        <p className="text-xl text-gray-600 mb-8">Could not find the requested page.</p>
        <Link 
          href="/"
          className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-semibold transition-colors"
        >
          Return to SEO Analyzer
        </Link>
      </div>
    </div>
  )
}