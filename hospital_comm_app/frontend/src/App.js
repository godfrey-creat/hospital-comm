// src/App.js
import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import LoginForm from './components/LoginForm';
import RegisterForm from './components/RegisterForm';
import DepartmentList from './components/DepartmentList';
import Dashboard from './components/Dashboard';
import { AuthContext } from './components/AuthContext';

function App() {
  const { authToken } = React.useContext(AuthContext);

  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<RegisterAdmin />} />
      <Route
        path="/departments/:id"
        element={authToken ? <Department /> : <Navigate to="/login" />}
      />
      <Route
        path="/messages"
        element={authToken ? <MessageBoard /> : <Navigate to="/login" />}
      />
      <Route
        path="/profile"
        element={authToken ? <UserProfile /> : <Navigate to="/login" />}
      />
      <Route path="/" element={<Navigate to={authToken ? "/profile" : "/login"} />} />
    </Routes>
  );
}

export default App;

