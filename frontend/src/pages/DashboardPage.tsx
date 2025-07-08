import React from 'react';
import { useNavigate } from 'react-router-dom';
import Layout from '../components/layout/Layout';
import DashboardStats from '../components/dashboard/DashboardStats';
import UploadHistory from '../components/dashboard/UploadHistory';
import Button from '../components/ui/Button';

const DashboardPage: React.FC = () => {
  const navigate = useNavigate();

  const handleValidateClick = () => {
    navigate('/validate');
  };

  return (
    <Layout title="Term Sheet Validation">
      <DashboardStats />
      
      <div className="flex justify-end mb-6">
        <Button 
          variant="primary" 
          className="flex items-center"
          onClick={handleValidateClick}
        >
          Validate now
        </Button>
      </div>
      
      <UploadHistory />
    </Layout>
  );
};

export default DashboardPage;