'use client';

import { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Upload, FileText, X, Loader2, CheckCircle, AlertCircle } from 'lucide-react';
import { api } from '@/lib/api';
import { cn } from '@/lib/utils';
import { JobStatus } from './JobStatus';

interface UploadedFile {
  file: File;
  status: 'pending' | 'uploading' | 'success' | 'error';
  error?: string;
}

export function FileUpload() {
  const [files, setFiles] = useState<UploadedFile[]>([]);
  const [isUploading, setIsUploading] = useState(false);
  const [currentJobId, setCurrentJobId] = useState<string | null>(null);

  const onDrop = useCallback((acceptedFiles: File[]) => {
    const newFiles = acceptedFiles.map((file) => ({
      file,
      status: 'pending' as const,
    }));
    setFiles((prev) => [...prev, ...newFiles]);
    setCurrentJobId(null);
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
    },
    multiple: true,
  });

  const removeFile = (index: number) => {
    setFiles((prev) => prev.filter((_, i) => i !== index));
  };

  const handleUpload = async () => {
    if (files.length === 0) return;

    setIsUploading(true);
    setFiles((prev) => prev.map((f) => ({ ...f, status: 'uploading' as const })));

    try {
      const filesToUpload = files.map((f) => f.file);
      const response = await api.uploadDocuments(filesToUpload, 'resume');
      
      setFiles((prev) => prev.map((f) => ({ ...f, status: 'success' as const })));
      setCurrentJobId(response.job_id);
    } catch (err) {
      setFiles((prev) =>
        prev.map((f) => ({
          ...f,
          status: 'error' as const,
          error: err instanceof Error ? err.message : 'Upload failed',
        }))
      );
    } finally {
      setIsUploading(false);
    }
  };

  const clearAll = () => {
    setFiles([]);
    setCurrentJobId(null);
  };

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Upload Resumes</CardTitle>
          <CardDescription>
            Upload PDF resumes to analyze and search candidates
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          {/* Dropzone */}
          <div
            {...getRootProps()}
            className={cn(
              'border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition-colors',
              isDragActive
                ? 'border-violet-500 bg-violet-50'
                : 'border-gray-200 hover:border-gray-300 hover:bg-gray-50'
            )}
          >
            <input {...getInputProps()} />
            <div className="flex flex-col items-center gap-3">
              <div className={cn(
                'p-3 rounded-full',
                isDragActive ? 'bg-violet-100' : 'bg-gray-100'
              )}>
                <Upload className={cn(
                  'h-6 w-6',
                  isDragActive ? 'text-violet-600' : 'text-gray-400'
                )} />
              </div>
              <div>
                <p className="font-medium text-gray-700">
                  {isDragActive ? 'Drop files here' : 'Drop PDF files here'}
                </p>
                <p className="text-sm text-gray-500 mt-1">or click to browse</p>
              </div>
            </div>
          </div>

          {/* File List */}
          {files.length > 0 && (
            <div className="space-y-2">
              {files.map((uploadedFile, index) => (
                <div
                  key={index}
                  className="flex items-center gap-3 bg-gray-50 rounded-lg px-4 py-3"
                >
                  <FileText className="h-5 w-5 text-red-500 flex-shrink-0" />
                  <span className="flex-1 text-sm text-gray-700 truncate">
                    {uploadedFile.file.name}
                  </span>
                  <span className="text-xs text-gray-400">
                    {(uploadedFile.file.size / 1024).toFixed(1)} KB
                  </span>
                  
                  {uploadedFile.status === 'pending' && (
                    <Button
                      variant="ghost"
                      size="icon"
                      className="h-8 w-8"
                      onClick={() => removeFile(index)}
                    >
                      <X className="h-4 w-4" />
                    </Button>
                  )}
                  
                  {uploadedFile.status === 'uploading' && (
                    <Loader2 className="h-4 w-4 animate-spin text-violet-600" />
                  )}
                  
                  {uploadedFile.status === 'success' && (
                    <CheckCircle className="h-4 w-4 text-green-500" />
                  )}
                  
                  {uploadedFile.status === 'error' && (
                    <AlertCircle className="h-4 w-4 text-red-500" />
                  )}
                </div>
              ))}
            </div>
          )}

          {/* Actions */}
          {files.length > 0 && !currentJobId && (
            <div className="flex gap-3">
              <Button
                onClick={handleUpload}
                disabled={isUploading}
                className="flex-1 bg-violet-600 hover:bg-violet-700"
              >
                {isUploading ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Uploading...
                  </>
                ) : (
                  <>
                    <Upload className="mr-2 h-4 w-4" />
                    Upload {files.length} file{files.length > 1 ? 's' : ''}
                  </>
                )}
              </Button>
              <Button variant="outline" onClick={clearAll}>
                Clear All
              </Button>
            </div>
          )}

          {/* Upload more button after success */}
          {currentJobId && (
            <Button variant="outline" onClick={clearAll} className="w-full">
              Upload More Files
            </Button>
          )}
        </CardContent>
      </Card>

      {/* Job Status - shows when we have a job */}
      {currentJobId && (
        <Card>
          <CardContent className="pt-6">
            <JobStatus jobId={currentJobId} />
          </CardContent>
        </Card>
      )}
    </div>
  );
}
