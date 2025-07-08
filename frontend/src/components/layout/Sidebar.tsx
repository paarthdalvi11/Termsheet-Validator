import React from 'react';
import { NavLink, useLocation } from 'react-router-dom';
import { LayoutDashboard, Upload, CheckSquare } from 'lucide-react';
import { useAuth } from '../../context/AuthContext';

const Sidebar: React.FC = () => {
  const { isAuthenticated } = useAuth();
  const location = useLocation();
  
  const navItems = [
    { 
      path: '/dashboard', 
      label: 'DASHBOARD', 
      icon: <LayoutDashboard className="w-5 h-5 mr-2" /> 
    },
    { 
      path: '/upload', 
      label: 'UPLOAD', 
      icon: <Upload className="w-5 h-5 mr-2" /> 
    },
    { 
      path: '/validate', 
      label: 'VALIDATE', 
      icon: <CheckSquare className="w-5 h-5 mr-2" /> 
    },
  ];

  // Only show navigation items if user is authenticated and not on login page
  if (!isAuthenticated || location.pathname === '/login') {
    return null;
  }

  return (
    <div className="w-40 bg-gray-50 min-h-screen p-4">
      {navItems.map((item) => (
        <NavLink
          key={item.path}
          to={item.path}
          className={({ isActive }) => 
            `flex items-center p-3 my-1 font-medium text-sm transition-colors ${
              isActive
                ? 'bg-blue-100 text-blue-800 rounded'
                : 'text-gray-700 hover:bg-gray-200 rounded'
            }`
          }
        >
          {item.icon}
          {item.label}
        </NavLink>
      ))}
    </div>
  );
};

export default Sidebar;