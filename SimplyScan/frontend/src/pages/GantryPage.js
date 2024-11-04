import React, { useRef, useEffect, useState } from 'react';
import * as faceapi from 'face-api.js';
import { useNavigate } from 'react-router-dom';

function GantryPage() {
  const navigate = useNavigate();
  const [recognitionStatus, setRecognitionStatus] = useState(null);
  const [gateStatus, setGateStatus] = useState('Closed');
  const [entryName, setEntryName] = useState('Punggol MRT');
  const [exitName, setExitName] = useState('Bukit Batok MRT');
  const [tripStatus, setTripStatus] = useState(
    localStorage.getItem('tripStatus') || 'Entry'
  );
  const [isGateOpen, setIsGateOpen] = useState(false);
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const intervalRef = useRef(null);

  useEffect(() => {
    const loadModels = async () => {
      await faceapi.nets.tinyFaceDetector.loadFromUri('../public/models/weights');
      await faceapi.nets.faceLandmark68Net.loadFromUri('../public/models/weights');
      await faceapi.nets.faceRecognitionNet.loadFromUri('../public/models/weights');
      startVideo();
    };

    const startVideo = () => {
      navigator.mediaDevices.getUserMedia({ video: {} })
        .then((stream) => {
          if (videoRef.current) {
            videoRef.current.srcObject = stream;
            videoRef.current.onloadedmetadata = () => {
              if (canvasRef.current) {
                canvasRef.current.width = videoRef.current.videoWidth;
                canvasRef.current.height = videoRef.current.videoHeight;
                startFaceDetection();
              }
            };
          }
        })
        .catch(err => console.error("Error accessing the webcam:", err));
    };

    loadModels();
    //startVideo();
    // Clean up video stream when component unmounts or user navigates away
    return () => {
      stopVideoStream();
    };
  }, []);

  const handleScanFace = async () => {
    if (!canvasRef.current || !videoRef.current) {
      return;
    }

    const startTime = performance.now();

    const detections = await faceapi.detectAllFaces(
      videoRef.current,
      new faceapi.TinyFaceDetectorOptions()
    ).withFaceLandmarks().withFaceDescriptors();

    const endTime = performance.now();
    const timeTaken = endTime - startTime;

    console.log(`Time taken to detect face: ${timeTaken.toFixed(2)} ms`);

    const ctx = canvasRef.current.getContext('2d');
    if (ctx) {
      ctx.clearRect(0, 0, canvasRef.current.width, canvasRef.current.height);
    } else {
      console.error("Failed to get canvas context");
      return;
    }

    if (detections.length > 0) {
      console.log('Face detected:', detections);
      faceapi.draw.drawDetections(canvasRef.current, detections);
      captureFrame();
    } else {
      console.log('No face detected');
      setRecognitionStatus('Failed to detect face');
    }
  };

  const captureFrame = async () => {
    if (!videoRef.current) return;

    const canvas = document.createElement('canvas');
    canvas.width = videoRef.current.videoWidth;
    canvas.height = videoRef.current.videoHeight;
    const context = canvas.getContext('2d');
    context.drawImage(videoRef.current, 0, 0, canvas.width, canvas.height);

    const frameData = canvas.toDataURL('image/jpeg');
    sendFrameToAPI(frameData);
  };

  const sendFrameToAPI = async (frameData) => {
    if (isGateOpen) return;

    console.log("Attempting to send frame to API...");
    
    const blob = await (await fetch(frameData)).blob();
    const formData = new FormData();
    formData.append('image', blob, 'frame.jpg');
    
    try {
      let response;
  
      if (tripStatus === 'Entry') {
        console.log('Entering station:', entryName);
        formData.append('entry', entryName);
        response = await fetch(`http://localhost:8080/gantry/tripStart?entry=${entryName}`, {
          method: 'POST',
          body: formData,
        });
      } else {
        console.log('Exiting station:', exitName);
        response = await fetch(`http://localhost:8080/gantry/tripEnd?exit=${exitName}`, {
          method: 'PUT',
          body: formData,
        });
      }
  
      if (response.ok) {
        const responseData = await response.json();
        console.log(responseData.message);
        setRecognitionStatus(responseData.message);
        if (responseData.message === 'Trip created' || responseData.message === 'Trip ended') {
          setGateStatus('Open');
          setIsGateOpen(true);
          setTimeout(() => {
            setGateStatus('Closed');
            setIsGateOpen(false);
          }, 3000);
        }
      } else {
        const errData = await response.json();
        console.log("Failed to send frame", errData);
        setRecognitionStatus(errData.detail);
        throw new Error("Failed to send frame");
      }
    } catch (error) {
      console.error("Error sending frame:", error);
    }
  };

  const startFaceDetection = () => {
    intervalRef.current = setInterval(() => {
      handleScanFace();
    }, 1000);
    console.log('Starting face detection...');
  };

  const stopVideoStream = () => {
    clearInterval(intervalRef.current);
  
    if (videoRef.current && videoRef.current.srcObject) {
      const stream = videoRef.current.srcObject;
      const tracks = stream.getTracks();
      tracks.forEach((track) => {
        track.stop();
        console.log(`Stopped track: ${track.kind}`);
      });
      videoRef.current.srcObject = null;
      console.log("Camera has been forcefully disabled.");
    }
  
    // Attempt to reset camera permissions
    navigator.mediaDevices.getUserMedia({ video: false }).catch(() => {
      console.log("Camera permissions have been reset.");
    });
  };
  

  const handleReset = () => {
    setRecognitionStatus(null);
  };

  const toggleTripStatus = () => {
    setTripStatus((prevStatus) => {
      const newStatus = prevStatus === 'Entry' ? 'Exit' : 'Entry';
      localStorage.setItem('tripStatus', newStatus);
      console.log("Trip status set to:", newStatus);
      
      setTimeout(() => {
        window.location.reload();
      }, 100);
      
      return newStatus;
    });
  };

  const goToLogin = () => {
    stopVideoStream(); // Ensure the video stream stops when navigating away
    setTimeout(() => navigate('/'), 50); // Slight delay to ensure stream stops before navigation
  };

  return (
    <div className="h-screen flex justify-center items-center bg-blue-200">
      <div className="p-8 bg-white rounded-lg shadow-lg max-w-md w-full text-center">
        <h1 className="text-2xl font-semibold mb-6 text-gray-800">Gantry Interface</h1>
        <p className="text-gray-600 mb-4">Simulate the facial recognition process for entry or exit.</p>
        <div className={`block w-full p-3 border border-gray-300 rounded-lg mb-4 ${tripStatus === 'Entry' ? 'text-green-500' : 'text-red-500'}`}>
          Gantry mode: {tripStatus}
        </div>
        <div className="block w-full p-3 border border-gray-300 rounded-lg mb-4">
          Gantry gates: {gateStatus}
        </div>
        <div className="block w-full p-3 border border-gray-300 rounded-lg mb-4">
          {tripStatus === 'Entry' ? entryName : exitName}
        </div>

        <div className="relative mb-6">
          <video ref={videoRef} autoPlay muted className="rounded-lg shadow-lg w-full h-48" />
          <canvas ref={canvasRef} className="absolute top-0 left-0 w-full h-full" />
        </div>

        <p className="text-gray-600 mb-4">{recognitionStatus}</p>

        <button
          onClick={toggleTripStatus}
          className={`mb-4 py-2 px-4 rounded-lg w-full ${tripStatus === 'Entry' ? 'bg-green-500' : 'bg-red-500'} text-white`}
        >
          Toggle to {tripStatus === 'Entry' ? 'Exit' : 'Entry'}
        </button>

        <button
          onClick={handleReset}
          className="bg-gray-500 text-white py-2 px-4 rounded-lg hover:bg-gray-600 transition duration-300 w-full mb-4"
        >
          Reset
        </button>

        <button
          onClick={goToLogin}
          className="bg-blue-500 text-white py-2 px-4 rounded-lg hover:bg-blue-600 transition duration-300 w-full"
        >
          Back to Login
        </button>
      </div>
    </div>
  );
}

export default GantryPage;