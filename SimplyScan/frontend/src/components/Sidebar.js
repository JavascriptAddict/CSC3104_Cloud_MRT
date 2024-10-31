import React from 'react';
import { Link, useNavigate } from 'react-router-dom';

function Sidebar() {
  const navigate = useNavigate();

  const handleLogout = () => {
    // Clear any session or token here (if applicable)
    // For now, simply redirect to the login page
    navigate('/');
  };

  return (
    <div className="h-screen w-64 bg-gray-900 text-white fixed flex flex-col justify-between">
      <div className="p-6">
        <h2 className="text-2xl font-bold text-gray-200 mb-6">Navigation</h2>
        <ul className="mt-4 space-y-4">
          <li>
            <Link
              to="/profile"
              className="block py-2 px-4 rounded-lg text-gray-200 bg-gray-800 hover:bg-gray-700 transition duration-300"
            >
              Profile
            </Link>
          </li>
          <li>
            <Link
              to="/history"
              className="block py-2 px-4 rounded-lg text-gray-200 bg-gray-800 hover:bg-gray-700 transition duration-300"
            >
              History
            </Link>
          </li>
        </ul>
      </div>

      {/* Log Out Button */}
      <div className="p-6">
        <button
          className="w-full bg-red-600 text-white py-3 px-4 rounded-lg hover:bg-red-700 transition duration-300"
          onClick={handleLogout}
        >
          Log Out
        </button>
      </div>
    </div>
  );
}

export default Sidebar;
