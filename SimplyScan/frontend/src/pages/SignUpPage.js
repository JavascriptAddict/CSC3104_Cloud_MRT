import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function SignUpPage() {
  const [userInfo, setUserInfo] = useState({
    name: '',
    email: '',
    phone: '',
    cardDetails: '',
  });

  const [image, setImage] = useState(null);
  const [error, setError] = useState('');
  const [successMessage, setSuccessMessage] = useState('');
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setUserInfo((prev) => ({ ...prev, [name]: value }));
  };

  const handleImageUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      setImage(URL.createObjectURL(file));
    }
  };

  const handleSignUp = () => {
    // Clear messages
    setError('');
    setSuccessMessage('');

    // Validate inputs
    const { name, email, phone, cardDetails } = userInfo;
    if (!name || !email || !phone || !cardDetails) {
      setError('Please fill in all the fields.');
      return;
    }
    if (!image) {
      setError('Please upload a profile image.');
      return;
    }

    // Mock sign-up logic
    setSuccessMessage('Sign up successful! Redirecting...');
    setTimeout(() => {
      navigate('/profile');
    }, 1500);
  };

  return (
    <div className="h-screen flex justify-center items-center bg-blue-300">
      <form className="p-10 bg-white rounded-lg shadow-lg w-full max-w-sm">
        <h1 className="text-xl font-bold mb-6">Sign Up</h1>

        <input
          type="text"
          name="name"
          placeholder="Name"
          value={userInfo.name}
          onChange={handleChange}
          className="block w-full p-3 mb-4 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <input
          type="email"
          name="email"
          placeholder="Email"
          value={userInfo.email}
          onChange={handleChange}
          className="block w-full p-3 mb-4 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <input
          type="text"
          name="phone"
          placeholder="Phone"
          value={userInfo.phone}
          onChange={handleChange}
          className="block w-full p-3 mb-4 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <input
          type="text"
          name="cardDetails"
          placeholder="Card Details"
          value={userInfo.cardDetails}
          onChange={handleChange}
          className="block w-full p-3 mb-4 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <label className="block mb-2 font-bold">Profile Image</label>
        <input type="file" onChange={handleImageUpload} className="block w-full mb-4" />
        {image && (
          <div className="mb-4">
            <img
              src={image}
              alt="Uploaded Profile"
              className="h-32 w-32 rounded-full object-cover"
            />
          </div>
        )}

        <button
          type="button"
          className="bg-green-500 text-white px-4 py-2 rounded w-full"
          onClick={handleSignUp}
        >
          Sign Up
        </button>

        {error && <p className="text-red-500 mt-4">{error}</p>}
        {successMessage && <p className="text-green-500 mt-4">{successMessage}</p>}
      </form>
    </div>
  );
}

export default SignUpPage;
