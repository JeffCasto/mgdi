/**
 * A wrapper for DOMPurify to sanitize HTML.
 *
 * @param html The HTML to sanitize.
 * @returns The sanitized HTML.
 */
import DOMPurify from 'isomorphic-dompurify';

export const sanitizeHtml = (html: string) =>
  DOMPurify.sanitize(html, { ALLOWED_TAGS: ['b', 'i', 'code', 'pre', 'a'], ALLOWED_ATTR: ['href', 'target'] });
