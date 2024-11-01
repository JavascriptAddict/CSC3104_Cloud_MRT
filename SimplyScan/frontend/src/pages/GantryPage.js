import React, { useRef, useEffect, useState } from 'react';
import * as faceapi from 'face-api.js';

function GantryPage() {
  const [recognitionStatus, setRecognitionStatus] = useState(null);
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
              // Set canvas size to match video size
              canvasRef.current.width = videoRef.current.videoWidth;
              canvasRef.current.height = videoRef.current.videoHeight;
              startFaceDetection();
            };
          }
        })
        .catch(err => console.error("Error accessing the webcam:", err));
    };

    loadModels();

    return () => clearInterval(intervalRef.current); // Clear interval on component unmount
  }, []);

  const handleScanFace = async () => {
    const detections = await faceapi.detectAllFaces(
      videoRef.current,
      new faceapi.TinyFaceDetectorOptions()
    ).withFaceLandmarks().withFaceDescriptors();

    const ctx = canvasRef.current.getContext('2d');
    ctx.clearRect(0, 0, canvasRef.current.width, canvasRef.current.height); // Clear previous drawings

    if (detections.length > 0) {
      console.log('Face detected:', detections);
      setRecognitionStatus('Success');
      // Draw bounding box
      faceapi.draw.drawDetections(canvasRef.current, detections, {
        boxColor: 'green', // I put green but the box is blue what the fuck
        lineWidth: 2 // Set line width of bounding box
      });
    } else {
      console.log('No face detected');
      setRecognitionStatus('Failed');
    }
  };

  const startFaceDetection = () => {
    intervalRef.current = setInterval(() => {
      handleScanFace();
    }, 1000); // Adjust interval as needed
    console.log('Face detection started');
  };

  const handleReset = () => {
    setRecognitionStatus(null);
  };

  return (
    <div className="h-screen flex justify-center items-center bg-blue-200">
      <div className="p-8 bg-white rounded-lg shadow-lg max-w-md w-full text-center">
        <h1 className="text-2xl font-semibold mb-6 text-gray-800">Gantry Interface</h1>
        <p className="text-gray-600 mb-4">Simulate the facial recognition process for entry or exit.</p>

        {/* Webcam Feed and Canvas Overlay */}
        <div className="relative mb-6">
          <video ref={videoRef} autoPlay muted className="rounded-lg shadow-lg w-full h-48" />
          <canvas ref={canvasRef} className="absolute top-0 left-0 w-full h-full" />
        </div>

        {/* Simulated recognition status */}
        {recognitionStatus === 'Success' && (
          <p className="text-green-500 mb-4">Face recognized! Access granted.</p>
        )}
        {recognitionStatus === 'Failed' && (
          <p className="text-red-500 mb-4">Face not recognized! Access denied.</p>
        )}

        {/* Reset button to start over */}
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
