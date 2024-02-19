import { useState } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import FarmerSignUp from './components/FarmerSignup';
import BuyerSignUp from './components/BuyerSignup';
import Home from './components/Home';

function App() {
  const[farmerId,setFamerId]=useState(null)
  const[buyerId,setBuyerId]=useState(null)
  return (
    <div>
    <Router>
      <Routes>
        <Route exact path="/" element={<Home/>}/>
        <Route path="/farmersignup" element={<FarmerSignUp/>}/>
        <Route path="/Buyersignup" element={<BuyerSignUp/>}/>
      </Routes>
      
    </Router> 

    </div>
  );
}

export default App;
