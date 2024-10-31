import React, { useRef, useEffect, useState } from 'react';
import * as faceapi from 'face-api.js';

function GantryPage() {
  const [recognitionStatus, setRecognitionStatus] = useState(null);
  const videoRef = useRef(null);

  useEffect(() => {
    const loadModels = async () => {
      await faceapi.nets.tinyFaceDetector.loadFromUri('/models/weights');
      await faceapi.nets.faceLandmark68Net.loadFromUri('/models/weights');
      await faceapi.nets.faceRecognitionNet.loadFromUri('/models/weights');
      startVideo();
    };
    
    loadModels();
  }, []);

  const startVideo = () => {
    navigator.mediaDevices.getUserMedia({ video: {} })
      .then((stream) => {
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
        }
      })
      .catch(err => console.error("Error accessing the webcam:", err));
  };

  const handleScanFace = async () => {
    const detections = await faceapi.detectAllFaces(
      videoRef.current,
      new faceapi.TinyFaceDetectorOptions()
    ).withFaceLandmarks().withFaceDescriptors();

    if (detections.length > 0) {
      console.log("Face detected:", detections); // Logs detection details
      setRecognitionStatus('Success');
    } else {
      console.log("No face detected"); // Logs if no face is found
      setRecognitionStatus('Failed');
    }
  };

  const handleReset = () => {
    setRecognitionStatus(null);
  };

  return (
    <div className="h-screen flex justify-center items-center bg-blue-200">
      <div className="p-8 bg-white rounded-lg shadow-lg max-w-md w-full text-center">
        <h1 className="text-2xl font-semibold mb-6 text-gray-800">Gantry Interface</h1>
        <p className="text-gray-600 mb-4">Simulate the facial recognition process for entry or exit.</p>

        {/* Webcam Feed */}
        <div className="mb-6">
          <video ref={videoRef} autoPlay muted className="rounded-lg shadow-lg w-full h-48" />
        </div>

        {/* Simulated recognition status */}
        {recognitionStatus === 'Success' && (
          <p className="text-green-500 mb-4">Face recognized! Access granted.</p>
        )}
        {recognitionStatus === 'Failed' && (
          <p className="text-red-500 mb-4">Face not recognized! Access denied.</p>
        )}

        {/* Simulate scan face */}
        <button
          onClick={handleScanFace}
          className="bg-blue-500 text-white py-3 px-6 rounded-lg hover:bg-blue-600 transition duration-300 mb-4 w-full"
        >
          Simulate Face Scan
        </button>

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
