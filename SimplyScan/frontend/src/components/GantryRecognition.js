import React, { useEffect, useState } from 'react';

function GantryRecognition() {
  const [recognitionResult, setRecognitionResult] = useState(null);

  useEffect(() => {
    // Open WebSocket connection
    const socket = new WebSocket('wss://your-websocket-url.com');
    
    // Handle incoming messages
    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setRecognitionResult(data.result);  // Assuming the result is in the `data.result`
    };

    // Close WebSocket connection when component unmounts
    return () => {
      socket.close();
    };
  }, []);

  return (
    <div className="recognition-result">
      <h2>Gantry Recognition Status</h2>
      {recognitionResult ? (
        <p>Recognition Result: {recognitionResult}</p>
      ) : (
        <p>Waiting for recognition...</p>
      )}
    </div>
  );
}

export default GantryRecognition;
