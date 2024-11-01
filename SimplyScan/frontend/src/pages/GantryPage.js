import React, { useRef, useEffect, useState } from 'react';
import * as faceapi from 'face-api.js';

function GantryPage() {
  const [recognitionStatus, setRecognitionStatus] = useState(null);
  const [entryName, setEntryName] = useState('Punggol MRT');
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const intervalRef = useRef(null);

  useEffect(() => {
    const loadModels = async () => {
      await faceapi.nets.tinyFaceDetector.loadFromUri('/models/weights');
      await faceapi.nets.faceLandmark68Net.loadFromUri('/models/weights');
      await faceapi.nets.faceRecognitionNet.loadFromUri('/models/weights');
      startVideo();
    };

    const startVideo = () => {
      navigator.mediaDevices.getUserMedia({ video: {} })
        .then((stream) => {
          if (videoRef.current) {
            videoRef.current.srcObject = stream;
            videoRef.current.onloadedmetadata = () => {
              canvasRef.current.width = videoRef.current.videoWidth;
              canvasRef.current.height = videoRef.current.videoHeight;
              startFaceDetection();
            };
          }
        })
        .catch(err => console.error("Error accessing the webcam:", err));
    };

    loadModels();

    return () => clearInterval(intervalRef.current);
  }, []);

  const handleScanFace = async () => {
    const detections = await faceapi.detectAllFaces(
      videoRef.current,
      new faceapi.TinyFaceDetectorOptions()
    ).withFaceLandmarks().withFaceDescriptors();

    const ctx = canvasRef.current.getContext('2d');
    ctx.clearRect(0, 0, canvasRef.current.width, canvasRef.current.height);

    if (detections.length > 0) {
      console.log('Face detected:', detections);
      faceapi.draw.drawDetections(canvasRef.current, detections);
      
      // Capture the frame and send it to the API
      captureFrame();
    } else {
      console.log('No face detected');
      setRecognitionStatus('Failed to detect face');
    }
  };

  const captureFrame = async () => {
    const canvas = document.createElement('canvas');
    canvas.width = videoRef.current.videoWidth;
    canvas.height = videoRef.current.videoHeight;
    const context = canvas.getContext('2d');
    context.drawImage(videoRef.current, 0, 0, canvas.width, canvas.height);

    const frameData = canvas.toDataURL('image/jpeg'); // Convert frame to base64
    sendFrameToAPI(frameData);
  };

  const sendFrameToAPI = async (frameData) => {
    console.log("Attempting to send frame to API...");
  
    // Convert base64 data URL to a Blob
    const blob = await (await fetch(frameData)).blob();
    
    // Create FormData object and append entry and image
    const formData = new FormData();
    formData.append('entry', entryName);
    formData.append('image', blob, 'frame.jpg');
  
    try {
      const response = await fetch(`http://localhost/gantry/tripStart?entry=${entryName}`, {
        method: 'POST',
        body: formData,
      });
  
      if (response.ok) {
        console.log("Frame sent successfully");
        /* console.log(await response.json().message); */
        const responseData = await response.json();
        console.log(responseData.message);
        setRecognitionStatus(responseData.message);
      } else {
        console.log("Failed to send frame", await response.text());
        throw new Error("Failed to send frame");
      }
    } catch (error) {
      console.error("Error sending frame:", error);
      setRecognitionStatus("Failed to send frame");
    }
  };
  

  const startFaceDetection = () => {
    intervalRef.current = setInterval(() => {
      handleScanFace();
    }, 1000);
    console.log('Face detection started');
  };

  const handleReset = () => {
    setRecognitionStatus(null);
    setEntryName('');
  };

  return (
    <div className="h-screen flex justify-center items-center bg-blue-200">
      <div className="p-8 bg-white rounded-lg shadow-lg max-w-md w-full text-center">
        <h1 className="text-2xl font-semibold mb-6 text-gray-800">Gantry Interface</h1>
        <p className="text-gray-600 mb-4">Simulate the facial recognition process for entry or exit.</p>

        {/* Entry Name Input */}
        <div className="block w-full p-3 border border-gray-300 rounded-lg mb-4">{entryName}</div>
        

        {/* Webcam Feed and Canvas Overlay */}
        <div className="relative mb-6">
          <video ref={videoRef} autoPlay muted className="rounded-lg shadow-lg w-full h-48" />
          <canvas ref={canvasRef} className="absolute top-0 left-0 w-full h-full" />
        </div>

        {/* Recognition Status */}
        {/* {recognitionStatus === 'Success' && (
          <p className="text-green-500 mb-4">Face recognized! Access granted.</p>
        )}
        {recognitionStatus === 'Failed' && (
          <p className="text-red-500 mb-4">Face not recognized! Access denied.</p>
        )}
        {recognitionStatus === 'Frame Sent' && (
          <p className="text-green-500 mb-4">Frame sent to server.</p>
        )} */}
        <p className="text-gray-600 mb-4">{recognitionStatus}</p>

        {/* Reset Button */}
        <button
          onClick={handleReset}
          className="bg-gray-500 text-white py-2 px-4 rounded-lg hover:bg-gray-600 transition duration-300 w-full"
        >
          Reset
        </button>
      </div>
    </div>
  );
}

export default GantryPage;
