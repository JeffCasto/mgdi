import type { ChatMessage } from '../types/chat';

const API_BASE = 'http://localhost:8000/api';

export interface ChatRequest {
  messages: ChatMessage[];
  model?: string;
  max_tokens?: number;
  temperature?: number;
  provider?: string;
  stream?: boolean;
}

export interface ChatResponse {
  content: string;
  model: string;
  provider: string;
  metadata: Record<string, any>;
}

export interface Provider {
  available: boolean;
  models?: string[];
  error?: string;
}

export interface Model {
  id: string;
  provider: string;
  name: string;
}

/**
 * A class for interacting with the API.
 *
 * This class provides methods for sending messages, getting providers and
 * models, and checking the health of the API.
 */
class ApiService {
  /**
   * Sends a message to the API.
   *
   * @param request The chat request.
   * @returns The chat response.
   */
  async sendMessage(request: ChatRequest): Promise<ChatResponse> {
    const response = await fetch(`${API_BASE}/chat/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${await response.text()}`);
    }

    return response.json();
  }

  /**
   * Sends a message to the API and streams the response.
   *
   * @param request The chat request.
   * @param onChunk A callback to handle each chunk of the response.
   */
  async sendMessageStream(
    request: ChatRequest,
    onChunk: (chunk: string) => void
  ): Promise<void> {
    const response = await fetch(`${API_BASE}/chat/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ ...request, stream: true }),
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${await response.text()}`);
    }

    const reader = response.body?.getReader();
    if (!reader) throw new Error('No response body');

    const decoder = new TextDecoder();
    let buffer = '';

    try {
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop() || '';

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = line.slice(6);
            if (data === '[DONE]') return;
            onChunk(data);
          }
        }
      }
    } finally {
      reader.releaseLock();
    }
  }

  /**
   * Gets a list of available providers from the API.
   *
   * @returns A record of available providers.
   */
  async getProviders(): Promise<Record<string, Provider>> {
    const response = await fetch(`${API_BASE}/chat/providers`);
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${await response.text()}`);
    }
    const data = await response.json();
    return data.providers;
  }

  /**
   * Gets a list of available models from the API.
   *
   * @returns A list of available models.
   */
  async getModels(): Promise<Model[]> {
    const response = await fetch(`${API_BASE}/chat/models`);
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${await response.text()}`);
    }
    const data = await response.json();
    return data.models;
  }

  /**
   * Checks the health of the API.
   *
   * @returns An object with the health status and version of the API.
   */
  async healthCheck(): Promise<{ status: string; version: string }> {
    const response = await fetch(`${API_BASE.replace('/api', '')}/health`);
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${await response.text()}`);
    }
    return response.json();
  }
}

export const api = new ApiService();
