'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { useAuth } from '@/hooks/auth';
import { apiClient } from '@/hooks/api';

export default function RegisterPage() {
  const [budget, setBudget] = useState('100.00');
  const [cpu, setCpu] = useState('');
  const [gpu, setGpu] = useState('');
  const [ram, setRam] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const router = useRouter();
  const { login } = useAuth();

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      // Create user
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/users/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          budget: parseFloat(budget),
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to create user');
      }

      const newUser = await response.json();

      // Create user specs if provided
      if (cpu || gpu || ram) {
        await fetch(`${process.env.NEXT_PUBLIC_API_URL}/user-specs/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            user: newUser.user_id,
            cpu: cpu || null,
            gpu: gpu || null,
            ram: ram || null,
          }),
        });
      }

      // Log the user in
      login(newUser.user_id);
      
      // Redirect to home
      router.push('/');
    } catch (err: any) {
      setError(err.message || 'Failed to create account. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white flex items-center justify-center">
      <div className="max-w-2xl w-full mx-4">
        <div className="bg-gray-800 rounded-lg p-8 border border-gray-700">
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold mb-2">Create Account</h1>
            <p className="text-gray-400">Join to create your gaming wishlist</p>
          </div>

          <form onSubmit={handleRegister} className="space-y-6">
            {/* Budget */}
            <div>
              <label htmlFor="budget" className="block text-sm font-medium mb-2">
                Gaming Budget ($)
              </label>
              <input
                id="budget"
                type="number"
                step="0.01"
                min="0"
                value={budget}
                onChange={(e) => setBudget(e.target.value)}
                placeholder="100.00"
                required
                className="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg focus:border-blue-500 focus:outline-none text-white"
              />
              <p className="text-sm text-gray-400 mt-1">
                Set your gaming budget for game recommendations
              </p>
            </div>

            {/* System Specs */}
            <div className="border-t border-gray-700 pt-6">
              <h3 className="text-lg font-semibold mb-4">System Specifications (Optional)</h3>
              
              <div className="space-y-4">
                <div>
                  <label htmlFor="cpu" className="block text-sm font-medium mb-2">
                    CPU
                  </label>
                  <input
                    id="cpu"
                    type="text"
                    value={cpu}
                    onChange={(e) => setCpu(e.target.value)}
                    placeholder="e.g., Intel Core i7-9700K"
                    className="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg focus:border-blue-500 focus:outline-none text-white placeholder-gray-400"
                  />
                </div>

                <div>
                  <label htmlFor="gpu" className="block text-sm font-medium mb-2">
                    GPU
                  </label>
                  <input
                    id="gpu"
                    type="text"
                    value={gpu}
                    onChange={(e) => setGpu(e.target.value)}
                    placeholder="e.g., NVIDIA GeForce RTX 3070"
                    className="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg focus:border-blue-500 focus:outline-none text-white placeholder-gray-400"
                  />
                </div>

                <div>
                  <label htmlFor="ram" className="block text-sm font-medium mb-2">
                    RAM
                  </label>
                  <input
                    id="ram"
                    type="text"
                    value={ram}
                    onChange={(e) => setRam(e.target.value)}
                    placeholder="e.g., 16GB DDR4"
                    className="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg focus:border-blue-500 focus:outline-none text-white placeholder-gray-400"
                  />
                </div>
              </div>
            </div>

            {error && (
              <div className="bg-red-900/50 border border-red-500 text-red-200 px-4 py-3 rounded">
                {error}
              </div>
            )}

            <button
              type="submit"
              disabled={loading}
              className="w-full px-6 py-3 bg-blue-600 hover:bg-blue-700 rounded-lg font-semibold transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Creating Account...' : 'Create Account'}
            </button>
          </form>

          <div className="mt-6 text-center">
            <p className="text-gray-400">
              Already have an account?{' '}
              <Link href="/login" className="text-blue-400 hover:text-blue-300">
                Login here
              </Link>
            </p>
          </div>

          <div className="mt-4 text-center">
            <Link href="/" className="text-gray-400 hover:text-gray-300 text-sm">
              ← Back to Home
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
