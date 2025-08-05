/** @type {import('next').NextConfig} */
const nextConfig = {
  eslint: {
    ignoreDuringBuilds: true,
  },
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
