// DOMPurify wrapper for input sanitization
import DOMPurify from 'isomorphic-dompurify';
export const sanitizeInput = (input: string) =>
  DOMPurify.sanitize(input, { ALLOWED_TAGS: ['b', 'i', 'code', 'pre', 'a'], ALLOWED_ATTR: ['href', 'target'] });
