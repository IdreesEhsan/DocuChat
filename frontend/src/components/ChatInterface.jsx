import React, { useState } from 'react';
import { streamChat } from '../services/api';

function ChatInterface() {
  const [query, setQuery] = useState('');
  const [answer, setAnswer] = useState('');
  const [sources, setSources] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;
    setAnswer('');
    setSources([]);
    setLoading(true);
    try {
      await streamChat(query, (event) => {
        if (event.type === 'sources') {
          setSources(event.data);
        } else if (event.type === 'text') {
          setAnswer(prev => prev + event.data);
        }
      });
    } catch (err) {
      setAnswer('Error: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ marginTop: '30px' }}>
      <h2>💬 Ask a question</h2>
      <form onSubmit={handleSubmit} style={{ display: 'flex', gap: '10px' }}>
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask about your documents..."
          style={{ flex: 1, padding: '10px', borderRadius: '4px', border: '1px solid #ccc' }}
        />
        <button type="submit" disabled={loading} style={{ padding: '10px 20px', borderRadius: '4px', border: 'none', background: '#007bff', color: 'white', cursor: 'pointer' }}>
          {loading ? 'Thinking...' : 'Ask'}
        </button>
      </form>
      
      <div style={{
        marginTop: '20px',
        padding: '16px',
        backgroundColor: '#f5f5f5',
        borderRadius: '8px',
        minHeight: '80px',
        whiteSpace: 'pre-wrap',
        border: '1px solid #e0e0e0'
      }}>
        {answer || 'Your answer will appear here...'}
      </div>

      {sources.length > 0 && (
        <div style={{ marginTop: '15px', padding: '12px', backgroundColor: '#e8f0fe', borderRadius: '8px', borderLeft: '4px solid #1a73e8' }}>
          <h4 style={{ margin: '0 0 8px 0', fontSize: '14px', color: '#1a73e8' }}>📚 Retrieved Sources</h4>
          {sources.map((src, idx) => (
            <div key={idx} style={{ fontSize: '13px', padding: '4px 0', borderBottom: '1px solid #d0e0f0' }}>
              <strong>{src.metadata.source}</strong> {src.metadata.page && `(Page ${src.metadata.page})`} 
              <span style={{ color: '#555', marginLeft: '8px' }}>— Similarity: {src.similarity}</span>
              <div style={{ color: '#444', fontSize: '12px', marginTop: '2px' }}>"{src.text}"</div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
export default ChatInterface;