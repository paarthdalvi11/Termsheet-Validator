import React, { useState, useRef } from 'react';
import { Upload } from 'lucide-react';
import Button from '../ui/Button';
import Card from '../ui/Card';

const FileUploader: React.FC = () => {
  const [isDragging, setIsDragging] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDragEnter = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  };

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      const file = e.dataTransfer.files[0];
      setSelectedFile(file);
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      const file = e.target.files[0];
      setSelectedFile(file);
    }
  };

  const handleClickUpload = () => {
    fileInputRef.current?.click();
  };

  const handleSubmit = () => {
    // Here you would typically upload the file to a server
    console.log('Uploading file:', selectedFile);
    // Reset the selected file after upload
    setSelectedFile(null);
    // In a real app, you'd add proper upload logic and success/error handling
  };

  return (
    <Card className="text-center">
      <h2 className="text-2xl font-bold mb-8">Upload New Term Sheet</h2>
      
      <div
        className={`
          border-2 border-dashed rounded-lg p-10 mb-6 transition-colors
          ${isDragging ? 'border-blue-500 bg-blue-50' : 'border-gray-300'}
          ${selectedFile ? 'bg-green-50 border-green-300' : ''}
        `}
        onDragEnter={handleDragEnter}
        onDragLeave={handleDragLeave}
        onDragOver={handleDragOver}
        onDrop={handleDrop}
      >
        <input
          type="file"
          className="hidden"
          ref={fileInputRef}
          onChange={handleFileChange}
          accept=".pdf,.doc,.docx,.xls,.xlsx"
        />
        
        <Upload className="w-12 h-12 mx-auto mb-4 text-gray-500" />
        
        {selectedFile ? (
          <div>
            <p className="text-green-600 font-medium mb-1">File selected:</p>
            <p className="mb-4">{selectedFile.name}</p>
          </div>
        ) : (
          <p className="mb-4">Drag and Drop</p>
        )}
        
        <Button
          variant="outline"
          onClick={handleClickUpload}
          className="mx-auto block"
        >
          Browse Files
        </Button>
      </div>
      
      <Button
        disabled={!selectedFile}
        onClick={handleSubmit}
        className={`w-full max-w-xs mx-auto ${!selectedFile ? 'opacity-50 cursor-not-allowed' : ''}`}
      >
        UPLOAD
      </Button>
    </Card>
  );
};

export default FileUploader;