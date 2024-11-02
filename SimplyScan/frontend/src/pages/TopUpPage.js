import React, { useState, useEffect } from 'react';
import Sidebar from '../components/Sidebar';

function TopUpPage() {
  const [isSuccess, setIsSuccess] = useState(false);
  const [message, setMessage] = useState(''); 
  const [wallet, setWallet] = useState(0);
  const [topupInfo, setTopupInfo] = useState({
    amount: '',
    cardNumber: '',
    cvv: '',
    expiryDate: '', // Combined field for month/year
  });

  const fetchWalletInfo = async () => {
    const token = localStorage.getItem('access_token');
    if (!token) {
      console.log('You must log in first.');
      return;
    }

    try {
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
      setWallet(walletData.data);
    } catch (error) {
      console.log('Error fetching wallet information: ' + error.message);
    }
  };

  useEffect(() => {
    fetchWalletInfo();
  }, []);

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

    // Input validations
    if (!amount || !cardNumber || !cvv || !expiryDate) {
      setMessage('Please fill in all the fields.');
      setIsSuccess(false);
      return;
    }
    if (isNaN(amount) || amount <= 0) {
      setMessage('Amount should be a positive number.');
      setIsSuccess(false);
      return;
    }
    if (cardNumber.length !== 16 || isNaN(cardNumber)) {
      setMessage('Card number must be a 16-digit number.');
      setIsSuccess(false);
      return;
    }

    const [expiryMonth, expiryYear] = expiryDate.split('/'); // Split the MM/YY format

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
        setIsSuccess(true);
        fetchWalletInfo();
      } else {
        const data = await response.json();
        if (typeof data.detail === 'object' && data.detail !== null) {
          setMessage(JSON.stringify(data.detail)); // Format error details if object
        } else {
          setMessage(data.detail); // Assuming it's a string
        }
      }
    } catch (error) {
      console.error('Error:', error);
      setMessage('Failed to top up balance');
    }
  };

  return (
    <div className="flex">
      <Sidebar />
      <div className="ml-64 p-8 w-full bg-blue-200 min-h-screen flex justify-center items-center">
        <div className="bg-white p-6 rounded-lg shadow-lg w-full max-w-md">
          <h2 className="text-2xl font-bold mb-4 text-gray-800">Top Up Balance</h2>
          <h3 className="text-lg font-semibold mb-4 text-gray-800">Current Balance: $ {wallet}</h3>
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

          <p
              className={`mt-4 text-center ${isSuccess ? 'text-green-500' : 'text-red-500'}`}
            >
              {message}
            </p>
        </div>
      </div>
    </div>
  );
}

export default TopUpPage;
