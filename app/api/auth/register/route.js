import { NextResponse } from "next/server";

const apiUrl = process.env.API_URL || process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

export async function POST(request) {
  try {
    const upstream = await fetch(`${apiUrl}/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(await request.json()),
    });
    const body = await upstream.text();
    let data = {};
    try { data = body ? JSON.parse(body) : {}; } catch { data = { detail: body }; }
    return NextResponse.json(data, { status: upstream.status });
  } catch {
    return NextResponse.json({ detail: "Could not reach the FastAPI server at port 8000." }, { status: 503 });
  }
}
