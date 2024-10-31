import React, { useState, useEffect } from 'react';
import Sidebar from '../components/Sidebar';

function ProfilePage() {
  // Initial user info, could be fetched from an API
  const [userInfo, setUserInfo] = useState({
    name: '',
    nric: '',
    username: '',
    password: '',
  });

  const [image, setImage] = useState(null);
  const [saveMessage, setSaveMessage] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchUserInfo = async () => {
      const token = localStorage.getItem('access_token'); // Retrieve token from local storage

      if (!token) {
        setError('You must log in first.');
        return;
      }

      try {
        const response = await fetch(`http://localhost/accounts`, {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`, // Include token in the header
            'Content-Type': 'application/json',
          },
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.detail || 'Failed to fetch user info.');
        }

        const data = await response.json();
        console.log(data);
        setUserInfo(data.data); // Assuming the data structure matches userInfo state
      } catch (error) {
        setError('Error fetching user information: ' + error.message);
      }
    };

    fetchUserInfo();
  }, []);

  const handleUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      setImage(file);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setUserInfo((prevInfo) => ({
      ...prevInfo,
      [name]: value,
    }));
  };

  const handleSaveProfile = async () => {
    setSaveMessage('');
    setError('');

    const token = localStorage.getItem('access_token'); // Retrieve token from local storage

    // Update user information
    try {
      const response = await fetch(`http://localhost/accounts`, {
        method: 'PUT', // Assuming your API uses PUT for updates
        headers: {
          'Authorization': `Bearer ${token}`, // Include token in the header
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(userInfo), // Send updated userInfo
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail);
      }

      // If image upload is needed, handle that as well
      if (image) {
        const formData = new FormData();
        formData.append('image', image);

        const uploadResponse = await fetch(`http://localhost/accounts/image/upload`, {
          method: 'PUT',
          headers: {
            'Authorization': `Bearer ${token}`, // Include token in the header
            
          },
          body: formData, // Send the form data
        });

        if (!uploadResponse.ok) {
          const errorData = await uploadResponse.json();
          throw new Error(errorData.detail);
        }
      }

      const data = await response.json();
      console.log(data);
      setSaveMessage('Profile saved successfully!'); // Show success message
    } catch (error) {
      setError('Error saving profile: ' + error.message);
    }
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
          <div>Name</div>
          <input
            type="text"
            name="name"
            placeholder="Name"
            value={userInfo.name}
            onChange={handleInputChange}
            className="block w-full p-3 border border-gray-300 rounded-lg mb-4"
          />
          <div>NRIC</div>
          <input
            type="text"
            name="nric"
            placeholder="NRIC"
            value={userInfo.nric}
            onChange={handleInputChange}
            className="block w-full p-3 border border-gray-300 rounded-lg mb-4"
          />
          <div>Username</div>
          <input
            type="text"
            name="username"
            placeholder="Username"
            value={userInfo.username}
            onChange={handleInputChange}
            className="block w-full p-3 border border-gray-300 rounded-lg mb-4"
          />
          
        </div>

        {/* Profile Image Upload */}
        <div className="mb-8 p-6 bg-white rounded-lg shadow-lg">
          <h2 className="text-xl font-semibold text-gray-800 mb-4">Upload a front-facing image for facial recognition</h2>
          <input type="file" onChange={handleUpload} className="block mb-4" />
          {image && (
            <img
              src={URL.createObjectURL(image)} // Show preview of uploaded image
              alt="Uploaded Profile"
              className="h-32 w-32 rounded-full object-cover mb-4"
            />
          )}
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
