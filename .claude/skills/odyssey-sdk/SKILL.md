---
name: odyssey-sdk
description: Explains how to use the Odyssey Javascript SDK.  
---


# Odyssey SDK Guide for Virtual Try-On MVP

## Table of Contents
- [Overview](#overview)
- [Installation](#installation)
- [Core Concepts](#core-concepts)
- [Authentication](#authentication)
- [The Odyssey Class](#the-odyssey-class)
- [React Integration](#react-integration)
- [Connection Lifecycle](#connection-lifecycle)
- [Stream Operations](#stream-operations)
- [Image-to-Video Capabilities](#image-to-video-capabilities)
- [Event Handling](#event-handling)
- [Recordings](#recordings)
- [TypeScript Types](#typescript-types)
- [Practical Examples](#practical-examples)

---

## Overview

Odyssey is an audio-visual intelligence platform powered by Odyssey-2 Pro, a general-purpose world model that enables real-time video generation with interactive capabilities. The JavaScript SDK (`@odysseyml/odyssey`) provides TypeScript/JavaScript developers the tools to build applications with continuous, interactive video simulations.

**Key Capabilities:**
- Real-time video streaming with interactive controls
- Image-to-video generation (perfect for virtual try-on)
- Dynamic content updates via text prompts
- Stream recording and retrieval
- React-specific hooks for seamless integration

---

## Installation

Install via your preferred package manager:

```bash
npm install @odysseyml/odyssey
```

Or alternatively:

```bash
yarn add @odysseyml/odyssey
pnpm add @odysseyml/odyssey
```

**Minimum Version:** `^1.0.0` for core functionality (including image-to-video support)

---

## Core Concepts

### What is Odyssey?

Odyssey is a **world model** that generates video content in real-time. Unlike traditional video APIs that render complete videos asynchronously, Odyssey provides:

1. **Interactive Streams** - Real-time generation with low latency
2. **Dynamic Updates** - Modify running streams with text prompts
3. **Image Conditioning** - Start generation from uploaded images

### Architecture Overview

```
┌─────────────┐
│  Your App   │
└──────┬──────┘
       │
       │ Odyssey SDK
       │
┌──────▼──────────────────┐
│   WebRTC Connection     │
│  (MediaStream API)      │
└──────┬──────────────────┘
       │
┌──────▼──────────────────┐
│  Odyssey Platform       │
│  (Video Generation)     │
└─────────────────────────┘
```

The SDK uses **WebRTC** to establish peer-to-peer connections, delivering video as a `MediaStream` object that can be attached to HTML `<video>` elements.

---

## Authentication

All API requests require an API key obtained from the Odyssey platform.

### Getting Your API Key

1. Sign up at the Odyssey platform
2. Navigate to your API settings
3. Generate a new API key (format: `ody_your_api_key_here`)

### Using the API Key

Pass your API key when initializing the Odyssey client:

```typescript
import { Odyssey } from '@odysseyml/odyssey';

const client = new Odyssey({
  apiKey: 'ody_your_api_key_here'
});
```

**Security Best Practices:**
- Never commit API keys to version control
- Use environment variables: `process.env.ODYSSEY_API_KEY`
- For frontend apps, implement a backend proxy to keep keys secure

---

## The Odyssey Class

The `Odyssey` class is the main interface for interacting with the platform.

### Constructor

```typescript
new Odyssey(config: ClientConfig)
```

**Parameters:**
- `config.apiKey` (string, required) - Your API key

**Example:**
```typescript
const client = new Odyssey({ apiKey: process.env.ODYSSEY_API_KEY });
```

### Core Methods

#### Connection Management

**`connect(handlers?: OdysseyEventHandlers): Promise<MediaStream>`**

Establishes a streaming session and returns the media stream.

```typescript
// Using async/await
const mediaStream = await client.connect();
videoElement.srcObject = mediaStream;

// Using callbacks
await client.connect({
  onConnected: (mediaStream) => {
    videoElement.srcObject = mediaStream;
  }
});
```

**`disconnect(): void`**

Terminates the session and releases resources.

```typescript
client.disconnect();
```

**`attachToVideo(videoElement: HTMLVideoElement): void`**

Convenience method to bind the stream to a video element.

```typescript
const videoEl = document.getElementById('video');
client.attachToVideo(videoEl);
```

#### Stream Operations

**`startStream(options?: StartStreamOptions): Promise<string>`**

Initiates video generation. Returns the stream ID.

```typescript
// Text-to-video
const streamId = await client.startStream({
  prompt: "A person trying on a red jacket",
  portrait: true  // Use portrait orientation
});

// Image-to-video (for virtual try-on)
const streamId = await client.startStream({
  prompt: "Person wearing the selected outfit",
  portrait: true,
  image: imageFile  // File object from <input type="file">
});
```

**Options:**
- `prompt` (string) - Text description of desired content
- `portrait` (boolean) - Orientation (true = portrait, false = landscape)
- `image` (File) - Optional image for image-to-video generation

**`interact(options: InteractOptions): Promise<void>`**

Sends prompts to modify the video in real-time.

```typescript
await client.interact({
  prompt: "Now try on blue jeans"
});
```

**`endStream(): Promise<void>`**

Closes the current stream session.

```typescript
await client.endStream();
```

#### Recording Access

**`getRecording(streamId: string): Promise<Recording>`**

Retrieves presigned URLs and metadata for a completed stream.

```typescript
const recording = await client.getRecording(streamId);
console.log(recording.video_url);  // Full MP4 video
console.log(recording.thumbnail_url);  // JPEG thumbnail
```

**`listStreamRecordings(options?: ListStreamRecordingsOptions): Promise<StreamRecordingsListResponse>`**

Lists all recordings with pagination.

```typescript
const recordings = await client.listStreamRecordings({
  limit: 50,
  offset: 0
});

console.log(recordings.total);  // Total count
console.log(recordings.recordings);  // Array of recordings
```

### Properties

All properties are read-only getters providing connection state:

- **`isConnected`** (boolean) - Whether client is connected
- **`currentStatus`** (ConnectionStatus) - Current connection state
- **`currentSessionId`** (string | null) - Active session identifier
- **`mediaStream`** (MediaStream | null) - The active video/audio stream
- **`connectionState`** (RTCPeerConnectionState | null) - WebRTC peer connection state
- **`iceConnectionState`** (RTCIceConnectionState | null) - ICE connection state

**Example:**
```typescript
if (client.isConnected) {
  console.log(`Session ID: ${client.currentSessionId}`);
  console.log(`Status: ${client.currentStatus}`);
}
```

---

## React Integration

The SDK provides a `useOdyssey` hook for React applications.

### useOdyssey Hook

```typescript
import { useOdyssey } from '@odysseyml/odyssey';

const client = useOdyssey({
  apiKey: process.env.REACT_APP_ODYSSEY_API_KEY,
  handlers: {
    onConnected: (mediaStream) => { /* handle connection */ },
    onError: (error, fatal) => { /* handle error */ }
  }
});
```

**Parameters:**
- `apiKey` (string, required) - Your API key
- `handlers` (UseOdysseyHandlers, optional) - Event callbacks

**Returns:** Client instance with:
- All Odyssey class methods
- `status` - Current connection state
- `error` - Error message (if any)
- `isConnected` - Boolean indicating readiness
- `mediaStream` - The active stream
- `sessionId` - Current session identifier

### React Component Example

```typescript
import { useOdyssey } from '@odysseyml/odyssey';
import { useEffect, useRef, useState } from 'react';

function VirtualTryOn() {
  const videoRef = useRef<HTMLVideoElement>(null);
  const [streamId, setStreamId] = useState<string | null>(null);

  const client = useOdyssey({
    apiKey: process.env.REACT_APP_ODYSSEY_API_KEY,
    handlers: {
      onConnected: (mediaStream) => {
        if (videoRef.current) {
          videoRef.current.srcObject = mediaStream;
        }
      },
      onStreamStarted: (id) => {
        setStreamId(id);
        console.log('Stream started:', id);
      },
      onError: (error, fatal) => {
        console.error('Error:', error, 'Fatal:', fatal);
      }
    }
  });

  useEffect(() => {
    // Connect on mount
    client.connect();

    // Cleanup on unmount
    return () => {
      client.disconnect();
    };
  }, []);

  const handleStartTryOn = async (imageFile: File) => {
    await client.startStream({
      prompt: "Person trying on the selected outfit",
      portrait: true,
      image: imageFile
    });
  };

  const handleChangeOutfit = async (description: string) => {
    await client.interact({
      prompt: description
    });
  };

  return (
    <div>
      <video ref={videoRef} autoPlay playsInline />
      <button
        onClick={() => handleStartTryOn(selectedImage)}
        disabled={!client.isConnected}
      >
        Start Try-On
      </button>
      <button onClick={() => handleChangeOutfit("Try on a red dress")}>
        Change Outfit
      </button>
    </div>
  );
}
```

### Lifecycle Best Practices

1. **Connect in useEffect:** Call `connect()` within a `useEffect` hook
2. **Cleanup:** Always call `disconnect()` in the cleanup function
3. **Disable UI:** Use `isConnected` to disable buttons until ready
4. **Error Handling:** Implement `onError` handler for user feedback

---

## Connection Lifecycle

Understanding the connection lifecycle is crucial for building robust applications.

### Connection States

The `ConnectionStatus` type has the following states:

```typescript
type ConnectionStatus =
  | 'authenticating'  // Validating API key
  | 'connecting'      // Establishing WebRTC connection
  | 'reconnecting'    // Attempting to reconnect after failure
  | 'connected'       // Ready for streaming
  | 'disconnected'    // Not connected
  | 'failed'          // Connection failed
```

### State Flow Diagram

```
┌──────────────┐
│ disconnected │
└──────┬───────┘
       │ connect()
       ▼
┌──────────────┐
│authenticating│
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  connecting  │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  connected   │ ◄─────┐
└──────┬───────┘       │
       │               │
       ▼               │
┌──────────────┐       │
│reconnecting  │───────┘
└──────┬───────┘
       │
       ▼
┌──────────────┐
│    failed    │
└──────────────┘
```

### Monitoring State Changes

Use the `onStatusChange` handler to track state transitions:

```typescript
client.connect({
  onStatusChange: (status, message) => {
    console.log(`Status: ${status}`, message);

    switch(status) {
      case 'authenticating':
        // Show loading indicator
        break;
      case 'connected':
        // Enable UI controls
        break;
      case 'failed':
        // Show error message
        break;
    }
  }
});
```

---

## Stream Operations

Streams are the core of interactive video generation in Odyssey.

### Stream Lifecycle

1. **Connect** - Establish WebRTC connection
2. **Start Stream** - Begin video generation
3. **Interact** (optional) - Send prompts to modify content
4. **End Stream** - Stop generation
5. **Retrieve Recording** - Access the final video

### Starting a Stream

**Text-to-Video:**
```typescript
const streamId = await client.startStream({
  prompt: "A fashion model walking down a runway",
  portrait: false  // Landscape mode
});
```

**Image-to-Video (Virtual Try-On Use Case):**
```typescript
// Get image from file input
const fileInput = document.getElementById('imageUpload');
const imageFile = fileInput.files[0];

const streamId = await client.startStream({
  prompt: "Person trying on a designer jacket",
  portrait: true,
  image: imageFile
});
```

### Interactive Prompts

Send real-time updates to modify the stream:

```typescript
// User clicks "Try Blue Shirt"
await client.interact({
  prompt: "Now wearing a blue button-up shirt"
});

// User clicks "Add Sunglasses"
await client.interact({
  prompt: "Same outfit but now wearing aviator sunglasses"
});
```

**Best Practices:**
- Keep prompts concise and specific
- Wait for `onInteractAcknowledged` before sending another prompt
- Use descriptive language for better results

### Ending a Stream

```typescript
await client.endStream();
```

This triggers the `onStreamEnded` callback and makes the recording available.

---

## Image-to-Video Capabilities

Image-to-video is essential for virtual try-on applications. It allows you to start generation from a user's photo.

### Supported Formats

- JPEG
- PNG
- WebP
- GIF
- BMP
- HEIC
- HEIF
- AVIF

### Size Constraints

- **Maximum file size:** 25MB
- **Automatic resizing:** Images are resized to:
  - `1280×704` (landscape)
  - `704×1280` (portrait)

### Implementation

```typescript
// HTML
<input
  type="file"
  id="userPhoto"
  accept="image/jpeg,image/png,image/webp"
/>

// JavaScript
const handleImageUpload = async (event) => {
  const file = event.target.files[0];

  // Validate file
  if (!file) return;
  if (file.size > 25 * 1024 * 1024) {
    alert('File too large. Maximum 25MB.');
    return;
  }

  // Start image-to-video stream
  await client.startStream({
    prompt: "Person wearing a red evening gown",
    portrait: true,
    image: file
  });
};

document.getElementById('userPhoto')
  .addEventListener('change', handleImageUpload);
```

### Virtual Try-On Flow

```typescript
// 1. User uploads their photo
const userPhoto = await getUserPhoto();

// 2. Start stream with their image
const streamId = await client.startStream({
  prompt: "Person in casual attire",
  portrait: true,
  image: userPhoto
});

// 3. Let them try different outfits
await client.interact({ prompt: "Wearing a black leather jacket" });
await client.interact({ prompt: "Now in a formal business suit" });
await client.interact({ prompt: "In a summer dress" });

// 4. End stream and retrieve recording
await client.endStream();
const recording = await client.getRecording(streamId);

// 5. Let user download or share
window.open(recording.video_url);
```

---

## Event Handling

The SDK uses an event-driven architecture for lifecycle management.

### OdysseyEventHandlers

All event handlers are optional and can be passed to `connect()`:

```typescript
interface OdysseyEventHandlers {
  onConnected?: (mediaStream: MediaStream) => void;
  onDisconnected?: () => void;
  onStreamStarted?: (streamId: string) => void;
  onStreamEnded?: () => void;
  onInteractAcknowledged?: (prompt: string) => void;
  onStreamError?: (reason: string, message: string) => void;
  onError?: (error: Error, fatal: boolean) => void;
  onStatusChange?: (status: ConnectionStatus, message?: string) => void;
}
```

### Event Descriptions

**`onConnected(mediaStream: MediaStream)`**

Called when the video stream is established. This is where you attach the stream to your video element.

```typescript
onConnected: (mediaStream) => {
  videoElement.srcObject = mediaStream;
  videoElement.play();
}
```

**`onDisconnected()`**

Triggered when the video connection closes.

```typescript
onDisconnected: () => {
  videoElement.srcObject = null;
  console.log('Disconnected from Odyssey');
}
```

**`onStreamStarted(streamId: string)`**

Fired when an interactive stream is ready. Save this ID to retrieve recordings later.

```typescript
onStreamStarted: (streamId) => {
  console.log('Stream ID:', streamId);
  localStorage.setItem('lastStreamId', streamId);
}
```

**`onStreamEnded()`**

Triggered when the stream completes.

```typescript
onStreamEnded: () => {
  console.log('Stream ended. Recording available.');
}
```

**`onInteractAcknowledged(prompt: string)`**

Called when an interaction is processed by the server.

```typescript
onInteractAcknowledged: (prompt) => {
  console.log('Processing:', prompt);
  setLoading(false);
}
```

**`onStreamError(reason: string, message: string)`**

Handles stream-specific errors (non-fatal). You can recover by calling `endStream()` and starting a new stream.

```typescript
onStreamError: (reason, message) => {
  console.error('Stream error:', reason, message);
  alert(`Stream error: ${message}`);
  // Optionally restart
  client.endStream();
}
```

**`onError(error: Error, fatal: boolean)`**

General error handler.

```typescript
onError: (error, fatal) => {
  console.error('Error:', error.message, 'Fatal:', fatal);

  if (fatal) {
    // Reconnection required
    alert('Connection lost. Please reconnect.');
    client.disconnect();
  } else {
    // Show warning, continue operation
    showWarning(error.message);
  }
}
```

**`onStatusChange(status: ConnectionStatus, message?: string)`**

Monitors connection state transitions.

```typescript
onStatusChange: (status, message) => {
  updateStatusIndicator(status);

  if (status === 'connected') {
    enableControls();
  } else if (status === 'failed') {
    showErrorScreen(message);
  }
}
```

### Error Handling Strategy

```typescript
const errorHandlingStrategy = {
  onError: (error, fatal) => {
    if (fatal) {
      // Fatal errors require reconnection
      client.disconnect();
      showReconnectButton();
    } else {
      // Non-fatal: log and continue
      logError(error);
      showToast(error.message);
    }
  },

  onStreamError: (reason, message) => {
    // Stream-specific errors: recoverable
    client.endStream();

    if (reason === 'content_policy') {
      showMessage('Content not allowed. Please try different input.');
    } else {
      showMessage('Stream error. Please try again.');
    }
  }
};

await client.connect(errorHandlingStrategy);
```

---

## Recordings

Every stream session can be recorded and retrieved for later use.

### Capturing Stream IDs

Save the stream ID from `onStreamStarted`:

```typescript
let currentStreamId: string | null = null;

await client.connect({
  onStreamStarted: (streamId) => {
    currentStreamId = streamId;
    console.log('Recording stream:', streamId);
  }
});
```

### Retrieving Recordings

After a stream ends, retrieve the recording:

```typescript
const recording = await client.getRecording(currentStreamId);

console.log({
  video: recording.video_url,      // Full MP4 video
  thumbnail: recording.thumbnail_url,  // JPEG thumbnail
  preview: recording.preview_url,   // MP4 preview
  events: recording.events_url,     // JSONL event log
  duration: recording.duration_seconds,
  frames: recording.frame_count
});
```

### Recording Object Structure

```typescript
interface Recording {
  stream_id: string;
  video_url: string | null;        // Presigned URL (expires ~1 hour)
  events_url: string | null;       // Event log in JSONL format
  thumbnail_url: string | null;    // JPEG thumbnail
  preview_url: string | null;      // Short preview video
  frame_count: number | null;
  duration_seconds: number | null;
}
```

### Listing All Recordings

```typescript
const response = await client.listStreamRecordings({
  limit: 50,
  offset: 0
});

console.log(`Total recordings: ${response.total}`);

response.recordings.forEach(rec => {
  console.log(`Stream ${rec.stream_id}:`);
  console.log(`  Duration: ${rec.duration_seconds}s`);
  console.log(`  Size: ${rec.width}x${rec.height}`);
  console.log(`  Created: ${rec.created_at}`);
});
```

### Pagination Example

```typescript
const getAllRecordings = async () => {
  const allRecordings = [];
  let offset = 0;
  const limit = 100; // Maximum allowed

  while (true) {
    const response = await client.listStreamRecordings({ limit, offset });
    allRecordings.push(...response.recordings);

    if (allRecordings.length >= response.total) {
      break;
    }

    offset += limit;
  }

  return allRecordings;
};
```

### Parsing Event Logs

Events are stored in JSONL format (JSON Lines):

```typescript
const recording = await client.getRecording(streamId);

// Fetch the events file
const eventsResponse = await fetch(recording.events_url);
const eventsText = await eventsResponse.text();

// Parse JSONL (one JSON object per line)
const events = eventsText
  .split('\n')
  .filter(line => line.trim())
  .map(line => JSON.parse(line));

console.log(events);
// Example events:
// { type: 'stream_started', timestamp: 1234567890 }
// { type: 'interact', prompt: 'wearing red jacket', timestamp: 1234567895 }
// { type: 'stream_ended', timestamp: 1234567900 }
```

### Building a Recording Gallery

```typescript
function RecordingGallery() {
  const [recordings, setRecordings] = useState([]);
  const client = useOdyssey({ apiKey: API_KEY });

  useEffect(() => {
    const loadRecordings = async () => {
      const response = await client.listStreamRecordings({ limit: 20 });
      setRecordings(response.recordings);
    };

    loadRecordings();
  }, []);

  return (
    <div className="gallery">
      {recordings.map(rec => (
        <div key={rec.stream_id} className="recording-card">
          <img src={rec.thumbnail_url} alt="Thumbnail" />
          <p>{rec.duration_seconds}s</p>
          <button onClick={() => window.open(rec.video_url)}>
            Watch
          </button>
        </div>
      ))}
    </div>
  );
}
```

---

## TypeScript Types

The SDK is fully typed. Here are the key types you'll use:

### Configuration Types

```typescript
interface ClientConfig {
  apiKey: string;
}

interface UseOdysseyOptions {
  apiKey: string;
  handlers?: UseOdysseyHandlers;
}
```

### Stream Options

```typescript
interface StartStreamOptions {
  prompt?: string;
  portrait?: boolean;
  image?: File;
}

interface InteractOptions {
  prompt: string;
}
```

### Connection Status

```typescript
type ConnectionStatus =
  | 'authenticating'
  | 'connecting'
  | 'reconnecting'
  | 'connected'
  | 'disconnected'
  | 'failed';
```

### Event Handlers

```typescript
interface OdysseyEventHandlers {
  onConnected?: (mediaStream: MediaStream) => void;
  onDisconnected?: () => void;
  onStreamStarted?: (streamId: string) => void;
  onStreamEnded?: () => void;
  onInteractAcknowledged?: (prompt: string) => void;
  onStreamError?: (reason: string, message: string) => void;
  onError?: (error: Error, fatal: boolean) => void;
  onStatusChange?: (status: ConnectionStatus, message?: string) => void;
}

type UseOdysseyHandlers = OdysseyEventHandlers;
```

### Recording Types

```typescript
interface Recording {
  stream_id: string;
  video_url: string | null;
  events_url: string | null;
  thumbnail_url: string | null;
  preview_url: string | null;
  frame_count: number | null;
  duration_seconds: number | null;
}

interface StreamRecordingSummary {
  stream_id: string;
  width: number;
  height: number;
  duration_seconds: number;
  created_at: string;
  thumbnail_url: string | null;
}

interface ListStreamRecordingsOptions {
  limit?: number;  // Default: 50, Max: 100
  offset?: number; // Default: 0
}

interface StreamRecordingsListResponse {
  recordings: StreamRecordingSummary[];
  total: number;
  limit: number;
  offset: number;
}
```

### Simulation Types

```typescript
type SimulationJobStatus =
  | 'pending'
  | 'running'
  | 'completed'
  | 'failed'
  | 'cancelled';

interface ScriptEntry {
  timestamp_ms: number;
  start?: { prompt: string; portrait?: boolean; image?: File };
  interact?: { prompt: string };
  end?: {};
}

interface SimulateOptions {
  script: ScriptEntry[];
  portrait?: boolean;
}

interface SimulationStream {
  stream_id: string;
  status: SimulationJobStatus;
  error_message?: string;
}

interface SimulationJob {
  job_id: string;
  status: SimulationJobStatus;
  priority: number;
  estimated_wait_seconds?: number;
  created_at: string;
  updated_at: string;
}

interface SimulationJobDetail extends SimulationJob {
  streams: SimulationStream[];
  started_at?: string;
  completed_at?: string;
}
```

---

## Practical Examples
See examples.md
---

## Summary

This guide covered the essential concepts for building a virtual try-on MVP with the Odyssey SDK:

1. **Installation & Setup** - Installing the package and configuring authentication
2. **Core Architecture** - Understanding the WebRTC-based streaming model
3. **Odyssey Class** - The main interface for all operations
4. **React Integration** - Using the `useOdyssey` hook for React apps
5. **Connection Lifecycle** - Managing connection states and transitions
6. **Stream Operations** - Starting, interacting with, and ending streams
7. **Image-to-Video** - Essential for virtual try-on use cases
8. **Event Handling** - Responding to lifecycle events
9. **Recordings** - Retrieving and managing stream recordings
10. **TypeScript Types** - Leveraging full type safety

### Next Steps

1. Obtain an API key from the Odyssey platform
2. Set up a basic React project with the SDK installed
3. Build a simple component that connects and displays video
4. Add image upload and try-on functionality
5. Implement recording retrieval for user downloads

### Additional Resources

- Odyssey Documentation: https://documentation.api.odyssey.ml
- Discord Community: Join for support and updates
- API License Agreement: Review terms of use

Happy building!
