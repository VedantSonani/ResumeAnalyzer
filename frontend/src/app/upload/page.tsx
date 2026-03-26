'use client';

import { useAuth } from '@/hooks/useAuth';
import { useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';
import { FileUpload } from '@/components/upload/FileUpload';
import { JobStatus } from '@/components/upload/JobStatus';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { FileText, MessageSquare, ArrowRight, History } from 'lucide-react';
import { Button } from '@/components/ui/button';
import Link from 'next/link';

export default function UploadPage() {
  const { isAuthenticated, isLoading } = useAuth();
  const router = useRouter();
  const [showRecentJobs, setShowRecentJobs] = useState(false);

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.push('/login');
    }
  }, [isAuthenticated, isLoading, router]);

  if (isLoading) {
    return (
      <div className="min-h-[60vh] flex items-center justify-center">
        <div className="animate-pulse text-gray-500">Loading...</div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return null;
  }

  return (
    <div className="container mx-auto px-4 py-8 max-w-5xl">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Upload Resumes</h1>
        <p className="text-gray-600">
          Upload PDF resumes to analyze. Our AI will extract skills, experience, and more.
        </p>
      </div>

      <div className="grid lg:grid-cols-3 gap-6">
        {/* Upload Component */}
        <div className="lg:col-span-2">
          <FileUpload />
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Tips */}
          <Card>
            <CardHeader>
              <CardTitle className="text-base">Tips</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3 text-sm text-gray-600">
              <div className="flex gap-2">
                <FileText className="h-4 w-4 text-violet-600 flex-shrink-0 mt-0.5" />
                <span>PDF format works best for accurate parsing</span>
              </div>
              <div className="flex gap-2">
                <FileText className="h-4 w-4 text-violet-600 flex-shrink-0 mt-0.5" />
                <span>You can upload multiple files at once</span>
              </div>
              <div className="flex gap-2">
                <FileText className="h-4 w-4 text-violet-600 flex-shrink-0 mt-0.5" />
                <span>Track progress in real-time below</span>
              </div>
            </CardContent>
          </Card>

          {/* Next Step */}
          <Card className="bg-violet-50 border-violet-200">
            <CardHeader>
              <CardTitle className="text-base flex items-center gap-2">
                <MessageSquare className="h-4 w-4 text-violet-600" />
                Next: Search Candidates
              </CardTitle>
              <CardDescription>
                After processing, use AI chat to find the best matches
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Link href="/chat">
                <Button variant="outline" className="w-full gap-2">
                  Go to Chat
                  <ArrowRight className="h-4 w-4" />
                </Button>
              </Link>
            </CardContent>
          </Card>

          {/* Recent Jobs Toggle */}
          <Button 
            variant="ghost" 
            className="w-full gap-2 text-gray-600"
            onClick={() => setShowRecentJobs(!showRecentJobs)}
          >
            <History className="h-4 w-4" />
            {showRecentJobs ? 'Hide' : 'View'} Recent Jobs
          </Button>
        </div>
      </div>

      {/* Recent Jobs Section - Collapsible */}
      {showRecentJobs && (
        <div className="mt-8">
          <Card>
            <CardHeader>
              <CardTitle>Recent Processing Jobs</CardTitle>
              <CardDescription>
                Track all your resume processing jobs
              </CardDescription>
            </CardHeader>
            <CardContent>
              <JobStatus />
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
}
