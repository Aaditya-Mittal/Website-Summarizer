import React, { useState } from 'react';
import './index.css';

function App() {
  const [url, setUrl] = useState('');
  const [scroll, setScroll] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [summary, setSummary] = useState(null);
  const [error, setError] = useState(null);

  const handleSummarize = async () => {
    if (!url) {
      setError('Please enter a valid URL.');
      return;
    }

    setIsLoading(true);
    setError(null);
    setSummary(null);

    try {
      const response = await fetch('http://127.0.0.1:8000/summarize', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url, scroll })
      });

      if (!response.ok) {
        throw new Error('Failed to fetch from the server');
      }

      const data = await response.json();
      setSummary(data.summary);
    } catch (err) {
      setError('Failed to connect to the backend. The FastAPI server may not be running.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app-container">
      <div className="glass-card">
        <h1>✨ AI Web Crawler</h1>
        <p className="subtitle">Extract and summarize knowledge from any website in seconds.</p>

        <div className="input-group">
          <input
            type="text"
            placeholder="https://example.com"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && !isLoading && handleSummarize()}
          />
        </div>

        <label className="checkbox-group">
          <input
            type="checkbox"
            checked={scroll}
            onChange={(e) => setScroll(e.target.checked)}
          />
          Enable Scroll Engine (Catches lazy-loaded content)
        </label>

        <button
          className="summarize-btn"
          onClick={handleSummarize}
          disabled={isLoading}
        >
          {isLoading ? (
            <div className="loading-text">
              <span className="loader"></span>
              Crawling Pages...
            </div>
          ) : (
            'Summarize Website'
          )}
        </button>

        {error && (
          <div className="result-container" style={{ borderColor: 'rgba(239, 68, 68, 0.3)' }}>
            <h3 className="result-title" style={{ color: '#ef4444' }}>Error</h3>
            <p className="result-content">{error}</p>
          </div>
        )}

        {summary && (
          <div className="result-container">
            <h3 className="result-title">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                <polyline points="14 2 14 8 20 8"></polyline>
                <line x1="16" y1="13" x2="8" y2="13"></line>
                <line x1="16" y1="17" x2="8" y2="17"></line>
                <polyline points="10 9 9 9 8 9"></polyline>
              </svg>
              Summary Result
            </h3>
            <div className="result-content">{summary}</div>
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
