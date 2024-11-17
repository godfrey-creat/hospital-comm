// src/components/DepartmentMessages.js
import React from 'react';
import { useParams } from 'react-router-dom';

function DepartmentMessages() {
    const { departmentId } = useParams();

    return (
        <div>
            <h1>Messages with {departmentId} Department</h1>
            {/* Display and send messages here */}
        </div>
    );
}

export default DepartmentMessages;

