import React from 'react';

const DepartmentList = ({ departments }) => {
  return (
    <div>
      <h3>Departments</h3>
      <ul>
        {departments.map((department) => (
          <li key={department.id}>
            {department.name}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default DepartmentList;

