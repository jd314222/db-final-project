'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useAuth } from '@/hooks/auth';

export default function Navigation() {
  const pathname = usePathname();
  const { userId, isAuthenticated, logout } = useAuth();

  return (
    <nav className="bg-gray-800 border-b border-gray-700">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <Link href="/" className="text-xl font-bold text-white hover:text-blue-400 transition-colors">
            Steam Browser
          </Link>
          
          <div className="flex items-center gap-4">
            <Link 
              href="/games" 
              className={`px-4 py-2 rounded transition-colors ${
                pathname === '/games' 
                  ? 'bg-blue-600 text-white' 
                  : 'text-gray-300 hover:text-white hover:bg-gray-700'
              }`}
            >
              Games
            </Link>
            <Link 
              href="/reviews" 
              className={`px-4 py-2 rounded transition-colors ${
                pathname === '/reviews' 
                  ? 'bg-blue-600 text-white' 
                  : 'text-gray-300 hover:text-white hover:bg-gray-700'
              }`}
            >
              Reviews
            </Link>
            
            {isAuthenticated ? (
              <div className="flex items-center gap-3">
                <Link 
                  href={`/user/${userId}`}
                  className="px-4 py-2 bg-purple-600 hover:bg-purple-700 rounded transition-colors text-white font-semibold"
                >
                  Profile
                </Link>
                <button
                  onClick={logout}
                  className="px-4 py-2 text-gray-300 hover:text-white hover:bg-gray-700 rounded transition-colors"
                >
                  Logout
                </button>
              </div>
            ) : (
              <div className="flex items-center gap-3">
                <Link 
                  href="/register"
                  className="px-4 py-2 bg-green-600 hover:bg-green-700 rounded transition-colors text-white font-semibold"
                >
                  Register
                </Link>
                <Link 
                  href="/login"
                  className="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded transition-colors text-white font-semibold"
                >
                  Login
                </Link>
              </div>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}
