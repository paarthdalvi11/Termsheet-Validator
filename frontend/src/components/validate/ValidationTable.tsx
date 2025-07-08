import React, { useState } from 'react';
import { Edit, Check, X, AlertTriangle, Download } from 'lucide-react';
import Table from '../ui/Table';
import Button from '../ui/Button';
import { ValidationClause } from '../../types';

const ValidationTable: React.FC = () => {
  const [clauses, setClauses] = useState<ValidationClause[]>([
    {
      id: '1',
      clause: 'Payment Terms Section 3.1',
      date: '2025-04-01',
      status: 'Valid',
    },
    {
      id: '2',
      clause: 'Warranty Section 5.2',
      date: '2025-03-28',
      status: 'Invalid',
    },
    {
      id: '3',
      clause: 'Term Length Section 1.3',
      date: '2025-03-25',
      status: 'Warning',
    },
    {
      id: '4',
      clause: 'Confidentiality Section 7.1',
      date: '2025-03-20',
      status: 'Valid',
    },
  ]);

  const columns = [
    { key: 'clause', header: 'Clause', editable: true, width: '40%' },
    { key: 'date', header: 'Date', width: '20%' },
    { key: 'status', header: 'Status', width: '20%' },
  ];

  const handleRowUpdate = (rowIndex: number, updatedRow: ValidationClause) => {
    const newClauses = [...clauses];
    newClauses[rowIndex] = updatedRow;
    setClauses(newClauses);
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'Valid':
        return <Check className="w-4 h-4 text-green-500" />;
      case 'Invalid':
        return <X className="w-4 h-4 text-red-500" />;
      case 'Warning':
        return <AlertTriangle className="w-4 h-4 text-yellow-500" />;
      default:
        return null;
    }
  };

  const renderActions = (row: ValidationClause) => (
    <div className="flex justify-end space-x-2">
      <span className="flex items-center">
        {getStatusIcon(row.status)}
      </span>
      <Button 
        variant="outline" 
        size="sm" 
        className="p-1" 
        aria-label="Edit"
      >
        <Edit className="w-4 h-4" />
      </Button>
    </div>
  );

  return (
    <div>
      <h2 className="text-2xl font-bold mb-6">VALIDATION REPORT</h2>
      <div className="bg-white rounded-lg border border-gray-200 overflow-hidden">
        <Table 
          columns={columns} 
          data={clauses} 
          onRowUpdate={handleRowUpdate}
          actionRenderer={renderActions}
        />
        <div className="flex justify-end p-4">
          <Button className="flex items-center">
            <Download className="w-4 h-4 mr-2" />
            Export Report
          </Button>
        </div>
      </div>
    </div>
  );
};

export default ValidationTable;