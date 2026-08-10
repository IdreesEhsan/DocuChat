import React, { useState } from 'react';
import { useAuth } from './contexts/AuthContext';
import Login from './components/Login';
import UploadArea from './components/UploadArea';
import ChatInterface from './components/ChatInterface';

function App() {
  const { user, loading, logout } = useAuth();
  const [docUploaded, setDocUploaded] = useState(false);
  const [uploadStatus, setUploadStatus] = useState('');

  const handleUploadComplete = (data) => {
    setDocUploaded(true);
    setUploadStatus(`✅ Uploaded ${data.filename} — ${data.chunks_stored} chunks stored.`);
  };

  if (loading) return <div style={{ textAlign: 'center', marginTop: 50 }}>Loading...</div>;
  if (!user) return <Login />;

  return (
    <div style={{ maxWidth: 800, margin: '40px auto', padding: '0 20px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h1 style={{ fontSize: 36 }}>📄 DocuChat</h1>
        <button onClick={logout} style={{ padding: '8px 16px', background: '#dc3545', color: 'white', border: 'none', borderRadius: 4, cursor: 'pointer' }}>
          Logout
        </button>
      </div>
      <p style={{ color: '#666', marginBottom: 20 }}>Upload a document, then ask questions grounded in its content.</p>
      
      <UploadArea onUploadComplete={handleUploadComplete} />
      
      {uploadStatus && (
        <div style={{ padding: 12, backgroundColor: '#e6f7e6', borderRadius: 4, marginBottom: 20 }}>
          {uploadStatus}
        </div>
      )}
      
      {docUploaded && <ChatInterface />}
    </div>
  );
}

export default App;