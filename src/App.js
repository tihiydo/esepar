import React from 'react';

import './App.css';

import { Routes, Route } from 'react-router-dom';
import Alerts from './pages/Alerts';
import PointsOfInvincibility from './pages/PointsOfInvincibility';
import Navbar from './navbar/Navbar';

function App() 
{
  return (
    <div>
        <Navbar/>
        <Routes>
            <Route path="/" element={<Alerts />} />
            <Route index element={<Alerts />} />
            <Route path="/alerts" element={<Alerts />} />
            <Route path="/invincibility" element={<PointsOfInvincibility />} />
        </Routes>
    </div>
  );
}

export default App;
