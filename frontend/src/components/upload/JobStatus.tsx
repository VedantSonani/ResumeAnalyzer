'use client';

import { useEffect, useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { api, JobInfo, FileStatus } from '@/lib/api';
import { 
  Loader2, 
  CheckCircle, 
  XCircle, 
  Clock, 
  FileText,
  RefreshCw,
  User
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';

interface JobStatusProps {
  jobId?: string;
  onComplete?: () => void;
}

export function JobStatus({ jobId, onComplete }: JobStatusProps) {
  const [jobs, setJobs] = useState<JobInfo[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [autoRefresh, setAutoRefresh] = useState(true);

  const fetchJobs = async () => {
    try {
      if (jobId) {
        const job = await api.getJobStatus(jobId);
        if (job && !('error' in job)) {
          setJobs([job]);
          // Check if job is complete
          if (job.completed_files + job.failed_files === job.total_files) {
            setAutoRefresh(false);
            onComplete?.();
          }
        }
      } else {
        const allJobs = await api.getJobs();
        setJobs(allJobs);
      }
    } catch (err) {
      console.error('Failed to fetch jobs:', err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchJobs();
    
    // Auto-refresh every 2 seconds while processing
    let interval: NodeJS.Timeout;
    if (autoRefresh) {
      interval = setInterval(fetchJobs, 2000);
    }
    
    return () => {
      if (interval) clearInterval(interval);
    };
  }, [jobId, autoRefresh]);

  const getStatusIcon = (status: FileStatus['status']) => {
    switch (status) {
      case 'queued':
        return <Clock className="h-4 w-4 text-gray-400" />;
      case 'processing':
        return <Loader2 className="h-4 w-4 text-violet-600 animate-spin" />;
      case 'completed':
        return <CheckCircle className="h-4 w-4 text-green-500" />;
      case 'failed':
        return <XCircle className="h-4 w-4 text-red-500" />;
    }
  };

  const getStatusBadge = (status: FileStatus['status']) => {
    const variants: Record<string, string> = {
      queued: 'bg-gray-100 text-gray-600',
      processing: 'bg-violet-100 text-violet-700',
      completed: 'bg-green-100 text-green-700',
      failed: 'bg-red-100 text-red-700',
    };
    return (
      <Badge className={cn('capitalize', variants[status])}>
        {status}
      </Badge>
    );
  };

  if (isLoading && jobs.length === 0) {
    return (
      <div className="flex items-center justify-center py-8 text-gray-500">
        <Loader2 className="h-5 w-5 animate-spin mr-2" />
        Loading...
      </div>
    );
  }

  if (jobs.length === 0) {
    return (
      <div className="text-center py-8 text-gray-500">
        <FileText className="h-8 w-8 mx-auto mb-2 opacity-50" />
        <p>No processing jobs yet</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="font-medium text-gray-900">Processing Status</h3>
        <Button
          variant="ghost"
          size="sm"
          onClick={fetchJobs}
          className="gap-2"
        >
          <RefreshCw className={cn('h-4 w-4', isLoading && 'animate-spin')} />
          Refresh
        </Button>
      </div>

      {jobs.map((job) => {
        const progress = ((job.completed_files + job.failed_files) / job.total_files) * 100;
        const isProcessing = job.completed_files + job.failed_files < job.total_files;

        return (
          <Card key={job.job_id} className="overflow-hidden">
            <CardHeader className="py-3 bg-gray-50 border-b">
              <div className="flex items-center justify-between">
                <CardTitle className="text-sm font-medium flex items-center gap-2">
                  {isProcessing && <Loader2 className="h-4 w-4 animate-spin text-violet-600" />}
                  Job #{job.job_id}
                </CardTitle>
                <div className="flex items-center gap-2 text-sm text-gray-500">
                  <span>{job.completed_files}/{job.total_files} complete</span>
                  {job.failed_files > 0 && (
                    <span className="text-red-500">({job.failed_files} failed)</span>
                  )}
                </div>
              </div>
              
              {/* Progress bar */}
              <div className="w-full bg-gray-200 rounded-full h-1.5 mt-2">
                <div
                  className={cn(
                    'h-1.5 rounded-full transition-all duration-500',
                    job.failed_files > 0 ? 'bg-yellow-500' : 'bg-violet-600'
                  )}
                  style={{ width: `${progress}%` }}
                />
              </div>
            </CardHeader>
            
            <CardContent className="p-0">
              <div className="divide-y">
                {job.files.map((file, idx) => (
                  <div
                    key={idx}
                    className={cn(
                      'flex items-center gap-3 px-4 py-3',
                      file.status === 'processing' && 'bg-violet-50'
                    )}
                  >
                    {getStatusIcon(file.status)}
                    
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium text-gray-900 truncate">
                        {file.filename}
                      </p>
                      {file.candidate_name && (
                        <p className="text-xs text-gray-500 flex items-center gap-1">
                          <User className="h-3 w-3" />
                          {file.candidate_name}
                          {file.chunks_created > 0 && (
                            <span className="text-gray-400">
                              • {file.chunks_created} chunks
                            </span>
                          )}
                        </p>
                      )}
                      {file.error && (
                        <p className="text-xs text-red-500 truncate">{file.error}</p>
                      )}
                    </div>
                    
                    {getStatusBadge(file.status)}
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        );
      })}
    </div>
  );
}
