import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
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

    // Playwright strictly requires http:// or https:// to work
    let finalUrl = url.trim();
    if (!finalUrl.startsWith('http://') && !finalUrl.startsWith('https://')) {
      finalUrl = 'https://' + finalUrl;
      setUrl(finalUrl); // Update the input box to show the user
    }

    setIsLoading(true);
    setError(null);
    setSummary(null);

    try {
      const response = await fetch('http://127.0.0.1:8000/summarize', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: finalUrl, scroll })
      });

      if (!response.ok) {
        throw new Error(`The Python backend crashed or returned an error (Status ${response.status})`);
      }

      const data = await response.json();
      setSummary(data.summary);
    } catch (err) {
      setError(`${err.message}. Check your Python terminal for the exact error!`);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app-container">
      <div className="glass-card">
        <h1>✨ AI Website Summarizer</h1>
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
              Analyzing Website...
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
