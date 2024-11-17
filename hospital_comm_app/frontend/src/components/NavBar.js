// src/components/NavBar.js
import React from 'react';
import { Link } from 'react-router-dom';

function NavBar() {
    return (
        <nav>
            <ul>
                <li><Link to="/">Dashboard</Link></li>
                {/* Add other links here */}
            </ul>
        </nav>
    );
}

export default NavBar;

