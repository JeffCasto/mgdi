/**
 * An interface for an attachment.
 */
export interface Attachment {
  id: string;
  type: "image" | "audio" | "file";
  url: string;
}

/**
 * An interface for a chat message.
 */
export interface ChatMessage {
  id: string;
  role: "user" | "assistant" | "system";
  content: string;
  attachments?: Attachment[];
  metadata: {
    model: string;
    timestamp: number;
    tokens?: number;
    toolsUsed?: string[];
  };
}
