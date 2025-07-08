import React, { useState } from 'react';

interface TableColumn {
  key: string;
  header: string;
  width?: string;
  editable?: boolean;
}

interface TableProps {
  columns: TableColumn[];
  data: Record<string, any>[];
  onRowUpdate?: (rowIndex: number, rowData: Record<string, any>) => void;
  actionRenderer?: (row: Record<string, any>, rowIndex: number) => React.ReactNode;
}

const Table: React.FC<TableProps> = ({
  columns,
  data,
  onRowUpdate,
  actionRenderer,
}) => {
  const [editingCell, setEditingCell] = useState<{ rowIndex: number; columnKey: string } | null>(null);
  const [editValue, setEditValue] = useState<string>('');

  const handleCellClick = (rowIndex: number, columnKey: string, value: string, editable?: boolean) => {
    if (!editable || !onRowUpdate) return;
    
    setEditingCell({ rowIndex, columnKey });
    setEditValue(value);
  };

  const handleCellBlur = () => {
    if (!editingCell || !onRowUpdate) return;
    
    const { rowIndex, columnKey } = editingCell;
    const updatedRow = { ...data[rowIndex], [columnKey]: editValue };
    onRowUpdate(rowIndex, updatedRow);
    setEditingCell(null);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleCellBlur();
    } else if (e.key === 'Escape') {
      setEditingCell(null);
    }
  };

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full divide-y divide-gray-200">
        <thead>
          <tr>
            {columns.map((column) => (
              <th
                key={column.key}
                style={{ width: column.width }}
                className="px-6 py-3 text-left text-sm font-medium text-gray-700 tracking-wider"
              >
                {column.header}
              </th>
            ))}
            {actionRenderer && (
              <th className="px-6 py-3 text-right text-sm font-medium text-gray-700 tracking-wider">
                Actions
              </th>
            )}
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {data.map((row, rowIndex) => (
            <tr key={rowIndex} className="hover:bg-gray-50">
              {columns.map((column) => (
                <td key={column.key} className="px-6 py-4 text-sm text-gray-700">
                  {editingCell?.rowIndex === rowIndex && editingCell?.columnKey === column.key ? (
                    <input
                      type="text"
                      value={editValue}
                      onChange={(e) => setEditValue(e.target.value)}
                      onBlur={handleCellBlur}
                      onKeyDown={handleKeyDown}
                      className="w-full px-2 py-1 border border-blue-300 rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500"
                      autoFocus
                    />
                  ) : (
                    <div
                      className={column.editable && onRowUpdate ? 'cursor-pointer px-2 py-1 rounded hover:bg-blue-50' : ''}
                      onClick={() => handleCellClick(rowIndex, column.key, row[column.key], column.editable)}
                    >
                      {row[column.key]}
                    </div>
                  )}
                </td>
              ))}
              {actionRenderer && (
                <td className="px-6 py-4 text-right text-sm">
                  {actionRenderer(row, rowIndex)}
                </td>
              )}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Table;