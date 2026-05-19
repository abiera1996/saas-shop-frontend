import { NextRequest, NextResponse } from "next/server";
import { cookies } from "next/headers";
import { logger } from "@/lib/logger";

const DJANGO_API_URL = "http://localhost:8000/api";

export async function GET(req: NextRequest, { params }: { params: Promise<{ path: string[] }> }) {
  return handleProxy(req, await params);
}

export async function POST(req: NextRequest, { params }: { params: Promise<{ path: string[] }> }) {
  return handleProxy(req, await params);
}

export async function PUT(req: NextRequest, { params }: { params: Promise<{ path: string[] }> }) {
  return handleProxy(req, await params);
}

export async function DELETE(req: NextRequest, { params }: { params: Promise<{ path: string[] }> }) {
  return handleProxy(req, await params);
}

async function handleProxy(req: NextRequest, params: { path: string[] }) {
  const pathObj = await params;
  const targetPath = pathObj.path.join("/");
  
  // Extract HttpOnly cookie
  const cookieStore = await cookies();
  const accessToken = cookieStore.get("access_token")?.value;

  // Prepare headers
  const headers = new Headers();
  headers.set("Content-Type", "application/json");
  
  // Forward client-side Authorization header if present (e.g. customer storefront token)
  const clientAuth = req.headers.get("Authorization");
  if (clientAuth) {
    headers.set("Authorization", clientAuth);
  } else if (accessToken && !targetPath.startsWith("storefront/")) {
    // Only use HTTP-only admin cookie access token for non-storefront (dashboard/admin) requests
    headers.set("Authorization", `Bearer ${accessToken}`);
  }

  // Handle Request Body for POST/PUT
  let body = undefined;
  if (req.method !== "GET" && req.method !== "HEAD") {
    try {
      body = await req.text();
    } catch (e) {
      // no body
    }
  }

  const start = Date.now();
  const res = await fetch(`${DJANGO_API_URL}/${targetPath}/`, {
    method: req.method,
    headers,
    body,
  });
  const duration = Date.now() - start;

  logger.info(`[SSR PROXY] ${req.method} /api/proxy/${targetPath} -> Django Status: ${res.status} (${duration}ms)`);

  // Read response
  const data = await res.text();
  let parsedData = data;
  try {
    parsedData = JSON.parse(data);
  } catch (e) {
    // Keep as text if parsing fails
  }

  // Handle Unauthorized globally
  if (res.status === 401) {
    return NextResponse.json({ detail: "Unauthorized" }, { status: 401 });
  }

  return NextResponse.json(parsedData, { status: res.status });
}
