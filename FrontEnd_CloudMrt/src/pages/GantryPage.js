import React, { useState } from 'react';

function GantryPage() {
  const [recognitionStatus, setRecognitionStatus] = useState(null);

  const handleScanFace = () => {
    // Simulating face scan success (can be replaced with backend integration later)
    const isRecognized = Math.random() > 0.5; // Random success/failure simulation
    setRecognitionStatus(isRecognized ? 'Success' : 'Failed');
  };

  const handleReset = () => {
    setRecognitionStatus(null);
  };

  return (
    <div className="h-screen flex justify-center items-center bg-blue-200">
      <div className="p-8 bg-white rounded-lg shadow-lg max-w-md w-full text-center">
        <h1 className="text-2xl font-semibold mb-6 text-gray-800">Gantry Interface</h1>
        <p className="text-gray-600 mb-4">Simulate the facial recognition process for entry or exit.</p>

        {/* Placeholder for camera feed */}
        <div className="mb-6">
          <div className="w-full h-48 bg-gray-200 rounded-lg flex justify-center items-center">
            <span className="text-gray-500">Camera Feed Placeholder</span>
          </div>
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
