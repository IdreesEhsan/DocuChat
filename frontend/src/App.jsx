import React, { useState } from 'react';
import UploadArea from './components/UploadArea';
import ChatInterface from './components/ChatInterface';

function App() {
  const [docUploaded, setDocUploaded] = useState(false);
  const [uploadStatus, setUploadStatus] = useState('');

  const handleUploadComplete = (data) => {
    setDocUploaded(true);
    setUploadStatus(`✅ Uploaded ${data.filename} — ${data.chunks_stored} chunks stored.`);
  };

  return (
    <div style={{ maxWidth: '800px', margin: '40px auto', padding: '0 20px' }}>
      <h1 style={{ fontSize: '36px', marginBottom: '10px' }}>📄 DocuChat</h1>
      <p style={{ color: '#666', marginBottom: '30px' }}>Upload a document, then ask questions grounded in its content.</p>
      
      <UploadArea onUploadComplete={handleUploadComplete} />
      
      {uploadStatus && (
        <div style={{ padding: '12px', backgroundColor: '#e6f7e6', borderRadius: '4px', marginBottom: '20px' }}>
          {uploadStatus}
        </div>
      )}
      
      {docUploaded && <ChatInterface />}
    </div>
  );
}
export default App;