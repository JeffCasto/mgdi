/**
 * The entry point of the application.
 *
 * This file renders the main application component into the DOM.
 */
import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './App';
import './styles/theme.css';

const root = document.getElementById('root');
if (root) {
  createRoot(root).render(<App />);
}
