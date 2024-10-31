import React, { useRef, useEffect } from 'react';
import * as faceapi from 'face-api.js';

const FaceRecognition = () => {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);

  useEffect(() => {
    // Load face-api.js models
    const loadModels = async () => {
      await faceapi.nets.tinyFaceDetector.loadFromUri('../public/models');
      await faceapi.nets.faceLandmark68Net.loadFromUri('../public/models');
      await faceapi.nets.faceRecognitionNet.loadFromUri('../public/models');
      await faceapi.nets.faceExpressionNet.loadFromUri('../public/models');

      startVideo();
    };

    loadModels();
  }, []);

  // Start video stream
  const startVideo = () => {
    navigator.mediaDevices
      .getUserMedia({ video: {} })
      .then((stream) => {
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
        }
      })
      .catch((err) => console.error("Error accessing webcam:", err));
  };

  useEffect(() => {
    // Set up face detection once the video is playing
    if (videoRef.current) {
      videoRef.current.addEventListener('play', () => {
        const canvas = canvasRef.current;
        const displaySize = {
          width: videoRef.current.videoWidth,
          height: videoRef.current.videoHeight,
        };
        
        faceapi.matchDimensions(canvas, displaySize);

        setInterval(async () => {
          const detections = await faceapi.detectAllFaces(
            videoRef.current,
            new faceapi.TinyFaceDetectorOptions()
          ).withFaceLandmarks().withFaceExpressions();

          const resizedDetections = faceapi.resizeResults(detections, displaySize);
          canvas.getContext('2d').clearRect(0, 0, canvas.width, canvas.height);
          faceapi.draw.drawDetections(canvas, resizedDetections);
          faceapi.draw.drawFaceLandmarks(canvas, resizedDetections);
          faceapi.draw.drawFaceExpressions(canvas, resizedDetections);
        }, 100);
      });
    }
  }, []);

  return (
    <div className="flex flex-col items-center">
      <video ref={videoRef} autoPlay muted className="rounded-lg shadow-lg" width="720" height="560" />
      <canvas ref={canvasRef} className="absolute top-0 left-0" />
    </div>
  );
};

export default FaceRecognition;
