import React, { useState } from 'react';
import Sidebar from '../components/Sidebar';


function TopUpPage() {
  /* const [amount, setAmount] = useState('');
  const [cardNumber, setCardNumber] = useState('');
  const [cvv, setCvv] = useState('');
  const [expiryDate, setExpiryDate] = useState(''); // Combined field for month/year */
  const [message, setMessage] = useState(''); 

  const [topupInfo, setTopupInfo] = useState({
    amount: '',
    cardNumber: '',
    cvv: '',
    expiryDate: '', // Combined field for month/year
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setTopupInfo((prev) => ({ ...prev, [name]: value }));
  };

  const handleTopUp = async () => {
    const token = localStorage.getItem('access_token');
    const { amount, cardNumber, cvv, expiryDate } = topupInfo;
    if (!token) {
      setMessage('You must log in first.');
      return;
    }
    const [expiryMonth, expiryYear] = expiryDate.split('/'); // Split the MM/YY format
    if (!amount || !cardNumber || !cvv || !expiryDate) {
      setMessage('Please fill in all the fields.');
      return;
    }
  
    var newForm = {
      "amount": amount,
      "cardNumber": cardNumber,
      "cvv": cvv,
      "expiryYear": expiryYear,
      "expiryMonth": expiryMonth,
    };
    try {
      const response = await fetch('http://localhost/accounts/topup', {
        method: 'POST',
        body: JSON.stringify(newForm),
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });
      if (response.ok) {
        const data = await response.json();
        setMessage(data.message);
      } else{
        const data = await response.json();
        // Check if data.detail is an object
        if (typeof data.detail === 'object' && data.detail !== null) {
          // Optionally, convert it to a string if it's an object
          setMessage(JSON.stringify(data.detail)); // You may want to format this differently
        } else {
          setMessage(data.detail); // Assuming it's a string
        }
        return;
      }
    } catch (error) {
      console.error('Error:', error);
      setMessage('Failed to top up balance');
    }
  };
  

  return (
    <div className="flex">
      {/* Sidebar */}
      <Sidebar />

      {/* Main Content */}
      <div className="ml-64 p-8 w-full bg-blue-200 min-h-screen flex justify-center items-center">
        <div className="bg-white p-6 rounded-lg shadow-lg w-full max-w-md">
          <h2 className="text-2xl font-bold mb-4 text-gray-800">Top Up Balance</h2>

          <input
            type="number"
            name='amount'
            placeholder="Amount"
            value={topupInfo.amount}
            onChange={handleChange}
            className="w-full mb-4 p-2 border rounded"
          />
          <input
            type="text"
            name='cardNumber'
            placeholder="Card Number"
            value={topupInfo.cardNumber}
            onChange={handleChange}
            className="w-full mb-4 p-2 border rounded"
          />
          <input
            type="text"
            name='cvv'
            placeholder="CVV"
            value={topupInfo.cvv}
            onChange={handleChange}
            className="w-full mb-4 p-2 border rounded"
          />
          <input
            type="text"
            name='expiryDate'
            placeholder="Expiry Date (MM/YY)"
            value={topupInfo.expiryDate}
            onChange={handleChange}
            className="w-full mb-4 p-2 border rounded"
          />

          <button
            onClick={handleTopUp}
            className="w-full bg-blue-500 text-white p-3 rounded"
          >
            Top Up
          </button>

          {message && <p className="mt-4 text-center">{message}</p>}
        </div>
      </div>
    </div>
  );
}

export default TopUpPage;
