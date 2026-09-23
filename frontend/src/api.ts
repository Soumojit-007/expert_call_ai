//files handles all the communication with the backend


import type {
  AnalysisResult,
  ChatResult,
  ComparisonResult,
  Transcript,
} from "./types";

const API_BASE_URL =
//   import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";
  import.meta.env.VITE_API_BASE_URL || "";

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const errorData = await response.json().catch(() => null);

    throw new Error(
      errorData?.detail || `Request failed with status ${response.status}`
    );
  }

  return response.json();
}

// Get all available expert transcripts
export async function getTranscripts(): Promise<{
  transcripts: Transcript[];
}> {
  const response = await fetch(`${API_BASE_URL}/api/transcripts/`);

  return handleResponse(response);
}

// Analyze an interview question
export async function analyzeQuestion(
  question: string,
  market?: string
): Promise<AnalysisResult> {
  const response = await fetch(`${API_BASE_URL}/api/analysis/question`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      question,
      market: market || null,
    }),
  });

  const data = await handleResponse<{
    success: boolean;
    result: AnalysisResult;
  }>(response);

  return data.result;
}

// Compare all three experts
export async function compareExperts(): Promise<ComparisonResult> {
  const response = await fetch(`${API_BASE_URL}/api/analysis/compare`);

  const data = await handleResponse<{
    success: boolean;
    result: ComparisonResult;
  }>(response);

  return data.result;
}

// Ask a question across all transcripts
export async function askAI(question: string): Promise<ChatResult> {
  const response = await fetch(`${API_BASE_URL}/api/chat/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      question,
    }),
  });

  const data = await handleResponse<{
    success: boolean;
    answer: ChatResult;
  }>(response);

  return data.answer;
}