Examples on how to use the javascript sdk

### Example 1: Basic Vanilla JavaScript

```html
<!DOCTYPE html>
<html>
<head>
  <title>Odyssey Basic Example</title>
</head>
<body>
  <video id="video" autoplay playsinline></video>
  <div id="status">Disconnected</div>

  <button id="connect">Connect</button>
  <button id="start">Start Stream</button>
  <button id="interact">Change Scene</button>
  <button id="end">End Stream</button>

  <script type="module">
    import { Odyssey } from '@odysseyml/odyssey';

    const client = new Odyssey({ apiKey: 'ody_your_api_key_here' });
    const videoEl = document.getElementById('video');
    const statusEl = document.getElementById('status');

    // Connect
    document.getElementById('connect').onclick = async () => {
      await client.connect({
        onConnected: (mediaStream) => {
          videoEl.srcObject = mediaStream;
          statusEl.textContent = 'Connected';
        },
        onStatusChange: (status) => {
          statusEl.textContent = status;
        }
      });
    };

    // Start stream
    document.getElementById('start').onclick = async () => {
      await client.startStream({
        prompt: "A person walking in a park",
        portrait: true
      });
    };

    // Interact
    document.getElementById('interact').onclick = async () => {
      await client.interact({
        prompt: "Now walking on a beach at sunset"
      });
    };

    // End stream
    document.getElementById('end').onclick = async () => {
      await client.endStream();
    };
  </script>
</body>
</html>
```

### Example 2: React Virtual Try-On Component

```typescript
import React, { useEffect, useRef, useState } from 'react';
import { useOdyssey } from '@odysseyml/odyssey';

interface Outfit {
  id: string;
  name: string;
  prompt: string;
}

const outfits: Outfit[] = [
  { id: '1', name: 'Red Dress', prompt: 'wearing an elegant red evening dress' },
  { id: '2', name: 'Blue Suit', prompt: 'wearing a navy blue business suit' },
  { id: '3', name: 'Casual Jeans', prompt: 'wearing blue jeans and white t-shirt' },
];

function VirtualTryOn() {
  const videoRef = useRef<HTMLVideoElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const [userPhoto, setUserPhoto] = useState<File | null>(null);
  const [streamId, setStreamId] = useState<string | null>(null);
  const [isStreaming, setIsStreaming] = useState(false);

  const client = useOdyssey({
    apiKey: process.env.REACT_APP_ODYSSEY_API_KEY!,
    handlers: {
      onConnected: (mediaStream) => {
        if (videoRef.current) {
          videoRef.current.srcObject = mediaStream;
        }
      },
      onStreamStarted: (id) => {
        setStreamId(id);
        setIsStreaming(true);
      },
      onStreamEnded: () => {
        setIsStreaming(false);
      },
      onError: (error, fatal) => {
        console.error('Error:', error, 'Fatal:', fatal);
        alert(`Error: ${error.message}`);
      }
    }
  });

  useEffect(() => {
    client.connect();
    return () => client.disconnect();
  }, []);

  const handlePhotoUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      if (file.size > 25 * 1024 * 1024) {
        alert('File too large. Maximum 25MB.');
        return;
      }
      setUserPhoto(file);
    }
  };

  const handleStartTryOn = async () => {
    if (!userPhoto) {
      alert('Please upload a photo first');
      return;
    }

    await client.startStream({
      prompt: "Person in neutral clothing",
      portrait: true,
      image: userPhoto
    });
  };

  const handleTryOutfit = async (outfit: Outfit) => {
    if (!isStreaming) {
      alert('Please start a try-on session first');
      return;
    }

    await client.interact({
      prompt: outfit.prompt
    });
  };

  const handleEndSession = async () => {
    await client.endStream();

    if (streamId) {
      // Retrieve and download recording
      const recording = await client.getRecording(streamId);
      if (recording.video_url) {
        window.open(recording.video_url, '_blank');
      }
    }
  };

  return (
    <div className="virtual-tryon">
      <h1>Virtual Try-On</h1>

      <div className="video-container">
        <video
          ref={videoRef}
          autoPlay
          playsInline
          muted
          className="preview-video"
        />
        <div className="status">
          {client.isConnected ? '🟢 Connected' : '🔴 Disconnected'}
        </div>
      </div>

      <div className="controls">
        <input
          ref={fileInputRef}
          type="file"
          accept="image/*"
          onChange={handlePhotoUpload}
          style={{ display: 'none' }}
        />

        <button
          onClick={() => fileInputRef.current?.click()}
          disabled={isStreaming}
        >
          📷 Upload Photo
        </button>

        <button
          onClick={handleStartTryOn}
          disabled={!client.isConnected || !userPhoto || isStreaming}
        >
          ▶️ Start Try-On
        </button>

        <button
          onClick={handleEndSession}
          disabled={!isStreaming}
        >
          ⏹️ End & Download
        </button>
      </div>

      {userPhoto && (
        <div className="photo-preview">
          <img
            src={URL.createObjectURL(userPhoto)}
            alt="Your photo"
            style={{ maxWidth: '200px' }}
          />
        </div>
      )}

      <div className="outfits">
        <h2>Try These Outfits</h2>
        <div className="outfit-grid">
          {outfits.map(outfit => (
            <button
              key={outfit.id}
              onClick={() => handleTryOutfit(outfit)}
              disabled={!isStreaming}
              className="outfit-button"
            >
              {outfit.name}
            </button>
          ))}
        </div>
      </div>

      {streamId && (
        <div className="stream-info">
          Stream ID: <code>{streamId}</code>
        </div>
      )}
    </div>
  );
}

export default VirtualTryOn;
```

### Example 3: Error Handling & Reconnection

```typescript
import { Odyssey, ConnectionStatus } from '@odysseyml/odyssey';
import { useState, useEffect } from 'react';

function RobustOdysseyClient() {
  const [client] = useState(() =>
    new Odyssey({ apiKey: process.env.ODYSSEY_API_KEY })
  );
  const [status, setStatus] = useState<ConnectionStatus>('disconnected');
  const [error, setError] = useState<string | null>(null);
  const [shouldReconnect, setShouldReconnect] = useState(false);

  const connect = async () => {
    setError(null);

    try {
      await client.connect({
        onStatusChange: (newStatus, message) => {
          setStatus(newStatus);
          console.log(`Status: ${newStatus}`, message);
        },

        onError: (err, fatal) => {
          setError(err.message);

          if (fatal) {
            console.error('Fatal error:', err);
            setShouldReconnect(true);
          } else {
            console.warn('Non-fatal error:', err);
          }
        },

        onStreamError: (reason, message) => {
          console.error('Stream error:', reason, message);
          setError(`Stream error: ${message}`);
        }
      });
    } catch (err) {
      setError(err.message);
      setShouldReconnect(true);
    }
  };

  const disconnect = () => {
    client.disconnect();
    setStatus('disconnected');
    setShouldReconnect(false);
  };

  // Auto-reconnect logic
  useEffect(() => {
    if (shouldReconnect && status === 'disconnected') {
      const timeout = setTimeout(() => {
        console.log('Attempting reconnection...');
        connect();
      }, 3000);

      return () => clearTimeout(timeout);
    }
  }, [shouldReconnect, status]);

  return (
    <div>
      <div className="status-bar">
        Status: {status}
        {error && <span className="error">{error}</span>}
      </div>

      <button onClick={connect} disabled={status === 'connected'}>
        Connect
      </button>
      <button onClick={disconnect} disabled={status === 'disconnected'}>
        Disconnect
      </button>

      {shouldReconnect && (
        <div className="reconnect-notice">
          Attempting to reconnect...
        </div>
      )}
    </div>
  );
}
```

### Example 4: Recording Gallery with Pagination

```typescript
import { useOdyssey } from '@odysseyml/odyssey';
import { useState, useEffect } from 'react';

function RecordingGallery() {
  const client = useOdyssey({ apiKey: process.env.REACT_APP_ODYSSEY_API_KEY });
  const [recordings, setRecordings] = useState([]);
  const [total, setTotal] = useState(0);
  const [offset, setOffset] = useState(0);
  const [loading, setLoading] = useState(false);

  const limit = 20;

  const loadRecordings = async () => {
    setLoading(true);
    try {
      const response = await client.listStreamRecordings({ limit, offset });
      setRecordings(response.recordings);
      setTotal(response.total);
    } catch (err) {
      console.error('Failed to load recordings:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadRecordings();
  }, [offset]);

  const handlePrevious = () => {
    setOffset(Math.max(0, offset - limit));
  };

  const handleNext = () => {
    if (offset + limit < total) {
      setOffset(offset + limit);
    }
  };

  if (loading) return <div>Loading...</div>;

  return (
    <div className="recording-gallery">
      <h2>Your Try-On Sessions</h2>
      <p>Total recordings: {total}</p>

      <div className="gallery-grid">
        {recordings.map(rec => (
          <div key={rec.stream_id} className="recording-card">
            <img
              src={rec.thumbnail_url}
              alt={`Recording ${rec.stream_id}`}
            />
            <div className="recording-info">
              <p>{rec.duration_seconds}s</p>
              <p>{rec.width}×{rec.height}</p>
              <p>{new Date(rec.created_at).toLocaleDateString()}</p>
            </div>
            <button
              onClick={async () => {
                const recording = await client.getRecording(rec.stream_id);
                window.open(recording.video_url, '_blank');
              }}
            >
              Watch
            </button>
          </div>
        ))}
      </div>

      <div className="pagination">
        <button
          onClick={handlePrevious}
          disabled={offset === 0}
        >
          Previous
        </button>
        <span>
          Page {Math.floor(offset / limit) + 1} of {Math.ceil(total / limit)}
        </span>
        <button
          onClick={handleNext}
          disabled={offset + limit >= total}
        >
          Next
        </button>
      </div>
    </div>
  );
}
```
