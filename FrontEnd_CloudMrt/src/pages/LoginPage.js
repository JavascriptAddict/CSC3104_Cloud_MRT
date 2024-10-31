import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';

function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loginError, setLoginError] = useState('');
  const [loginSuccess, setLoginSuccess] = useState('');
  const navigate = useNavigate();

  const handleLogin = () => {
    setLoginError('');
    setLoginSuccess('');

    if (email === 'hi' && password === 'hi') {
      setLoginSuccess('Login successful! Redirecting...');
      setTimeout(() => {
        navigate('/profile');
      }, 1500);
    } else {
      setLoginError('Invalid credentials. Please try again.');
    }
  };

  return (
    <div className="h-screen flex justify-center items-center bg-blue-300">
      <form className="p-10 bg-white rounded-lg shadow-lg w-full max-w-sm">
        <h1 className="text-2xl font-semibold text-center mb-6 text-gray-800">
          Welcome to SMRT
        </h1>

        {/* Email Input */}
        <input
          type="email"
          placeholder="Email"
          className="block w-full p-3 mb-4 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />

        {/* Password Input */}
        <input
          type="password"
          placeholder="Password"
          className="block w-full p-3 mb-4 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
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
