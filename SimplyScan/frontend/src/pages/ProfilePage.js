import React, { useState, useEffect } from 'react';
import Sidebar from '../components/Sidebar';

function ProfilePage() {
  // Initial user info, could be fetched from an API
  const [userInfo, setUserInfo] = useState({
    name: 'John Doe',
    nric: 'johndoe@example.com',
    username: 'johndoe',
    password: '123-456-7890',
  });

  const [image, setImage] = useState(null);
  const [cardDetails, setCardDetails] = useState('');
  const [saveMessage, setSaveMessage] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    // Here you can fetch the user data from an API and set the state
    // Example:
    // fetch('/api/user-info')
    //   .then(response => response.json())
    //   .then(data => setUserInfo(data));
  }, []);

  const handleUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      setImage(URL.createObjectURL(file));
    }
  };

  const handleSaveProfile = () => {
    setSaveMessage('');
    setError('');

    if (!image) {
      setError('Please upload a profile image.');
      return;
    }
    if (!cardDetails) {
      setError('Please enter your card details.');
      return;
    }

    // Mock save logic
    setSaveMessage('Profile saved successfully!');
  };

  return (
    <div className="flex">
      {/* Sidebar */}
      <Sidebar />

      {/* Main content */}
      <div className="ml-64 p-8 w-full bg-blue-200 min-h-screen">
        <h1 className="text-2xl font-semibold mb-6 text-gray-800">Profile</h1>

        {/* User Information */}
        <div className="mb-8 p-6 bg-white rounded-lg shadow-lg">
          <h2 className="text-xl font-semibold text-gray-800 mb-4">User Information</h2>
          <p className="mb-2"><strong>Name:</strong> {userInfo.name}</p>
          <p className="mb-2"><strong>NRIC:</strong> {userInfo.nric}</p>
          <p className="mb-2"><strong>Username:</strong> {userInfo.username}</p>
          <p className="mb-4"><strong>Phone:</strong> {userInfo.password}</p>
        </div>

        {/* Profile Image Upload */}
        <div className="mb-8 p-6 bg-white rounded-lg shadow-lg">
          <h2 className="text-xl font-semibold text-gray-800 mb-4">Profile Image</h2>
          <input type="file" onChange={handleUpload} className="block mb-4" />
          {image && (
            <img
              src={image}
              alt="Uploaded Profile"
              className="h-32 w-32 rounded-full object-cover mb-4"
            />
          )}
        </div>

        {/* Card Details */}
        <div className="mb-8 p-6 bg-white rounded-lg shadow-lg">
          <h2 className="text-xl font-semibold text-gray-800 mb-4">Card Details</h2>
          <input
            type="text"
            placeholder="Enter Card Details"
            value={cardDetails}
            onChange={(e) => setCardDetails(e.target.value)}
            className="block w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        {/* Save Button */}
        <button
          onClick={handleSaveProfile}
          className="bg-blue-500 text-white py-3 px-6 rounded-lg hover:bg-blue-600 transition duration-300"
        >
          Save
        </button>

        {/* Feedback Messages */}
        {saveMessage && <p className="text-green-500 mt-4">{saveMessage}</p>}
        {error && <p className="text-red-500 mt-4">{error}</p>}
      </div>
    </div>
  );
}

export default ProfilePage;
