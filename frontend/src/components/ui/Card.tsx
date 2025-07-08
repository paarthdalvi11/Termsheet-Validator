import React, { ReactNode } from 'react';

interface CardProps {
  children: ReactNode;
  className?: string;
  bgColor?: string;
}

const Card: React.FC<CardProps> = ({ children, className = '', bgColor = 'bg-gray-50' }) => {
  return (
    <div className={`${bgColor} p-6 rounded-lg shadow-sm ${className}`}>
      {children}
    </div>
  );
};

export default Card;