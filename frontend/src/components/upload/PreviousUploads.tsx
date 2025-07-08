import React, { useState } from 'react';
import { Edit, Trash2, Eye } from 'lucide-react';
import Table from '../ui/Table';
import Button from '../ui/Button';
import { TermSheet } from '../../types';

const PreviousUploads: React.FC = () => {
  const [files, setFiles] = useState<TermSheet[]>([
    {
      id: '1',
      fileName: 'Term Sheet 2025-A',
      uploadDate: '2025-04-01',
      status: 'Validated',
    },
    {
      id: '2',
      fileName: 'Financial Terms Q1',
      uploadDate: '2025-03-28',
      status: 'Error',
    },
    {
      id: '3',
      fileName: 'Contract Agreement',
      uploadDate: '2025-03-25',
      status: 'Pending',
    },
  ]);

  const columns = [
    { key: 'fileName', header: 'File name', editable: true },
    { key: 'uploadDate', header: 'Date' },
    { key: 'status', header: 'Status' },
  ];

  const handleRowUpdate = (rowIndex: number, updatedRow: TermSheet) => {
    const newFiles = [...files];
    newFiles[rowIndex] = updatedRow;
    setFiles(newFiles);
  };

  const handleDelete = (id: string) => {
    setFiles(files.filter(file => file.id !== id));
  };

  const renderActions = (row: TermSheet) => (
    <div className="flex justify-end space-x-2">
      <Button 
        variant="outline" 
        size="sm" 
        className="p-1" 
        aria-label="View"
      >
        <Eye className="w-4 h-4" />
      </Button>
      <Button 
        variant="outline" 
        size="sm" 
        className="p-1" 
        aria-label="Edit"
      >
        <Edit className="w-4 h-4" />
      </Button>
      <Button 
        variant="outline" 
        size="sm" 
        className="p-1 text-red-500 hover:bg-red-50" 
        aria-label="Delete"
        onClick={() => handleDelete(row.id)}
      >
        <Trash2 className="w-4 h-4" />
      </Button>
    </div>
  );

  return (
    <div className="mt-12">
      <h2 className="text-xl font-semibold mb-4">View Previous Uploads</h2>
      <div className="bg-white rounded-lg border border-gray-200 overflow-hidden">
        <Table 
          columns={columns} 
          data={files} 
          onRowUpdate={handleRowUpdate}
          actionRenderer={renderActions}
        />
      </div>
    </div>
  );
};

export default PreviousUploads;