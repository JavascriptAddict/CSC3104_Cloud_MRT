import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';


function SignUpPage() {
  const [userInfo, setUserInfo] = useState({
    name: '',
    nric: '',
    username: '',
    password: '',
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
      setImage(file);
    }
  };

  const handleSignUp = async () => {
    // Clear messages
    setError('');
    setSuccessMessage('');

    // Validate inputs
    const { name, nric, username, password } = userInfo;
    if (!name || !nric || !username || !password) {
      setError('Please fill in all the fields.');
      return;
    }
    const profile_image = image;
    if (!profile_image) {
      setError('Please upload a profile image.');
      return;
    } 
    
    

    /* var newForm = {
      "name": name,
      "nric": nric,
      "username": username,
      "password": password,
    } */

    var formData = new FormData();
    formData.append('name', name);
    formData.append('nric', nric);
    formData.append('username', username);
    formData.append('password', password);
    formData.append('image', profile_image);


    try {
      const response = await fetch(`http://localhost:8080/accounts/create?name=${name}&nric=${nric}&username=${username}&password=${password}`, {
          method: 'POST',
          body: formData,
          
         
      });

      if (!response.ok) {
          throw new Error('Network response was not ok');
      }
      else if (response.ok) {
        const data = await response.json();
        
        console.log(data.message);
        if (data.message === 'Account created') {
          console.log('Account created');
          setSuccessMessage(data.message);
          // Redirect or handle success
          setTimeout(() => {
            navigate('/');
          }, 2000);
        } else {
          setError(data.message);
        }
        /* navigate('/'); */
      }
      
      
    } catch (error) {
        setError('Sign up failed: ' + error.message);
    }
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
          type="nric"
          name="nric"
          placeholder="Nric"
          value={userInfo.nric}
          onChange={handleChange}
          className="block w-full p-3 mb-4 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <input
          type="text"
          name="username"
          placeholder="Username"
          value={userInfo.username}
          onChange={handleChange}
          className="block w-full p-3 mb-4 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <input
          type="password"
          name="password"
          placeholder="Password"
          value={userInfo.password}
          onChange={handleChange}
          className="block w-full p-3 mb-4 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <label className="block mb-2 font-bold">Profile Image</label>
        <input type="file" onChange={handleImageUpload} className="block w-full mb-4" />
        {image && (
          <div className="mb-4">
            <img
              src={URL.createObjectURL(image)}
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