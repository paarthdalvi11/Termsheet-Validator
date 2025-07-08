import React from 'react';
import Layout from '../components/layout/Layout';
import LoginForm from '../components/auth/LoginForm';

const LoginPage: React.FC = () => {
  return (
    <Layout title="Term Sheet Validation">
      <div className="max-w-md mx-auto pt-8">
        <LoginForm />
      </div>
    </Layout>
  );
};

export default LoginPage;