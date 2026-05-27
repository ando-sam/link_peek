import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  async rewrites() {
    return [
      {
        source: "/api/preview",
        destination: "http://127.0.0.1:8000/api/preview/",
      },
    ];
  },
};

export default nextConfig;
