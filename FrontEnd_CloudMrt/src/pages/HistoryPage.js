import React, { useEffect, useState } from 'react';
import Sidebar from '../components/Sidebar';

function HistoryPage() {
  const [history, setHistory] = useState([]);

  useEffect(() => {
    const fetchedHistory = [
      { id: 1, date: '2024-01-01', from: 'Station A', to: 'Station B', cost: '$2.50' },
      { id: 2, date: '2024-01-02', from: 'Station B', to: 'Station C', cost: '$3.00' },
      { id: 3, date: '2024-01-03', from: 'Station C', to: 'Station D', cost: '$4.00' },
    ];
    setHistory(fetchedHistory);
  }, []);

  return (
    <div className="flex">
      {/* Sidebar */}
      <Sidebar />

      {/* Main content */}
      <div className="ml-64 p-8 w-full bg-blue-200 min-h-screen">
        <h1 className="text-2xl font-semibold mb-6 text-gray-800">Travel History</h1>

        <div className="bg-white rounded-lg shadow-lg p-6">
          <table className="table-auto w-full">
            <thead>
              <tr>
                <th className="px-4 py-2 text-left text-gray-600">Date</th>
                <th className="px-4 py-2 text-left text-gray-600">From</th>
                <th className="px-4 py-2 text-left text-gray-600">To</th>
                <th className="px-4 py-2 text-left text-gray-600">Cost</th>
              </tr>
            </thead>
            <tbody>
              {history.map((item) => (
                <tr key={item.id} className="border-t border-gray-200">
                  <td className="px-4 py-2">{item.date}</td>
                  <td className="px-4 py-2">{item.from}</td>
                  <td className="px-4 py-2">{item.to}</td>
                  <td className="px-4 py-2">{item.cost}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default HistoryPage;
