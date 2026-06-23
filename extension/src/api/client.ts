import type { DecodeRunResponse } from "./types";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

interface ApiErrorBody {
  detail?: unknown;
}

export async function decodeBrief(text: string): Promise<DecodeRunResponse> {
  const response = await fetch(`${API_BASE_URL}/v1/briefs/decode`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ text }),
  });

  if (!response.ok) {
    throw new Error(await getSafeErrorMessage(response));
  }

  return (await response.json()) as DecodeRunResponse;
}

async function getSafeErrorMessage(response: Response): Promise<string> {
  try {
    const body = (await response.json()) as ApiErrorBody;
    if (typeof body.detail === "string") {
      return body.detail;
    }
  } catch {
    return `Request failed with status ${response.status}.`;
  }

  return `Request failed with status ${response.status}.`;
}
