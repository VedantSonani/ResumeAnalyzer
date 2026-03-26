import { FileText, Github, Twitter } from 'lucide-react';
import Link from 'next/link';

export function Footer() {
  return (
    <footer className="border-t bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <div className="flex flex-col md:flex-row items-center justify-between gap-4">
          {/* Logo */}
          <div className="flex items-center gap-2">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-violet-600">
              <FileText className="h-5 w-5 text-white" />
            </div>
            <span className="text-lg font-bold text-gray-900">ResumeLens</span>
          </div>

          {/* Links */}
          <nav className="flex items-center gap-6 text-sm text-gray-600">
            <Link href="/about" className="hover:text-violet-600 transition">
              About
            </Link>
            <Link href="/privacy" className="hover:text-violet-600 transition">
              Privacy
            </Link>
            <Link href="/terms" className="hover:text-violet-600 transition">
              Terms
            </Link>
          </nav>

          {/* Social */}
          <div className="flex items-center gap-4">
            <a href="#" className="text-gray-500 hover:text-gray-900 transition">
              <Github className="h-5 w-5" />
            </a>
            <a href="#" className="text-gray-500 hover:text-gray-900 transition">
              <Twitter className="h-5 w-5" />
            </a>
          </div>
        </div>

        <div className="mt-6 pt-6 border-t text-center text-sm text-gray-500">
          © {new Date().getFullYear()} ResumeLens. All rights reserved.
        </div>
      </div>
    </footer>
  );
}
