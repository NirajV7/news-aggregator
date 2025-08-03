import { useState, useEffect, useCallback } from 'react';
import axios from 'axios';

const TOPICS = [
  "All Topics",
  "Technology & Computing",
  "Business & Finance",
  "Politics & Government", 
  "Science & Research",
  "Health & Medicine",
  "Entertainment & Celebrities",
  "Sports & Athletics",
  "General News"
];

export default function NewsFeed() {
  // Add darkmode state ( default to users OS preference)
  const [darkMode, setDarkMode] = useState(()=>{
    return window.matchMedia('(prefers-color-scheme: dark)').matches || localStorage.getItem('darkMode') === 'true';
  }); 
  const [news, setNews] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [activeTopic, setActiveTopic] = useState("All Topics");
  const [lastUpdated, setLastUpdated] = useState(null);
  //Toggle function
  const toggleDarkMode = () => {
    const newMode = !darkMode;
    setDarkMode(newMode);
    localStorage.setItem('darkMode', newMode);
  };
  //Apply class to body
  useEffect(() => {
    document.body.className = darkMode ? 'darkmode' : 'light-mode';
  },[darkMode]);
  // Fetch news only when explicitly called (initial load or manual refresh)
  const fetchNews = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.post(`${process.env.REACT_APP_BACKEND_URL}/news`, {
        category: "general",
        page_size: 20
      });
      setNews(response.data.results);
      setLastUpdated(new Date());
    } catch (err) {
      console.error("Failed to fetch news:", err);
      setError({
        message: err.response?.data?.detail || "Failed to load news",
        retryable: !err.response || err.response.status >= 500
      });
    } finally {
      setLoading(false);
    }
  }, []);

  // Initial load
  useEffect(() => {
    fetchNews();
  }, [fetchNews]);

  // Filter news client-side without API call
  const filteredNews = news.filter(item =>
    activeTopic === "All Topics" || item.topic === activeTopic
  );

  return (
    <div className={`news-container ${darkMode ? 'dark' : ''}`}>
      <header>
        <h1>AI Powered News Aggregator</h1>
        {lastUpdated && (
          <p className="subtitle">
            Last updated: {lastUpdated.toLocaleTimeString()}
          </p>
        )}
      </header>
       {/* Add toggle button near your controls */}
      <div className="controls">
        {/* ... existing controls ... */}
        <button 
          onClick={toggleDarkMode}
          className="dark-mode-toggle"
          aria-label={darkMode ? 'Switch to light mode' : 'Switch to dark mode'}
        >
          {darkMode ? '☀️' : '🌙'}
        </button>
      </div>
      <div className="controls">
        <select 
          value={activeTopic}
          onChange={(e) => setActiveTopic(e.target.value)}
          disabled={loading}
        >
          {TOPICS.map(topic => (
            <option key={topic} value={topic}>{topic}</option>
          ))}
        </select>
        
        <button 
          onClick={fetchNews}
          disabled={loading}
          className="refresh-btn"
        >
          {loading ? 'Refreshing...' : 'Refresh News'}
        </button>
      </div>

      {error ? (
        <div className="error-message">
          <p>{error.message}</p>
          <button onClick={fetchNews} className="retry-btn">
            Retry
          </button>
        </div>
      ) : loading ? (
        <div className="skeleton-loader">
          {[...Array(5)].map((_, i) => (
            <div key={i} className="skeleton-item" />
          ))}
        </div>
      ) : filteredNews.length === 0 ? (
        <div className="no-results">
          <p>No news found for this topic.</p>
          <button onClick={fetchNews}>Try refreshing</button>
        </div>
      ) : (
        <div className="news-list">
          {filteredNews.map((item) => (
            <div key={`${item.headline}-${item.url}`} className="news-card">
              <h3>
                <a href={item.url} target="_blank" rel="noopener noreferrer">
                  {item.headline}
                </a>
              </h3>
              <div className="meta">
                <span className={`topic-badge ${item.topic.toLowerCase().replace(/\s+/g, '-')}`}>
                  {item.topic}
                  <span className="confidence">({item.confidence})</span>
                </span>
                <span className="source">{item.source}</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
