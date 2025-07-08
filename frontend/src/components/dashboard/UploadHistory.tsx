import React, { useState } from 'react';
import { Edit, Trash2, Eye, FileText, Search, Filter } from 'lucide-react';
import Table from '../ui/Table';
import Button from '../ui/Button';
import { TermSheet } from '../../types';

const UploadHistory: React.FC = () => {
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
    {
      id: '4',
      fileName: 'Partnership Terms',
      uploadDate: '2025-03-20',
      status: 'Validated',
    },
  ]);

  const [searchTerm, setSearchTerm] = useState('');
  const [filterType, setFilterType] = useState('name');

  const columns = [
    { key: 'fileName', header: 'File name', editable: true, width: '40%' },
    { key: 'uploadDate', header: 'Date', width: '20%' },
    { key: 'status', header: 'Status', width: '20%' },
  ];

  const handleRowUpdate = (rowIndex: number, updatedRow: TermSheet) => {
    const newFiles = [...files];
    newFiles[rowIndex] = updatedRow;
    setFiles(newFiles);
  };

  const handleDelete = (id: string) => {
    setFiles(files.filter(file => file.id !== id));
  };

  const filteredFiles = files.filter(file => {
    const searchLower = searchTerm.toLowerCase();
    switch (filterType) {
      case 'name':
        return file.fileName.toLowerCase().includes(searchLower);
      case 'date':
        return file.uploadDate.includes(searchTerm);
      case 'status':
        return file.status.toLowerCase().includes(searchLower);
      default:
        return true;
    }
  });

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
    <div>
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center">
          <FileText className="w-5 h-5 mr-2 text-blue-600" />
          <h2 className="text-xl font-semibold">Upload History</h2>
        </div>
        <div className="flex items-center space-x-2">
          <div className="relative flex items-center">
            <input
              type="text"
              placeholder="Search..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-8 pr-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-300"
            />
            <Search className="w-4 h-4 absolute left-2.5 text-gray-400" />
          </div>
          <select
            value={filterType}
            onChange={(e) => setFilterType(e.target.value)}
            className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-300"
          >
            <option value="name">Filter by Name</option>
            <option value="date">Filter by Date</option>
            <option value="status">Filter by Status</option>
          </select>
        </div>
      </div>
      
      <div className="bg-white rounded-lg border border-gray-200 overflow-hidden">
        <Table 
          columns={columns} 
          data={filteredFiles} 
          onRowUpdate={handleRowUpdate}
          actionRenderer={renderActions}
        />
      </div>
    </div>
  );
};

export default UploadHistory;