import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';

function LoginPage() {
  /* const [username, setusername] = useState('');
  const [password, setPassword] = useState(''); */
  const [userLogin, setUserLogin] = useState({
    username: '',
    password: '',
  });
  const [loginError, setLoginError] = useState('');
  const [loginSuccess, setLoginSuccess] = useState('');
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setUserLogin((prev) => ({ ...prev, [name]: value }));
  };

  const handleLogin = async () => {
    setLoginError('');
    setLoginSuccess('');

    const {username, password} = userLogin;
    if (!username || !password) {
      setLoginError('Please fill in all the fields.');
      return;
    }

    const newForm = new URLSearchParams();
    newForm.append('username', username);
    newForm.append('password', password);

    try {
      const response = await fetch('http://localhost:8080/token', { 
          method: 'POST',
          body: newForm,
          headers: {
              'Content-Type': 'application/x-www-form-urlencoded',
          },
      });

      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.detail);
      }

      const data = await response.json();
      // Store the access token in local storage or state
      console.log(data);
      localStorage.setItem('access_token', data.access_token);
      setLoginSuccess(data.message);
      

      // Redirect or handle success
      
      navigate('/profile');
      
    } catch (error) {
      setLoginError('Sign up failed: ' + error.message);
    }

  };

  return (
    <div className="h-screen flex justify-center items-center bg-blue-300">
      <form className="p-10 bg-white rounded-lg shadow-lg w-full max-w-sm">
        <h1 className="text-2xl font-semibold text-center mb-6 text-gray-800">
          Welcome to SimplyScan
        </h1>

        {/* username Input */}
        <input
          type="username"
          name='username'
          placeholder="Username"
          className="block w-full p-3 mb-4 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          value={userLogin.username}
          onChange={handleChange}
        />

        {/* Password Input */}
        <input
          type="password"
          name='password'
          placeholder="Password"
          className="block w-full p-3 mb-4 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          value={userLogin.password}
          onChange={handleChange}
        />

        {/* Login Button */}
        <button
          type="button"
          className="bg-blue-500 text-white w-full py-3 rounded-lg hover:bg-blue-600 transition duration-300"
          onClick={handleLogin}
        >
          Login
        </button>

        {/* Error/Success Feedback */}
        {loginError && <p className="text-red-500 text-center mt-4">{loginError}</p>}
        {loginSuccess && <p className="text-green-500 text-center mt-4">{loginSuccess}</p>}

        {/* Sign Up Link */}
        <div className="mt-4 text-center">
          <p className="text-gray-600">
            Don't have an account?{' '}
            <Link to="/signup" className="text-blue-500 hover:underline">
              Sign up here
            </Link>.
          </p>
          <Link to="/gantry" className="text-blue-500">[Gantry Interface]</Link>
        </div>
      </form>
    </div>
  );
}

export default LoginPage;
