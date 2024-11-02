import React, { useEffect, useState } from 'react';
import Sidebar from '../components/Sidebar';

function HistoryPage() {
  const [transactionInfo, setTransactionInfo] = useState([]);
  const [tripInfo, setTripInfo] = useState([]);

  useEffect(() => {
    const fetchHistory = async () => {
      const token = localStorage.getItem('access_token');
      if (!token) {
        console.log('You must log in first.');
        return;
      }

      try {
        // GET TRANSACTION HISTORY
        const transactionResponse = await fetch(`http://localhost/transactions`, {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        });

        if (!transactionResponse.ok) {
          const errorData = await transactionResponse.json();
          throw new Error(errorData.detail || 'Failed to fetch transaction history.');
        }

        const transactionData = await transactionResponse.json();
        setTransactionInfo(transactionData.data.transactions || []); // Fallback to empty array if undefined

        // GET TRIP HISTORY
        const tripResponse = await fetch(`http://localhost/trips`, {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        });

        if (!tripResponse.ok) {
          const errorData = await tripResponse.json();
          throw new Error(errorData.detail || 'Failed to fetch trip history.');
        }

        const tripData = await tripResponse.json();
        setTripInfo(tripData.data.trips || []); // Fallback to empty array if undefined

      } catch (error) {
        console.log('Error fetching history: ' + error.message);
      }
    };
    fetchHistory();
  }, []);

  return (
    <div className="flex">
      {/* Sidebar */}
      <Sidebar />

      {/* Main content */}
      <div className="ml-64 p-8 w-full bg-blue-200 min-h-screen">
        <h1 className="text-2xl font-semibold mb-6 text-gray-800">Travel History</h1>

        {/* Transaction Table */}
        <div className="bg-white rounded-lg shadow-lg p-6 mb-8">
          <h2 className="text-xl font-semibold mb-4">Transaction History</h2>
          {transactionInfo.length > 0 ? (
            <table className="table-auto w-full">
              <thead>
                <tr>
                  <th className="px-4 py-2 text-left text-gray-600">Transaction ID</th>
                  <th className="px-4 py-2 text-left text-gray-600">Amount</th>
                  <th className="px-4 py-2 text-left text-gray-600">Timestamp</th>
                </tr>
              </thead>
              <tbody>
                {transactionInfo.map((transaction) => (
                  <tr key={transaction.transactionId}>
                    <td className="px-4 py-2">{transaction.transactionId}</td>
                    <td className="px-4 py-2">
                      {transaction.amount !== undefined ? `$${transaction.amount.toFixed(2)}` : 'N/A'}
                    </td>
                    <td className="px-4 py-2">{new Date(transaction.timestamp).toLocaleString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <p className="text-gray-600">No transaction history yet.</p>
          )}
        </div>

        {/* Trip Table */}
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h2 className="text-xl font-semibold mb-4">Trip History</h2>
          {tripInfo.length > 0 ? (
            <table className="table-auto w-full">
              <thead>
                <tr>
                  <th className="px-4 py-2 text-left text-gray-600">Trip ID</th>
                  <th className="px-4 py-2 text-left text-gray-600">Entry</th>
                  <th className="px-4 py-2 text-left text-gray-600">Exit</th>
                  <th className="px-4 py-2 text-left text-gray-600">Timestamp</th>
                </tr>
              </thead>
              <tbody>
                {tripInfo.map((trip) => (
                  <tr key={trip.tripId}>
                    <td className="px-4 py-2">{trip.tripId}</td>
                    <td className="px-4 py-2">{trip.entry}</td>
                    <td className="px-4 py-2">{trip.exit}</td>
                    <td className="px-4 py-2">{new Date(trip.timestamp).toLocaleString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <p className="text-gray-600">No trip history yet.</p>
          )}
        </div>
      </div>
    </div>
  );
}

export default HistoryPage;
