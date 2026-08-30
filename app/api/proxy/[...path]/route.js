import { cookies } from "next/headers";
import { NextResponse } from "next/server";

const apiUrl = process.env.API_URL || process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

async function proxy(request, { params }) {
  const token = cookies().get("stockflow_token")?.value;
  const path = params.path.join("/");
  const headers = {};
  if (token) headers.Authorization = `Bearer ${token}`;
  if (request.method !== "GET") headers["Content-Type"] = "application/json";

  try {
    const upstream = await fetch(`${apiUrl}/${path}`, {
      method: request.method,
      headers,
      body: request.method === "GET" ? undefined : await request.text(),
      cache: "no-store",
    });
    const contentType = upstream.headers.get("content-type") || "application/json";
    return new NextResponse(await upstream.arrayBuffer(), { status: upstream.status, headers: { "Content-Type": contentType } });
  } catch {
    return NextResponse.json({ detail: "Could not reach the FastAPI server at port 8000." }, { status: 503 });
  }
}

export const GET = proxy;
export const POST = proxy;
export const DELETE = proxy;
export const PUT = proxy;
