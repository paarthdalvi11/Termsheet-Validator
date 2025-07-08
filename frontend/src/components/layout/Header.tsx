import React from 'react';
import { UserCircle, LogOut } from 'lucide-react';
import { useAuth } from '../../context/AuthContext';

interface HeaderProps {
  title: string;
}

const Header: React.FC<HeaderProps> = ({ title }) => {
  const { user, logout } = useAuth();

  return (
    <div className="bg-blue-100 p-4 flex justify-between items-center">
      <h1 className="text-xl font-bold">{title}</h1>
      <div className="flex items-center">
        {user ? (
          <>
            <div className="flex flex-col items-end mr-4 text-right">
              <span className="font-medium">{user.name}</span>
              <span className="text-sm text-gray-600">{user.role}</span>
            </div>
            <UserCircle className="w-6 h-6 text-gray-700" />
            <button 
              onClick={logout} 
              className="ml-4 p-2 rounded-full hover:bg-blue-200 transition-colors"
              aria-label="Logout"
            >
              <LogOut className="w-5 h-5 text-gray-700" />
            </button>
          </>
        ) : (
          <div className="flex items-center">
            <UserCircle className="w-6 h-6 text-gray-700" />
          </div>
        )}
      </div>
    </div>
  );
};

export default Header;