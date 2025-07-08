import React from 'react';
import Layout from '../components/layout/Layout';
import ValidationTable from '../components/validate/ValidationTable';

const ValidatePage: React.FC = () => {
  return (
    <Layout title="Term Sheet Validation">
      <div className="bg-gray-50 p-6 rounded-lg">
        <ValidationTable />
      </div>
    </Layout>
  );
};

export default ValidatePage;