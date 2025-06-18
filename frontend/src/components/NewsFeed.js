import { useState, useEffect, useCallback } from 'react';
import axios from 'axios';

const TOPICS = [
  "All Topics",
  "Technology & Computing",
  "Business & Finance",
  "Politics & Government", 
  "Science & Research",
  "Health & Medicine",
  "General News"
];

export default function NewsFeed() {
  const [news, setNews] = useState([]);
  const [loading, setLoading] = useState(false);
  const [activeTopic, setActiveTopic] = useState("All Topics")

// Wraping fetchNews in useCallback to prevent recreation on every render
  const fetchNews = useCallback ( async () => {
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:8000/news', {
        category: "general",
        page_size: 20  // Fetch 20 headlines at a time
      });
      setNews(response.data.results);
    } catch (error) {
      console.error("Failed to fetch news:", error);
    } finally {
      setLoading(false);
    }
  }, []); // Only recreate when category changes

  // Debounce rapid category changes
useEffect(() => {
  const timer = setTimeout(() => fetchNews(), 300);
  return () => clearTimeout(timer);
}, [fetchNews]);

const filteredNews = news.filter(item =>
    activeTopic === "All Topics" || item.topic === activeTopic
);
  return (
    <div className="news-container">
      <h1>AI Powered News Aggregator</h1>
      
      <div className="controls">
        <select 
          value={activeTopic} 
          onChange={(e) => setActiveTopic(e.target.value)}
        >
          {TOPICS.map(topic =>(
            <option key={topic} value={topic}>{topic}</option>
          ))}
        </select>
      </div>

       {loading ? (
        <div className="skeleton-loader">
          {[...Array(5)].map((_, i) => (
            <div key={i} className="skeleton-item" />
          ))}
        </div>
      ): (
      <div className="news-list">
        {filteredNews.map((item, index) => (
<div key={index} className="news-card">
            <h3>{item.headline}</h3>
            <p className={`topic-badge ${item.topic.toLowerCase().replace(/\s+/g, '-')}`}>
              {item.topic} 
              <span className='confidence'>({item.confidence})</span>
            </p>
          </div>
          
        ))}
      </div>
      )}
    </div>
  );
}