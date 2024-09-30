import React, { useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';

function App() {
  const [videoUrl, setVideoUrl] = useState(null);
  const [errorMessage, setErrorMessage] = useState('');

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      const formData = new FormData();
      formData.append('file', file);

      fetch('/upload', {
        method: 'POST',
        body: formData,
      })
        .then(response => response.json())
        .then(data => {
          if (data.message === 'File uploaded successfully') {
            setVideoUrl('/video_feed'); // URL to fetch video feed
            setErrorMessage(''); // Clear any previous error messages
          } else {
            setErrorMessage(data.message || 'Failed to upload file');
          }
        })
        .catch(error => {
          setErrorMessage('Error uploading file: ' + error.message);
          console.error('Error uploading file:', error);
        });
    }
  };

  return (
    <div className="container text-center mt-5">
      <h1 className="mb-4">Video File Processing</h1>

      {/* File upload */}
      <div className="form-group mb-4">
        <label htmlFor="videoUpload">Upload a Video File:</label>
        <input
          type="file"
          id="videoUpload"
          className="form-control-file"
          onChange={handleFileChange}
        />
      </div>

      {/* Video feed */}
      <div className="video-feed mb-4">
        {videoUrl ? (
          <img
            src={videoUrl}  // Video feed from Flask endpoint
            alt="Video Feed"
            className="img-fluid rounded"
            style={{ maxWidth: '100%' }}
          />
        ) : (
          <p className="text-muted">No video feed available</p>
        )}
      </div>

      {/* Error message display */}
      {errorMessage && <div className="alert alert-danger mt-4">{errorMessage}</div>}
    </div>
  );
}

export default App;
