import React, { useState } from 'react';
import { topUpBalance } from '../services/api';
import Sidebar from '../components/Sidebar';

function TopUpPage() {
  const [amount, setAmount] = useState('');
  const [cardName, setCardName] = useState('');
  const [cardNumber, setCardNumber] = useState('');
  const [cvv, setCvv] = useState('');
  const [expiryDate, setExpiryDate] = useState(''); // Combined field for month/year
  const [message, setMessage] = useState('');

  const handleTopUp = async () => {
    try {
      const [expiryMonth, expiryYear] = expiryDate.split('/'); // Split the MM/YY format
      const response = await topUpBalance({
        amount,
        cardName,
        cardNumber,
        cvv,
        expiryMonth,
        expiryYear,
      });
      setMessage(response.data.message);
    } catch (error) {
      setMessage('Error: Unable to top up balance.');
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
            placeholder="Amount"
            value={amount}
            onChange={(e) => setAmount(e.target.value)}
            className="w-full mb-4 p-2 border rounded"
          />
          <input
            type="text"
            placeholder="Card Name"
            value={cardName}
            onChange={(e) => setCardName(e.target.value)}
            className="w-full mb-4 p-2 border rounded"
          />
          <input
            type="text"
            placeholder="Card Number"
            value={cardNumber}
            onChange={(e) => setCardNumber(e.target.value)}
            className="w-full mb-4 p-2 border rounded"
          />
          <input
            type="text"
            placeholder="CVV"
            value={cvv}
            onChange={(e) => setCvv(e.target.value)}
            className="w-full mb-4 p-2 border rounded"
          />
          <input
            type="text"
            placeholder="Expiry Date (MM/YY)"
            value={expiryDate}
            onChange={(e) => setExpiryDate(e.target.value)}
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
