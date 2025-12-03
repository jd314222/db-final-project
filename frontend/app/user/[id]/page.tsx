'use client';

import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import { apiClient } from '@/hooks/api';
import { useAuth } from '@/hooks/auth';

interface WishlistGame {
  user: number;
  game: {
    game_id: number;
    game_name: string;
    genre_name?: string;
    price: number;
    discount_percentage: number;
    rating: number;
    total_reviews?: number;
    release_year?: number;
  };
}

export default function UserProfilePage() {
  const params = useParams();
  const router = useRouter();
  const userId = params.id as string;
  const { userId: authUserId, isAuthenticated } = useAuth();
  const [user, setUser] = useState<any>(null);
  const [wishlist, setWishlist] = useState<WishlistGame[]>([]);
  const [loading, setLoading] = useState(true);
  const [removing, setRemoving] = useState<number | null>(null);

  // Check if user is authenticated and viewing their own profile
  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login');
      return;
    }
    if (authUserId?.toString() !== userId) {
      router.push(`/user/${authUserId}`);
    }
  }, [isAuthenticated, authUserId, userId, router]);

  useEffect(() => {
    const fetchUserData = async () => {
      setLoading(true);
      try {
        const [userData, wishlistData] = await Promise.all([
          apiClient.getUser(Number(userId)),
          apiClient.getWishlist(Number(userId))
        ]);
        setUser(userData);
        setWishlist(wishlistData.results);
      } catch (error) {
        console.error('Failed to fetch user data:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchUserData();
  }, [userId]);

  const handleRemoveFromWishlist = async (gameId: number) => {
    setRemoving(gameId);
    try {
      await apiClient.removeFromWishlist(Number(userId), gameId);
      setWishlist(wishlist.filter(item => item.game.game_id !== gameId));
    } catch (error) {
      console.error('Failed to remove from wishlist:', error);
      alert('Failed to remove game from wishlist');
    } finally {
      setRemoving(null);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-900 text-white flex items-center justify-center">
        <div className="text-xl">Loading user profile...</div>
      </div>
    );
  }

  if (!user) {
    return (
      <div className="min-h-screen bg-gray-900 text-white flex items-center justify-center">
        <div className="text-xl">User not found</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <div className="container mx-auto px-4 py-8">
        {/* User Header */}
        <div className="bg-gray-800 rounded-lg p-8 mb-8">
          <div className="flex items-center gap-6 mb-6">
            <div className="w-20 h-20 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center text-3xl font-bold">
              {userId}
            </div>
            <div>
              <h1 className="text-4xl font-bold mb-2">User #{userId}</h1>
              <div className="text-gray-400">
                Budget: ${user.budget ? Number(user.budget).toFixed(2) : '0.00'}
              </div>
            </div>
          </div>

          {user.specs && (
            <div className="bg-gray-700 p-6 rounded">
              <h2 className="text-xl font-semibold mb-4">System Specifications</h2>
              <div className="grid md:grid-cols-3 gap-4 text-sm">
                {user.specs.cpu && (
                  <div>
                    <span className="font-semibold">CPU:</span> {user.specs.cpu}
                  </div>
                )}
                {user.specs.gpu && (
                  <div>
                    <span className="font-semibold">GPU:</span> {user.specs.gpu}
                  </div>
                )}
                {user.specs.ram && (
                  <div>
                    <span className="font-semibold">RAM:</span> {user.specs.ram}
                  </div>
                )}
              </div>
            </div>
          )}
        </div>

        {/* Wishlist Section */}
        <div>
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-3xl font-bold">Wishlist ({wishlist.length})</h2>
            <Link 
              href="/games"
              className="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors"
            >
              + Add Games
            </Link>
          </div>

          {wishlist.length === 0 ? (
            <div className="bg-gray-800 rounded-lg p-12 text-center">
              <div className="text-6xl mb-4">🎮</div>
              <h3 className="text-xl font-semibold mb-2">Your wishlist is empty</h3>
              <p className="text-gray-400 mb-6">
                Browse games and add them to your wishlist to track them
              </p>
              <Link 
                href="/games"
                className="inline-block px-6 py-3 bg-blue-600 hover:bg-blue-700 rounded-lg font-semibold transition-colors"
              >
                Browse Games
              </Link>
            </div>
          ) : (
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {wishlist.map((item) => (
                <div 
                  key={item.game.game_id}
                  className="bg-gray-800 rounded-lg overflow-hidden flex flex-col"
                >
                  <div className="p-6 flex-1 flex flex-col">
                    <Link 
                      href={`/games/${item.game.game_id}`}
                      className="hover:text-blue-400 transition-colors"
                    >
                      <h3 className="text-xl font-semibold mb-2 line-clamp-2">
                        {item.game.game_name}
                      </h3>
                    </Link>
                    
                    <div className="flex items-center gap-2 mb-3">
                      <span className="text-2xl font-bold text-blue-400">
                        {item.game.price === 0 ? 'Free' : `$${item.game.price}`}
                      </span>
                      {item.game.discount_percentage > 0 && (
                        <span className="text-sm bg-green-600 px-2 py-1 rounded">
                          -{item.game.discount_percentage}%
                        </span>
                      )}
                    </div>

                    <div className="text-sm text-gray-400 space-y-1 mb-4 flex-1">
                      {item.game.genre_name && (
                        <div>🎯 {item.game.genre_name}</div>
                      )}
                      <div>⭐ Rating: {item.game.rating}/10</div>
                      {item.game.release_year && (
                        <div>📅 {item.game.release_year}</div>
                      )}
                    </div>

                    <button
                      onClick={() => handleRemoveFromWishlist(item.game.game_id)}
                      disabled={removing === item.game.game_id}
                      className="w-full px-4 py-2 bg-red-600 hover:bg-red-700 rounded disabled:opacity-50 disabled:cursor-not-allowed transition-colors mt-auto"
                    >
                      {removing === item.game.game_id ? 'Removing...' : 'Remove from Wishlist'}
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
