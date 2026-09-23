export interface Evidence {
  expert: string;
  role: string;
  market: string;
  timestamp: string;
  speaker: string;
  quote: string;
  distance?: number;
}

export interface Expert {
  expert: string;
  role: string;
  market: string;
}

export interface AnalysisResult {
  question: string;
  answer: string;
  evidence: Evidence[];
}

export interface ComparisonResult {
  comparison: string;
  experts: Expert[];
}

export interface ChatResult {
  answer: string;
  evidence: Evidence[];
}

export interface Transcript {
  id: string;
  expert: string;
  role: string;
  market: string;
}