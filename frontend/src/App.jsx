import React, { useState, useEffect, useRef } from 'react';
import ReactMarkdown from 'react-markdown';
import './index.css';

function App() {
  const [url, setUrl] = useState('');
  const [scroll, setScroll] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [isStreaming, setIsStreaming] = useState(false);
  const [summary, setSummary] = useState(null);
  const [error, setError] = useState(null);
  const [progressStep, setProgressStep] = useState(0);
  const resultRef = useRef(null);

  // Progress steps during loading (before streaming begins)
  useEffect(() => {
    let timers = [];
    if (isLoading && !isStreaming) {
      setProgressStep(1);
      timers.push(setTimeout(() => setProgressStep(2), 4000));
    } else if (isStreaming) {
      setProgressStep(3);
    } else {
      setProgressStep(0);
    }
    return () => timers.forEach(clearTimeout);
  }, [isLoading, isStreaming]);

  // Auto-scroll to result once streaming begins
  useEffect(() => {
    if (isStreaming && resultRef.current) {
      resultRef.current.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  }, [isStreaming]);

  const handleSummarize = async () => {
    if (!url) {
      setError('Please enter a valid URL.');
      return;
    }

    // Auto-prepend https:// if missing
    let finalUrl = url.trim();
    if (!finalUrl.startsWith('http://') && !finalUrl.startsWith('https://')) {
      finalUrl = 'https://' + finalUrl;
      setUrl(finalUrl);
    }

    setIsLoading(true);
    setIsStreaming(false);
    setError(null);
    setSummary(null);

    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';
      const response = await fetch(`${apiUrl}/summarize`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: finalUrl, scroll })
      });

      if (!response.ok) {
        throw new Error(`Server returned an error (Status ${response.status})`);
      }

      // Stream the response body chunk by chunk
      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let accumulated = '';

      setIsStreaming(true);

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value, { stream: true });
        accumulated += chunk;
        setSummary(accumulated);
      }
    } catch (err) {
      if (err.message.includes('Failed to fetch') || err.message.includes('NetworkError')) {
        setError('Cannot connect to the backend server. Make sure to run: python main.py');
      } else {
        setError(err.message);
      }
    } finally {
      setIsLoading(false);
      setIsStreaming(false);
    }
  };

  return (
    <div className="app-container">
      <div className="glass-card">

        {/* Header */}
        <div className="header-section">
          <div className="header-icon">✨</div>
          <h1>AI Website Summarizer</h1>
          <p className="subtitle">
            Paste any URL and let AI extract the key insights for you.
          </p>
        </div>

        {/* URL Input */}
        <div className="input-group">
          <span className="input-icon">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71" />
              <path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71" />
            </svg>
          </span>
          <input
            type="text"
            placeholder="https://example.com"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && !isLoading && handleSummarize()}
          />
        </div>

        {/* Scroll Engine Toggle */}
        <label className="checkbox-group">
          <input
            type="checkbox"
            checked={scroll}
            onChange={(e) => setScroll(e.target.checked)}
          />
          Enable Scroll Engine (Catches lazy-loaded content)
        </label>

        {/* Submit Button */}
        <button
          className="summarize-btn"
          onClick={handleSummarize}
          disabled={isLoading}
        >
          {isLoading ? (
            <div className="loading-text">
              <span className="loader"></span>
              {isStreaming ? 'Streaming Result...' : 'Analyzing Website...'}
            </div>
          ) : (
            'Summarize Website'
          )}
        </button>

        {/* Progress Stepper */}
        {isLoading && (
          <div className="progress-stepper">
            <div className={`step ${progressStep >= 1 ? (progressStep > 1 ? 'done' : 'active') : ''}`}>
              <span className="step-dot"></span>
              Crawling
            </div>
            <span className={`step-connector ${progressStep > 1 ? 'done' : progressStep === 1 ? 'active' : ''}`}></span>
            <div className={`step ${progressStep >= 2 ? (progressStep > 2 ? 'done' : 'active') : ''}`}>
              <span className="step-dot"></span>
              Extracting
            </div>
            <span className={`step-connector ${progressStep > 2 ? 'done' : progressStep === 2 ? 'active' : ''}`}></span>
            <div className={`step ${progressStep >= 3 ? 'active' : ''}`}>
              <span className="step-dot"></span>
              Summarizing
            </div>
          </div>
        )}

        {/* Error Display */}
        {error && (
          <div className="error-container">
            <span className="error-icon">⚠</span>
            <span className="error-text">{error}</span>
          </div>
        )}

        {/* Summary Result */}
        {summary && (
          <div className="result-container" ref={resultRef}>
            <h3 className="result-title">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                <polyline points="14 2 14 8 20 8"></polyline>
                <line x1="16" y1="13" x2="8" y2="13"></line>
                <line x1="16" y1="17" x2="8" y2="17"></line>
                <polyline points="10 9 9 9 8 9"></polyline>
              </svg>
              Summary Result
              {isStreaming && <span className="streaming-indicator"></span>}
            </h3>
            <div className="result-content markdown-body">
              <ReactMarkdown>{summary}</ReactMarkdown>
            </div>
          </div>
        )}
      </div>

      <footer className="footer">
        <p>Developed by Aaditya Mittal</p>
      </footer>
    </div>
  );
}

export default App;
