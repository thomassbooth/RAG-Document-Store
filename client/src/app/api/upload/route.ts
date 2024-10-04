"use server";

import { NextResponse } from "next/server";

export async function POST(request: Request) {
  console.log("hi");
  //grab parameters from the request to forward it through
  try {
    const formData = await request.formData();
    console.log(formData);
    /*
  selected could be an empty array, participants could also be an empty array so we give an optional type here
    */
    console.log(formData);
    if (!formData)
      return NextResponse.json(
        { message: "Invalid Parameters" },
        { status: 400 }
      );
    const res = await fetch(`http://localhost:8000/upload`, {
      method: "POST",
      body: formData,
    });

    if (!res.ok) {
      return NextResponse.json(
        { message: "Unable to upload." },
        { status: 400 }
      );
    }
  } catch (e) {
    console.log(e);
  }
  return NextResponse.json("Uploaded");
}
