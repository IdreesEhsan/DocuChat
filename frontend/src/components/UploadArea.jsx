import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { uploadFile } from '../services/api';

function UploadArea({ onUploadComplete }) {
  const onDrop = useCallback(async (acceptedFiles) => {
    if (acceptedFiles.length === 0) return;
    const file = acceptedFiles[0];
    try {
      const response = await uploadFile(file);
      onUploadComplete(response.data);
    } catch (err) {
      alert('Upload failed: ' + err.message);
    }
  }, [onUploadComplete]);
  
  const { getRootProps, getInputProps } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx']
    }
  });
  
  return (
    <div {...getRootProps()} style={{
      border: '2px dashed #ccc',
      borderRadius: '8px',
      padding: '40px 20px',
      textAlign: 'center',
      cursor: 'pointer',
      marginBottom: '20px',
      backgroundColor: '#fafafa'
    }}>
      <input {...getInputProps()} />
      <p style={{ fontSize: '18px' }}>📄 Drag & drop a PDF or DOCX here, or click to select</p>
      <p style={{ fontSize: '14px', color: '#888' }}>Supported: .pdf, .docx</p>
    </div>
  );
}
export default UploadArea;