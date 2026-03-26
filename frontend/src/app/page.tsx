import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { 
  FileText, 
  Upload, 
  MessageSquare, 
  Search, 
  Users, 
  Zap,
  ArrowRight,
  CheckCircle
} from 'lucide-react';

const features = [
  {
    icon: Upload,
    title: 'Upload Resumes',
    description: 'Bulk upload PDF resumes. Our AI extracts skills, experience, education, and projects automatically.',
  },
  {
    icon: Search,
    title: 'Semantic Search',
    description: 'Find candidates by skills, experience, or job requirements using natural language queries.',
  },
  {
    icon: MessageSquare,
    title: 'AI Chat',
    description: 'Ask questions like "Find React developers with 3+ years" and get ranked candidate lists.',
  },
  {
    icon: Users,
    title: 'Smart Matching',
    description: 'AI scores and ranks candidates based on job requirements with detailed match analysis.',
  },
];

const steps = [
  { step: '1', title: 'Upload', description: 'Drop your PDF resumes' },
  { step: '2', title: 'Process', description: 'AI extracts structured data' },
  { step: '3', title: 'Search', description: 'Find best candidates instantly' },
];

export default function HomePage() {
  return (
    <div className="flex flex-col">
      {/* Hero */}
      <section className="py-20 px-4">
        <div className="container mx-auto max-w-5xl text-center">
          <div className="inline-flex items-center gap-2 bg-violet-50 text-violet-700 px-4 py-2 rounded-full text-sm font-medium mb-6">
            <Zap className="h-4 w-4" />
            AI-Powered Recruitment
          </div>
          
          <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
            Find the Perfect Candidates
            <span className="text-violet-600"> Instantly</span>
          </h1>
          
          <p className="text-xl text-gray-600 max-w-2xl mx-auto mb-10">
            Upload resumes, ask in natural language, and get AI-ranked candidates 
            with match scores and detailed analysis.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link href="/signup">
              <Button size="lg" className="bg-violet-600 hover:bg-violet-700 gap-2">
                Get Started Free
                <ArrowRight className="h-4 w-4" />
              </Button>
            </Link>
            <Link href="/login">
              <Button size="lg" variant="outline">
                Sign In
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* How it works */}
      <section className="py-16 px-4 bg-gray-50">
        <div className="container mx-auto max-w-5xl">
          <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">
            How It Works
          </h2>
          
          <div className="grid md:grid-cols-3 gap-8">
            {steps.map((item) => (
              <div key={item.step} className="text-center">
                <div className="w-12 h-12 bg-violet-600 text-white rounded-full flex items-center justify-center text-xl font-bold mx-auto mb-4">
                  {item.step}
                </div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">{item.title}</h3>
                <p className="text-gray-600">{item.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="py-20 px-4">
        <div className="container mx-auto max-w-5xl">
          <h2 className="text-3xl font-bold text-center text-gray-900 mb-4">
            Powerful Features
          </h2>
          <p className="text-gray-600 text-center max-w-2xl mx-auto mb-12">
            Everything you need to streamline your recruitment process
          </p>
          
          <div className="grid md:grid-cols-2 gap-6">
            {features.map((feature) => {
              const Icon = feature.icon;
              return (
                <div
                  key={feature.title}
                  className="bg-white border rounded-xl p-6 hover:shadow-lg transition"
                >
                  <div className="w-12 h-12 bg-violet-100 rounded-lg flex items-center justify-center mb-4">
                    <Icon className="h-6 w-6 text-violet-600" />
                  </div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">
                    {feature.title}
                  </h3>
                  <p className="text-gray-600">{feature.description}</p>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-20 px-4 bg-violet-600">
        <div className="container mx-auto max-w-3xl text-center">
          <h2 className="text-3xl font-bold text-white mb-4">
            Ready to Find Your Next Great Hire?
          </h2>
          <p className="text-violet-100 mb-8">
            Start analyzing resumes in minutes. No credit card required.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link href="/signup">
              <Button size="lg" className="bg-white text-violet-600 hover:bg-gray-100 gap-2">
                Start Free Trial
                <ArrowRight className="h-4 w-4" />
              </Button>
            </Link>
          </div>
          
          <div className="flex items-center justify-center gap-6 mt-8 text-violet-100 text-sm">
            <span className="flex items-center gap-2">
              <CheckCircle className="h-4 w-4" />
              Free to start
            </span>
            <span className="flex items-center gap-2">
              <CheckCircle className="h-4 w-4" />
              No credit card
            </span>
            <span className="flex items-center gap-2">
              <CheckCircle className="h-4 w-4" />
              Cancel anytime
            </span>
          </div>
        </div>
      </section>
    </div>
  );
}
