/**
 * User making a query to the backend
 * @param formData File form data
 * @returns an error or if its ok
 */

export const user_query = async (query: string) => {
  const res = await fetch(`http://localhost:8000/query`, {
    // replace with your FastAPI URL
    method: "POST",
    body: JSON.stringify({ query: query }),
  });

  if (!res.ok) {
    const errorResponse = await res.json();
    throw new Error(errorResponse.detail || "Failed to make query");
  }

  // Handle the streaming response
  const reader = res.body?.getReader();
  const decoder = new TextDecoder("utf-8");
  let result = "";

  // Read the response stream
  if (reader) {
    while (true) {
      const { done, value } = await reader.read();
      if (done) break; // Exit the loop when the stream is done
      result += decoder.decode(value, { stream: true });
    }
  }

  // Return the accumulated result from the stream
  return result;
};
