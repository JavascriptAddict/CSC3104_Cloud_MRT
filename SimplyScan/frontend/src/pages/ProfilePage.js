import React, { useState, useEffect } from 'react';
import Sidebar from '../components/Sidebar';

function ProfilePage() {
  const [userInfo, setUserInfo] = useState({
    name: '',
    nric: '',
    username: '',
    password: '', // Leave this blank initially for the form
    wallet: 0,
  });

  const [currentPassword, setCurrentPassword] = useState(''); // Store the original password here
  const [image, setImage] = useState(null);
  const [saveMessage, setSaveMessage] = useState('');
  const [error, setError] = useState('');
  

  useEffect(() => {
    const fetchUserInfo = async () => {
      const token = localStorage.getItem('access_token');

      if (!token) {
        setError('You must log in first.');
        return;
      }

      try {
        const response = await fetch(`http://localhost/accounts`, {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.detail || 'Failed to fetch user info.');
        }

        const data = await response.json();
        console.log(data);

        const wallet = await fetch(`http://localhost/accounts/checkwallet`, {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        });

        if (!wallet.ok) {
          const errorData = await wallet.json();
          throw new Error(errorData.detail || 'Failed to fetch wallet info.');
        }

        const walletData = await wallet.json();
        console.log(walletData.data);
        
        setUserInfo({
          ...data.data,
          password: '', // Set password field to blank in the form
          wallet: walletData.data,
        });
        
        setCurrentPassword(data.data.password); // Store the original password separately
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

    const token = localStorage.getItem('access_token');

    // Check if password field is empty; if it is, use the original password
    const updatedUserInfo = {
      ...userInfo,
      password: userInfo.password || currentPassword,
    };

    try {
      const response = await fetch(`http://localhost/accounts`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(updatedUserInfo), // Send updated info with password handling
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail);
      }

      if (image) {
        const formData = new FormData();
        formData.append('image', image);

        const uploadResponse = await fetch(`http://localhost/accounts/image/upload`, {
          method: 'PUT',
          headers: {
            'Authorization': `Bearer ${token}`,
          },
          body: formData,
        });

        if (!uploadResponse.ok) {
          const errorData = await uploadResponse.json();
          throw new Error(errorData.detail);
        }
      }

      const data = await response.json();
      console.log(data);
      setSaveMessage('Profile saved successfully!');
    } catch (error) {
      setError('Error saving profile: ' + error.message);
    }
  };

  return (
    <div className="flex">
      <Sidebar />
      <div className="ml-64 p-8 w-full bg-blue-200 min-h-screen">
        <h1 className="text-2xl font-semibold mb-6 text-gray-800">Profile</h1>
        
        <div className="mb-8 p-6 bg-white rounded-lg shadow-lg">
          <h2 className="text-xl font-semibold text-gray-800 mb-4">User Information</h2>
          <div className="block w-full p-3 border border-gray-300 rounded-lg mb-4">Wallet Balance: ${userInfo.wallet}</div>
          <div className="block w-full p-3 border border-gray-300 rounded-lg mb-4">Username: {userInfo.username}</div>
          <div className="block w-full p-3 border border-gray-300 rounded-lg mb-4">Name: {userInfo.name}</div>
          <div className="block w-full p-3 border border-gray-300 rounded-lg mb-4">NRIC: {userInfo.nric}</div>
          <div>Change password</div>
          <input
            type="password"
            name="password"
            value={userInfo.password}
            onChange={handleInputChange}
            placeholder="Enter new password if you want to change"
            className="block w-full p-3 border border-gray-300 rounded-lg mb-4"
          />
        </div>

        <div className="mb-8 p-6 bg-white rounded-lg shadow-lg">
          <h2 className="text-xl font-semibold text-gray-800 mb-4">Upload a front-facing image for facial recognition</h2>
          <input type="file" onChange={handleUpload} className="block mb-4" />
          {image && (
            <img
              src={URL.createObjectURL(image)}
              alt="Uploaded Profile"
              className="h-32 w-32 rounded-full object-cover mb-4"
            />
          )}
        </div>

        <button
          onClick={handleSaveProfile}
          className="bg-blue-500 text-white py-3 px-6 rounded-lg hover:bg-blue-600 transition duration-300"
        >
          Save
        </button>

        {saveMessage && <p className="text-green-500 mt-4">{saveMessage}</p>}
        {error && <p className="text-red-500 mt-4">{error}</p>}
      </div>
    </div>
  );
}

export default ProfilePage;
