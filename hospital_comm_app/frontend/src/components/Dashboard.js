import React, { useState, useEffect } from 'react';
import { getDepartments } from '../api';
import DepartmentList from './DepartmentList';

const Dashboard = ({ token }) => {
  const [departments, setDepartments] = useState([]);

  useEffect(() => {
    const fetchDepartments = async () => {
      try {
        const response = await getDepartments(token);
        setDepartments(response.data);
      } catch (err) {
        console.error('Error fetching departments:', err);
      }
    };
    fetchDepartments();
  }, [token]);

  return (
    <div>
      <h2>Dashboard</h2>
      <DepartmentList departments={departments} />
    </div>
  );
};

export default Dashboard;

