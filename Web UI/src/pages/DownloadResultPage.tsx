import React, { useEffect, useState } from 'react';

interface DownloadResultProps {
  zipBlob: Blob;  // URL for the ZIP file
  zipFileName?: string; // Optional: Custom name for the downloaded ZIP file
}

const DownloadResult: React.FC<DownloadResultProps> = ({ zipBlob, zipFileName = 'results.zip' }) => {
  // Handle download button click
  const handleDownload = () => {
    if (zipBlob) {
      const url = window.URL.createObjectURL(zipBlob);
      const a = document.createElement('a');
      a.href = url;
      a.download = zipFileName;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
    }
  };

  return (
    <div id="download_page" style={{ textAlign: 'center', margin: '20px' }}>
      <img src="waveform-icon.svg" alt="SoundWave"/>
      <button
        onClick={handleDownload}
        disabled={!zipBlob}
      >
        {zipBlob ? 'Download ZIP' : 'Loading...'}
      </button>
    </div>
  );
};

export default DownloadResult;

