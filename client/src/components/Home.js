import React from 'react';
import { Link } from 'react-router-dom';

function Home() {
  return (
    <div className="bg-green-900 min-h-screen flex items-center justify-center">
      <div className="text-center">
        <h1 className="text-4xl font-bold mb-8 text-white">Welcome to Our Market</h1>
        <div className="space-x-4">
          <Link to="/farmersignup" className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
            Signup as Farmer
          </Link>
          <Link to="/buyersignup" className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded">
            Signup as Buyer
          </Link>
        </div>
      </div>
    </div>
  );
}

export default Home;

