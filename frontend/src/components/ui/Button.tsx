import React, { ButtonHTMLAttributes } from 'react';

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'outline';
  size?: 'sm' | 'md' | 'lg';
}

const Button: React.FC<ButtonProps> = ({
  children,
  variant = 'primary',
  size = 'md',
  className = '',
  ...props
}) => {
  const variantClasses = {
    primary: 'bg-blue-500 hover:bg-blue-600 text-white',
    secondary: 'bg-blue-200 hover:bg-blue-300 text-blue-800',
    outline: 'bg-transparent border border-blue-500 text-blue-500 hover:bg-blue-50',
  };

  const sizeClasses = {
    sm: 'text-xs px-3 py-1',
    md: 'text-sm px-4 py-2',
    lg: 'text-base px-5 py-2.5',
  };

  return (
    <button
      className={`
        ${variantClasses[variant]} 
        ${sizeClasses[size]} 
        font-medium rounded-md transition-colors focus:outline-none focus:ring-2 focus:ring-blue-300
        ${className}
      `}
      {...props}
    >
      {children}
    </button>
  );
};

export default Button;