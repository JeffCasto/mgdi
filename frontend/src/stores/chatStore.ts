import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { ChatMessage } from '../types/chat';
import { api, type ChatRequest, type Model } from '../services/api';

interface ChatSettings {
  provider: string;
  model: string;
  temperature: number;
  maxTokens: number;
  streamingEnabled: boolean;
}

interface ChatStore {
  // Messages
  messages: ChatMessage[];
  currentStreamingMessage: string;
  isStreaming: boolean;
  
  // Settings
  settings: ChatSettings;
  availableModels: Model[];
  
  // UI State
  isLoading: boolean;
  error: string | null;
  
  // Actions
  addMessage: (msg: ChatMessage) => void;
  updateStreamingMessage: (content: string) => void;
  startStreaming: () => void;
  stopStreaming: () => void;
  sendMessage: (content: string, attachments?: any[]) => Promise<void>;
  updateSettings: (settings: Partial<ChatSettings>) => void;
  loadModels: () => Promise<void>;
  clearMessages: () => void;
  setError: (error: string | null) => void;
}

const defaultSettings: ChatSettings = {
  provider: 'openai',
  model: 'gpt-3.5-turbo',
  temperature: 0.7,
  maxTokens: 4096,
  streamingEnabled: true,
};

export const useChatStore = create<ChatStore>()()
  (persist(
    (set, get) => ({
      // State
      messages: [],
      currentStreamingMessage: '',
      isStreaming: false,
      settings: defaultSettings,
      availableModels: [],
      isLoading: false,
      error: null,
      
      // Actions
      addMessage: (msg) => {
        set(state => ({ 
          messages: [...state.messages, msg],
          error: null 
        }));
      },
      
      updateStreamingMessage: (content) => {
        set({ currentStreamingMessage: content });
      },
      
      startStreaming: () => {
        set({ isStreaming: true, currentStreamingMessage: '', error: null });
      },
      
      stopStreaming: () => {
        const { currentStreamingMessage } = get();
        if (currentStreamingMessage) {
          const assistantMessage: ChatMessage = {
            id: Date.now().toString(),
            role: 'assistant',
            content: currentStreamingMessage,
            metadata: {
              model: get().settings.model,
              timestamp: Date.now(),
              tokens: currentStreamingMessage.split(' ').length,
            },
          };
          set(state => ({ 
            messages: [...state.messages, assistantMessage],
            isStreaming: false,
            currentStreamingMessage: '',
          }));
        } else {
          set({ isStreaming: false, currentStreamingMessage: '' });
        }
      },
      
      sendMessage: async (content: string, attachments?: any[]) => {
        const { settings, messages } = get();
        
        // Add user message
        const userMessage: ChatMessage = {
          id: Date.now().toString(),
          role: 'user',
          content,
          attachments,
          metadata: {
            model: settings.model,
            timestamp: Date.now(),
          },
        };
        
        set(state => ({ 
          messages: [...state.messages, userMessage],
          isLoading: true,
          error: null 
        }));
        
        try {
          const chatMessages = [...messages, userMessage].map(msg => ({
            role: msg.role,
            content: msg.content,
          }));
          
          const request: ChatRequest = {
            messages: chatMessages,
            model: settings.model,
            max_tokens: settings.maxTokens,
            temperature: settings.temperature,
            provider: settings.provider,
            stream: settings.streamingEnabled,
          };
          
          if (settings.streamingEnabled) {
            get().startStreaming();
            set({ isLoading: false });
            
            await api.sendMessageStream(request, (chunk) => {
              set(state => ({ 
                currentStreamingMessage: state.currentStreamingMessage + chunk 
              }));
            });
            
            get().stopStreaming();
          } else {
            const response = await api.sendMessage(request);
            
            const assistantMessage: ChatMessage = {
              id: (Date.now() + 1).toString(),
              role: 'assistant',
              content: response.content,
              metadata: {
                model: response.model,
                timestamp: Date.now(),
                tokens: response.metadata.tokens,
              },
            };
            
            set(state => ({ 
              messages: [...state.messages, assistantMessage],
              isLoading: false 
            }));
          }
        } catch (error) {
          set({ 
            isLoading: false, 
            isStreaming: false,
            error: error instanceof Error ? error.message : 'Unknown error' 
          });
        }
      },
      
      updateSettings: (newSettings) => {
        set(state => ({ 
          settings: { ...state.settings, ...newSettings } 
        }));
      },
      
      loadModels: async () => {
        try {
          const models = await api.getModels();
          set({ availableModels: models });
        } catch (error) {
          console.error('Failed to load models:', error);
        }
      },
      
      clearMessages: () => {
        set({ messages: [], error: null });
      },
      
      setError: (error) => {
        set({ error });
      },
    }),
    {
      name: 'mgdi-chat-store',
      partialize: (state) => ({ 
        messages: state.messages,
        settings: state.settings 
      }),
    }
  ));
