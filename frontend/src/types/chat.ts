// Types for chat messages and attachments
export interface Attachment {
  id: string;
  type: 'image' | 'audio' | 'file';
  url: string;
}

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  attachments?: Attachment[];
  metadata: {
    model: string;
    timestamp: number;
    tokens?: number;
    toolsUsed?: string[];
  };
}
