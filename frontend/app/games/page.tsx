'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { apiClient } from '@/hooks/api';
import { useAuth } from '@/hooks/auth';
import type { Game, Genre, GameFilters } from '@/hooks/types';

export default function GamesPage() {
  const router = useRouter();
  const { userId, isAuthenticated } = useAuth();
  const [games, setGames] = useState<Game[]>([]);
  const [genres, setGenres] = useState<Genre[]>([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState<GameFilters>({});
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [addingToWishlist, setAddingToWishlist] = useState<number | null>(null);
  const [wishlistedGames, setWishlistedGames] = useState<Set<number>>(new Set());

  useEffect(() => {
    const fetchGenres = async () => {
      try {
        const data = await apiClient.getGenres();
        setGenres(data.results);
      } catch (error) {
        console.error('Failed to fetch genres:', error);
      }
    };
    fetchGenres();
  }, []);

  useEffect(() => {
    const fetchWishlist = async () => {
      if (isAuthenticated && userId) {
        try {
          const data = await apiClient.getWishlist(userId);
          const gameIds = new Set(data.results.map((item: any) => item.game.game_id));
          setWishlistedGames(gameIds);
        } catch (error) {
          console.error('Failed to fetch wishlist:', error);
        }
      }
    };
    fetchWishlist();
  }, [isAuthenticated, userId]);

  useEffect(() => {
    const fetchGames = async () => {
      setLoading(true);
      try {
        const data = await apiClient.getGames({ ...filters, page });
        setGames(data.results);
        setTotalPages(Math.ceil(data.count / 20));
      } catch (error) {
        console.error('Failed to fetch games:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchGames();
  }, [filters, page]);

  const handleFilterChange = (newFilters: Partial<GameFilters>) => {
    setFilters({ ...filters, ...newFilters });
    setPage(1);
  };

  const handleAddToWishlist = async (gameId: number, e: React.MouseEvent) => {
    e.preventDefault(); // Prevent navigation to game detail
    
    if (!isAuthenticated || !userId) {
      router.push('/login');
      return;
    }
    
    setAddingToWishlist(gameId);
    try {
      await apiClient.addToWishlist(userId, gameId);
      setWishlistedGames(prev => new Set(prev).add(gameId));
    } catch (error: any) {
      // Silently handle errors - already in wishlist or failed
      console.error('Wishlist error:', error);
    } finally {
      setAddingToWishlist(null);
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <div className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-6">Browse Games</h1>
          
          {/* Filters */}
          <div className="bg-gray-800 p-6 rounded-lg space-y-4">
            <div className="grid md:grid-cols-3 gap-4">
              {/* Search */}
              <div>
                <label className="block text-sm font-medium mb-2">Search</label>
                <input
                  type="text"
                  placeholder="Game name..."
                  className="w-full px-3 py-2 bg-gray-700 rounded border border-gray-600 focus:border-blue-500 focus:outline-none"
                  onChange={(e) => handleFilterChange({ search: e.target.value || undefined })}
                />
              </div>

              {/* Min Price */}
              <div>
                <label className="block text-sm font-medium mb-2">Min Price ($)</label>
                <input
                  type="number"
                  placeholder="0"
                  min="0"
                  step="0.01"
                  className="w-full px-3 py-2 bg-gray-700 rounded border border-gray-600 focus:border-blue-500 focus:outline-none"
                  onChange={(e) => handleFilterChange({ price_min: e.target.value ? parseFloat(e.target.value) : undefined })}
                />
              </div>

              {/* Max Price */}
              <div>
                <label className="block text-sm font-medium mb-2">Max Price ($)</label>
                <input
                  type="number"
                  placeholder="100"
                  min="0"
                  step="0.01"
                  className="w-full px-3 py-2 bg-gray-700 rounded border border-gray-600 focus:border-blue-500 focus:outline-none"
                  onChange={(e) => handleFilterChange({ price_max: e.target.value ? parseFloat(e.target.value) : undefined })}
                />
              </div>
            </div>

            {/* Budget Filter */}
            <div>
              <label className="block text-sm font-medium mb-2">Budget</label>
              <select
                className="w-full md:w-64 px-3 py-2 bg-gray-700 rounded border border-gray-600 focus:border-blue-500 focus:outline-none"
                onChange={(e) => handleFilterChange({ budget: e.target.value || undefined })}
              >
                <option value="">Any Budget</option>
                <option value="free">Free</option>
                <option value="under_10">Under $10</option>
                <option value="under_20">Under $20</option>
                <option value="under_30">Under $30</option>
              </select>
            </div>

            {/* System Requirements Filter */}
            <div>
              <label className="block text-sm font-medium mb-2">System Requirements</label>
              <select
                className="w-full md:w-64 px-3 py-2 bg-gray-700 rounded border border-gray-600 focus:border-blue-500 focus:outline-none"
                onChange={(e) => handleFilterChange({ has_requirements: e.target.value || undefined })}
              >
                <option value="">All Games</option>
                <option value="true">Has System Requirements</option>
              </select>
            </div>
          </div>
        </div>

        {/* Games Grid */}
        {loading ? (
          <div className="text-center py-12">
            <div className="text-xl">Loading games...</div>
          </div>
        ) : (
          <>
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
              {games.map((game) => (
                <div 
                  key={game.game_id}
                  className="bg-gray-800 rounded-lg overflow-hidden hover:ring-2 hover:ring-blue-500 transition-all"
                >
                  <Link href={`/games/${game.game_id}`}>
                    {/* Game Image */}
                    <div className="relative w-full h-48 bg-gray-700">
                      <img 
                        src={game.image_url || '/steam_logo.jpg'} 
                        alt={game.game_name}
                        className="w-full h-full object-cover"
                        onError={(e) => {
                          // Fallback to steam logo if image fails to load
                          e.currentTarget.src = '/steam_logo.jpg';
                        }}
                      />
                    </div>
                    
                    <div className="p-6">
                      <h3 className="text-xl font-semibold mb-2 line-clamp-2">{game.game_name}</h3>
                      <div className="flex items-center gap-2 mb-3">
                        <span className="text-2xl font-bold text-blue-400">
                          {game.price === 0 ? 'Free' : `$${game.price}`}
                      </span>
                      {game.discount_percentage > 0 && (
                        <span className="text-sm bg-green-600 px-2 py-1 rounded">
                          -{game.discount_percentage}%
                        </span>
                      )}
                    </div>
                    <div className="text-sm text-gray-400 space-y-1 mb-4">
                      <div>⭐ Rating: {game.rating}/10</div>
                      <div>💬 Reviews: {game.total_reviews?.toLocaleString()}</div>
                      {game.release_year && <div>📅 Released: {game.release_year}</div>}
                    </div>
                  </div>
                </Link>
                <div className="px-6 pb-6">
                  <button
                    onClick={(e) => handleAddToWishlist(game.game_id, e)}
                    disabled={addingToWishlist === game.game_id || wishlistedGames.has(game.game_id)}
                    className="w-full px-4 py-2 bg-purple-600 hover:bg-purple-700 rounded transition-colors disabled:opacity-50 disabled:cursor-not-allowed text-sm font-semibold"
                  >
                    {addingToWishlist === game.game_id 
                      ? '⏳ Adding...' 
                      : wishlistedGames.has(game.game_id)
                      ? '✓ In Wishlist'
                      : '💖 Add to Wishlist'}
                  </button>
                </div>
              </div>
              ))}
            </div>

            {/* Pagination */}
            <div className="flex justify-center gap-2">
              <button
                onClick={() => setPage(p => Math.max(1, p - 1))}
                disabled={page === 1}
                className="px-4 py-2 bg-gray-700 rounded disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-600"
              >
                Previous
              </button>
              <span className="px-4 py-2">
                Page {page} of {totalPages}
              </span>
              <button
                onClick={() => setPage(p => Math.min(totalPages, p + 1))}
                disabled={page === totalPages}
                className="px-4 py-2 bg-gray-700 rounded disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-600"
              >
                Next
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
