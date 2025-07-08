import React from 'react';
import Layout from '../components/layout/Layout';
import FileUploader from '../components/upload/FileUploader';
import PreviousUploads from '../components/upload/PreviousUploads';

const UploadPage: React.FC = () => {
  return (
    <Layout title="Term Sheet Validation">
      <FileUploader />
      <PreviousUploads />
    </Layout>
  );
};

export default UploadPage;