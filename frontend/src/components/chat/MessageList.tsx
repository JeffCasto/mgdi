import React, { useEffect, useRef } from 'react';
import { useChatStore } from '../../stores/chatStore';
import type { ChatMessage } from '../../types/chat';

interface MessageProps {
  message: ChatMessage;
}

/**
 * A component to display a single message.
 *
 * This component displays the message content, sender, timestamp, and any
 * attachments or metadata.
 *
 * @param message The message to display.
 * @returns A component to display a single message.
 */
function Message({ message }: MessageProps) {
  const isUser = message.role === 'user';
  const isSystem = message.role === 'system';
  
  return (
    <div className="container" style={{
      borderBottom: '1px solid var(--surface-elevated)',
      background: isSystem ? 'var(--surface-elevated)' : 'transparent'
    }}>
      <div style={{
        display: 'flex',
        flexDirection: 'column',
        gap: '8px'
      }}>
        {/* Message Header */}
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '8px',
          fontSize: '12px',
          color: 'var(--text-secondary)'
        }}>
          <span style={{
            padding: '2px 8px',
            borderRadius: '12px',
            background: isUser ? 'var(--primary)' : 
                       isSystem ? 'var(--accent)' : 'var(--success)',
            color: 'white',
            fontWeight: '500'
          }}>
            {isUser ? 'You' : isSystem ? 'System' : 'Assistant'}
          </span>
          
          {message.metadata.timestamp && (
            <span>
              {new Date(message.metadata.timestamp).toLocaleTimeString()}
            </span>
          )}
          
          {message.metadata.model && (
            <span style={{ opacity: 0.7 }}>
              {message.metadata.model}
            </span>
          )}
          
          {message.metadata.tokens && (
            <span style={{ opacity: 0.7 }}>
              {message.metadata.tokens} tokens
            </span>
          )}
        </div>
        
        {/* Attachments */}
        {message.attachments && message.attachments.length > 0 && (
          <div style={{
            display: 'flex',
            flexWrap: 'wrap',
            gap: '8px',
            marginBottom: '8px'
          }}>
            {message.attachments.map((attachment, index) => (
              <div key={index} style={{
                padding: '8px 12px',
                background: 'var(--surface-elevated)',
                borderRadius: '8px',
                fontSize: '14px',
                color: 'var(--text-secondary)',
                display: 'flex',
                alignItems: 'center',
                gap: '8px'
              }}>
                <span>
                  {attachment.type === 'image' ? '🖼️' : 
                   attachment.type === 'audio' ? '🎵' : '📄'}
                </span>
                <span>{attachment.url.split('/').pop()}</span>
              </div>
            ))}
          </div>
        )}
        
        {/* Message Content */}
        <div style={{
          color: 'var(--text-primary)',
          fontSize: '14px',
          lineHeight: '1.5',
          whiteSpace: 'pre-wrap',
          wordBreak: 'break-word'
        }}>
          {/* For now, just render as text. Later can add markdown support */}
          {message.content}
        </div>
        
        {/* Tools Used */}
        {message.metadata.toolsUsed && message.metadata.toolsUsed.length > 0 && (
          <div style={{
            marginTop: '8px',
            fontSize: '12px',
            color: 'var(--text-secondary)'
          }}>
            <strong>Tools used:</strong> {message.metadata.toolsUsed.join(', ')}
          </div>
        )}
      </div>
    </div>
  );
}

/**
 * A component to display a list of messages.
 *
 * This component displays a list of messages, as well as a streaming message
 * indicator and an error message if one exists.
 *
 * @returns A component to display a list of messages.
 */
export default function MessageList() {
  const { messages, currentStreamingMessage, isStreaming, error } = useChatStore();
  const messagesEndRef = useRef<HTMLDivElement>(null);
  
  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, currentStreamingMessage]);
  
  return (
    <div style={{
      flex: 1,
      overflowY: 'auto',
      display: 'flex',
      flexDirection: 'column'
    }}>
      {/* Error Display */}
      {error && (
        <div style={{
          padding: '16px',
          margin: '16px',
          background: 'var(--error)',
          color: 'white',
          borderRadius: '8px',
          fontSize: '14px'
        }}>
          <strong>Error:</strong> {error}
        </div>
      )}
      
      {/* Empty State */}
      {messages.length === 0 && !isStreaming && (
        <div style={{
          flex: 1,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          flexDirection: 'column',
          gap: '16px',
          color: 'var(--text-secondary)',
          textAlign: 'center',
          padding: '32px'
        }}>
          <div style={{ fontSize: '48px' }}>🤖</div>
          <div>
            <h2 style={{ margin: '0 0 8px 0', color: 'var(--text-primary)' }}>
              Welcome to MGDI
            </h2>
            <p style={{ margin: 0, fontSize: '14px' }}>
              Start a conversation with your AI assistant.
              <br />
              Upload images, audio files, or documents to get started.
            </p>
          </div>
        </div>
      )}
      
      {/* Messages */}
      {messages.map((message) => (
        <Message key={message.id} message={message} />
      ))}
      
      {/* Streaming Message */}
      {isStreaming && currentStreamingMessage && (
        <div style={{
          padding: '16px',
          borderBottom: '1px solid var(--surface-elevated)'
        }}>
          <div style={{
            display: 'flex',
            flexDirection: 'column',
            gap: '8px'
          }}>
            <div style={{
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
              fontSize: '12px',
              color: 'var(--text-secondary)'
            }}>
              <span style={{
                padding: '2px 8px',
                borderRadius: '12px',
                background: 'var(--success)',
                color: 'white',
                fontWeight: '500'
              }}>
                Assistant
              </span>
              <span style={{ opacity: 0.7 }}>typing...</span>
            </div>
            
            <div style={{
              color: 'var(--text-primary)',
              fontSize: '14px',
              lineHeight: '1.5',
              whiteSpace: 'pre-wrap',
              wordBreak: 'break-word'
            }}>
              {currentStreamingMessage}
              <span style={{
                display: 'inline-block',
                width: '2px',
                height: '20px',
                background: 'var(--accent)',
                marginLeft: '2px',
                animation: 'blink 1s infinite'
              }} />
            </div>
          </div>
        </div>
      )}
      
      {/* Scroll anchor */}
      <div ref={messagesEndRef} />
      
      <style>{`
        @keyframes blink {
          0%, 50% { opacity: 1; }
          51%, 100% { opacity: 0; }
        }
      `}</style>
    </div>
  );
}
