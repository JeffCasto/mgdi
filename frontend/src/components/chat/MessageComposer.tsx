import React, { useState, useRef } from 'react';
import { useChatStore } from '../../stores/chatStore';

export default function MessageComposer() {
  const [input, setInput] = useState('');
  const [attachments, setAttachments] = useState<File[]>([]);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  
  const { sendMessage, isLoading, isStreaming } = useChatStore();
  
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading || isStreaming) return;
    
    const message = input.trim();
    setInput('');
    setAttachments([]);
    
    // Auto-resize textarea
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
    }
    
    await sendMessage(message, attachments);
  };
  
  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };
  
  const handleInputChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setInput(e.target.value);
    
    // Auto-resize textarea
    const textarea = e.target;
    textarea.style.height = 'auto';
    textarea.style.height = `${Math.min(textarea.scrollHeight, 200)}px`;
  };
  
  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(e.target.files || []);
    setAttachments(prev => [...prev, ...files]);
  };
  
  const removeAttachment = (index: number) => {
    setAttachments(prev => prev.filter((_, i) => i !== index));
  };
  
  const disabled = isLoading || isStreaming;
  
  return (
    <div style={{
      padding: '16px',
      borderTop: '1px solid var(--surface-elevated)',
      background: 'var(--surface)'
    }}>
      {/* Attachments Preview */}
      {attachments.length > 0 && (
        <div style={{
          marginBottom: '12px',
          display: 'flex',
          flexWrap: 'wrap',
          gap: '8px'
        }}>
          {attachments.map((file, index) => (
            <div key={index} style={{
              display: 'flex',
              alignItems: 'center',
              padding: '6px 12px',
              background: 'var(--surface-elevated)',
              borderRadius: '6px',
              fontSize: '14px',
              color: 'var(--text-secondary)'
            }}>
              <span style={{ marginRight: '8px' }}>
                {file.type.startsWith('image/') ? '🖼️' : 
                 file.type.startsWith('audio/') ? '🎵' : '📄'}
              </span>
              <span>{file.name}</span>
              <button
                onClick={() => removeAttachment(index)}
                style={{
                  marginLeft: '8px',
                  background: 'none',
                  border: 'none',
                  color: 'var(--error)',
                  cursor: 'pointer',
                  fontSize: '16px'
                }}
              >
                ×
              </button>
            </div>
          ))}
        </div>
      )}
      
      {/* Input Form */}
      <form onSubmit={handleSubmit} style={{ display: 'flex', gap: '12px' }}>
        <div style={{ flex: 1, position: 'relative' }}>
          <textarea
            ref={textareaRef}
            value={input}
            onChange={handleInputChange}
            onKeyDown={handleKeyDown}
            placeholder={disabled ? 'Sending...' : 'Type your message... (Shift+Enter for new line)'}
            disabled={disabled}
            style={{
              width: '100%',
              minHeight: '44px',
              maxHeight: '200px',
              padding: '12px 16px',
              border: '1px solid var(--surface-elevated)',
              borderRadius: '8px',
              background: 'var(--surface-elevated)',
              color: 'var(--text-primary)',
              fontSize: '14px',
              resize: 'none',
              outline: 'none',
              fontFamily: 'inherit'
            }}
          />
        </div>
        
        <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
          {/* File Upload Button */}
          <button
            type="button"
            onClick={() => fileInputRef.current?.click()}
            disabled={disabled}
            style={{
              padding: '12px',
              border: 'none',
              borderRadius: '8px',
              background: 'var(--surface-elevated)',
              color: 'var(--text-secondary)',
              cursor: disabled ? 'not-allowed' : 'pointer',
              fontSize: '16px',
              opacity: disabled ? 0.5 : 1
            }}
            title="Attach files"
          >
            📎
          </button>
          
          {/* Send Button */}
          <button
            type="submit"
            disabled={!input.trim() || disabled}
            style={{
              padding: '12px',
              border: 'none',
              borderRadius: '8px',
              background: (!input.trim() || disabled) ? 
                'var(--surface-elevated)' : 'var(--primary)',
              color: (!input.trim() || disabled) ? 
                'var(--text-secondary)' : 'white',
              cursor: (!input.trim() || disabled) ? 'not-allowed' : 'pointer',
              fontSize: '16px',
              transition: 'all 0.2s ease'
            }}
            title="Send message"
          >
            {isLoading || isStreaming ? '⏳' : '⬆️'}
          </button>
        </div>
        
        {/* Hidden File Input */}
        <input
          ref={fileInputRef}
          type="file"
          multiple
          accept="image/*,audio/*,.txt,.pdf,.doc,.docx,.json,.csv"
          onChange={handleFileSelect}
          style={{ display: 'none' }}
        />
      </form>
    </div>
  );
}
