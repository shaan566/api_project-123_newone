/** @type {import('next').NextConfig} */
const nextConfig = {
  eslint: {
    ignoreDuringBuilds: true,
  },
<<<<<<< HEAD
  images: {
    unoptimized: true,
  },
  // Remove export configuration for local development
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://localhost:5000/api/:path*',
      },
    ];
  },
}

export default nextConfig
=======
  typescript: {
    ignoreBuildErrors: true,
  },
  images: {
    unoptimized: true,
  },
  output: 'export',
  trailingSlash: true,
  distDir: 'out',

  // 👇 Add this block to fix the warning
  experimental: {
    allowedDevOrigins: [
      'http://localhost:3000',
      'http://192.168.1.2:3000',
    ],
  },
}

export default nextConfig;
>>>>>>> 7e044c30eb3e18bd4be2016dcd6352d5244eb229
