'use client';

import { useAuth } from '@/hooks/useAuth';
import { useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Upload, MessageSquare, FileText, ArrowRight, Users, Clock, RefreshCw } from 'lucide-react';
import Link from 'next/link';
import { api } from '@/lib/api';

interface Stats {
  resumes: number;
  candidates: number;
  queries: number;
  today: number;
}

export default function DashboardPage() {
  const { isAuthenticated, isLoading } = useAuth();
  const router = useRouter();
  const [stats, setStats] = useState<Stats | null>(null);
  const [statsLoading, setStatsLoading] = useState(true);

  const fetchStats = async () => {
    try {
      setStatsLoading(true);
      const data = await api.getStats();
      setStats(data);
    } catch (err) {
      console.error('Failed to fetch stats:', err);
    } finally {
      setStatsLoading(false);
    }
  };

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.push('/login');
    }
  }, [isAuthenticated, isLoading, router]);

  useEffect(() => {
    if (isAuthenticated) {
      fetchStats();
    }
  }, [isAuthenticated]);

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
    <div className="container mx-auto px-4 py-8 max-w-6xl">
      {/* Welcome */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Welcome back!</h1>
        <p className="text-gray-600">Manage your resumes and find the best candidates.</p>
      </div>

      {/* Quick Actions */}
      <div className="grid md:grid-cols-2 gap-6 mb-8">
        <Card className="hover:shadow-lg transition cursor-pointer" onClick={() => router.push('/upload')}>
          <CardHeader className="flex flex-row items-center gap-4">
            <div className="p-3 bg-violet-100 rounded-xl">
              <Upload className="h-6 w-6 text-violet-600" />
            </div>
            <div>
              <CardTitle className="text-lg">Upload Resumes</CardTitle>
              <CardDescription>Add new PDF resumes to analyze</CardDescription>
            </div>
          </CardHeader>
          <CardContent>
            <Button className="w-full bg-violet-600 hover:bg-violet-700 gap-2">
              Go to Upload
              <ArrowRight className="h-4 w-4" />
            </Button>
          </CardContent>
        </Card>

        <Card className="hover:shadow-lg transition cursor-pointer" onClick={() => router.push('/chat')}>
          <CardHeader className="flex flex-row items-center gap-4">
            <div className="p-3 bg-green-100 rounded-xl">
              <MessageSquare className="h-6 w-6 text-green-600" />
            </div>
            <div>
              <CardTitle className="text-lg">AI Chat</CardTitle>
              <CardDescription>Search candidates with natural language</CardDescription>
            </div>
          </CardHeader>
          <CardContent>
            <Button variant="outline" className="w-full gap-2">
              Start Chatting
              <ArrowRight className="h-4 w-4" />
            </Button>
          </CardContent>
        </Card>
      </div>

      {/* Stats */}
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-semibold text-gray-900">Overview</h2>
        <Button 
          variant="ghost" 
          size="sm" 
          onClick={fetchStats}
          disabled={statsLoading}
          className="gap-2"
        >
          <RefreshCw className={`h-4 w-4 ${statsLoading ? 'animate-spin' : ''}`} />
          Refresh
        </Button>
      </div>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-blue-100 rounded-lg">
                <FileText className="h-5 w-5 text-blue-600" />
              </div>
              <div>
                <p className="text-2xl font-bold text-gray-900">
                  {statsLoading ? '...' : stats?.resumes ?? 0}
                </p>
                <p className="text-sm text-gray-500">Resumes</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-green-100 rounded-lg">
                <Users className="h-5 w-5 text-green-600" />
              </div>
              <div>
                <p className="text-2xl font-bold text-gray-900">
                  {statsLoading ? '...' : stats?.candidates ?? 0}
                </p>
                <p className="text-sm text-gray-500">Candidates</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-purple-100 rounded-lg">
                <MessageSquare className="h-5 w-5 text-purple-600" />
              </div>
              <div>
                <p className="text-2xl font-bold text-gray-900">
                  {statsLoading ? '...' : stats?.queries ?? 0}
                </p>
                <p className="text-sm text-gray-500">Queries</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-orange-100 rounded-lg">
                <Clock className="h-5 w-5 text-orange-600" />
              </div>
              <div>
                <p className="text-2xl font-bold text-gray-900">
                  {statsLoading ? '...' : stats?.today ?? 0}
                </p>
                <p className="text-sm text-gray-500">Today</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Getting Started */}
      {stats && stats.resumes === 0 && (
        <Card className="bg-gray-50 border-dashed">
          <CardContent className="py-8 text-center">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Getting Started</h3>
            <p className="text-gray-600 mb-4 max-w-md mx-auto">
              Upload your first batch of resumes to start finding the best candidates with AI-powered search.
            </p>
            <Link href="/upload">
              <Button className="bg-violet-600 hover:bg-violet-700 gap-2">
                <Upload className="h-4 w-4" />
                Upload Your First Resume
              </Button>
            </Link>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
