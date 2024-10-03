"use server";

import { NextResponse } from "next/server";

interface searchData {
  query: string;
}

export async function POST(request: Request) {
  //grab parameters from the request to forward it through
  const { query }: Partial<searchData> = await request.json();
  /*
  selected could be an empty array, participants could also be an empty array so we give an optional type here
    */
  if (!query)
    return NextResponse.json(
      { message: "Invalid Parameters" },
      { status: 400 }
    );

  const res = await fetch(`http://localhost:8000/query`, {
    method: "POST",
    body: JSON.stringify({ query: query }),
  });

}
