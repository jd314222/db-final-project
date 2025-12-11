'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { apiClient } from '@/hooks/api';
import type { Review, ReviewFilters } from '@/hooks/types';

interface AnalyticsData {
  top_reviewed_games?: Array<{
    game_id: number;
    game_name: string;
    total_reviews: number;
    positive_reviews: number;
    rating: number;
  }>;
  best_value_games?: Array<{
    game_id: number;
    game_name: string;
    price: number;
    rating: number;
    total_reviews: number;
    value_score: number;
  }>;
  most_wishlisted_games?: Array<{
    game_id: number;
    game_name: string;
    wishlist_count: number;
    rating: number;
    price: number;
  }>;
}

export default function ReviewsPage() {
  const [reviews, setReviews] = useState<Review[]>([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState<ReviewFilters>({});
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [activeTab, setActiveTab] = useState<'reviews' | 'analytics'>('reviews');
  const [analytics, setAnalytics] = useState<AnalyticsData>({});

  useEffect(() => {
    const fetchReviews = async () => {
      setLoading(true);
      try {
        const data = await apiClient.getReviews({ ...filters, page });
        setReviews(data.results);
        setTotalPages(Math.ceil(data.count / 20));
      } catch (error) {
        console.error('Failed to fetch reviews:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchReviews();
  }, [filters, page]);

  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        const [topReviewed, bestValue, mostWishlisted] = await Promise.all([
          apiClient.getTopReviewedGames(),
          apiClient.getBestValueGames(),
          apiClient.getMostWishlistedGames()
        ]);
        
        console.log('Most wishlisted data:', mostWishlisted);
        
        setAnalytics({
          top_reviewed_games: topReviewed,
          best_value_games: bestValue,
          most_wishlisted_games: mostWishlisted
        });
      } catch (error) {
        console.error('Failed to fetch analytics:', error);
      }
    };
    
    if (activeTab === 'analytics') {
      fetchAnalytics();
    }
  }, [activeTab]);

  const handleFilterChange = (newFilters: Partial<ReviewFilters>) => {
    setFilters({ ...filters, ...newFilters });
    setPage(1);
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <div className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-6">Review Hub</h1>
          
          {/* Tab Navigation */}
          <div className="flex gap-4 mb-6">
            <button
              onClick={() => setActiveTab('reviews')}
              className={`px-6 py-3 rounded-lg font-semibold transition-colors ${
                activeTab === 'reviews'
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
              }`}
            >
              📝 Reviews
            </button>
            <button
              onClick={() => setActiveTab('analytics')}
              className={`px-6 py-3 rounded-lg font-semibold transition-colors ${
                activeTab === 'analytics'
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
              }`}
            >
              📊 Analytics
            </button>
          </div>
          
          {activeTab === 'reviews' && (
            <>
              {/* Filters */}
              <div className="bg-gray-800 p-6 rounded-lg">
                <div className="grid md:grid-cols-3 gap-4">
                  {/* Game Search */}
                  <div>
                    <label className="block text-sm font-medium mb-2">Search Game</label>
                    <input
                      type="text"
                      placeholder="Search by game name..."
                      className="w-full px-3 py-2 bg-gray-700 rounded border border-gray-600 focus:border-blue-500 focus:outline-none"
                      onChange={(e) => handleFilterChange({ search: e.target.value || undefined })}
                    />
                  </div>

                  {/* Sentiment Filter */}
                  <div>
                    <label className="block text-sm font-medium mb-2">Sentiment</label>
                    <select
                      className="w-full px-3 py-2 bg-gray-700 rounded border border-gray-600 focus:border-blue-500 focus:outline-none"
                      onChange={(e) => handleFilterChange({ sentiment: e.target.value || undefined })}
                    >
                      <option value="">All Reviews</option>
                      <option value="Positive">Positive</option>
                      <option value="Negative">Negative</option>
                    </select>
                  </div>

                  {/* Sort By */}
                  <div>
                    <label className="block text-sm font-medium mb-2">Sort By</label>
                    <select
                      className="w-full px-3 py-2 bg-gray-700 rounded border border-gray-600 focus:border-blue-500 focus:outline-none"
                      onChange={(e) => handleFilterChange({ ordering: e.target.value || undefined })}
                    >
                      <option value="-created_at">Newest First</option>
                      <option value="created_at">Oldest First</option>
                      <option value="-author_playtime_forever">Most Hours Played</option>
                      <option value="author_playtime_forever">Least Hours Played</option>
                    </select>
                  </div>
                </div>
              </div>
            </>
          )}
        </div>

        {activeTab === 'reviews' ? (
          /* Reviews List */
          loading ? (
            <div className="text-center py-12">
              <div className="text-xl">Loading reviews...</div>
            </div>
          ) : (
            <>
              <div className="space-y-4 mb-8">
                {reviews.map((review) => (
                  <div key={review.review_id} className="bg-gray-800 rounded-lg p-6">
                    <div className="flex items-center justify-between mb-3">
                      <div className="flex items-center gap-3">
                        <Link 
                          href={`/games/${review.game_id}`}
                          className="font-semibold text-blue-400 hover:text-blue-300"
                        >
                          {review.game_name}
                        </Link>
                        <span className={`px-3 py-1 rounded text-sm ${
                          review.sentiment === 'Positive' 
                            ? 'bg-green-600' 
                            : review.sentiment === 'Negative'
                            ? 'bg-red-600'
                            : 'bg-gray-600'
                        }`}>
                          {review.sentiment}
                        </span>
                      </div>
                      <div className="text-sm text-gray-400">
                        {review.hours_played} hours played
                      </div>
                    </div>
                    <p className="text-gray-300 mb-2">{review.review_text}</p>
                    {review.date_posted && (
                      <div className="text-sm text-gray-500">
                        Posted: {new Date(review.date_posted).toLocaleDateString()}
                      </div>
                    )}
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
          )
        ) : (
          /* Analytics Dashboard */
          <div className="space-y-8">
            {/* Top Reviewed Games */}
            <div className="bg-gray-800 rounded-lg p-6">
              <h2 className="text-2xl font-bold mb-4 flex items-center gap-2">
                <span>🏆</span>
                Top Reviewed Games
              </h2>
              <p className="text-gray-400 mb-4">Games with the most user reviews</p>
              <div className="space-y-3">
                {analytics.top_reviewed_games?.map((game, index) => (
                  <div key={game.game_id} className="flex items-center gap-4 bg-gray-700 p-4 rounded">
                    <div className="text-2xl font-bold text-blue-400 w-8">#{index + 1}</div>
                    <div className="flex-1">
                      <Link href={`/games/${game.game_id}`} className="font-semibold text-lg hover:text-blue-400">
                        {game.game_name}
                      </Link>
                      <div className="text-sm text-gray-400">
                        {game.total_reviews} reviews • {game.positive_reviews} positive • Rating: {game.rating}/10
                      </div>
                    </div>
                  </div>
                )) || <div className="text-gray-500">Loading...</div>}
              </div>
            </div>

            {/* Best Value Games */}
            <div className="bg-gray-800 rounded-lg p-6">
              <h2 className="text-2xl font-bold mb-4 flex items-center gap-2">
                <span>💎</span>
                Best Value Games
              </h2>
              <p className="text-gray-400 mb-4">Highest rated games per dollar spent</p>
              <div className="space-y-3">
                {analytics.best_value_games?.map((game, index) => (
                  <div key={game.game_id} className="flex items-center gap-4 bg-gray-700 p-4 rounded">
                    <div className="text-2xl font-bold text-green-400 w-8">#{index + 1}</div>
                    <div className="flex-1">
                      <Link href={`/games/${game.game_id}`} className="font-semibold text-lg hover:text-blue-400">
                        {game.game_name}
                      </Link>
                      <div className="text-sm text-gray-400">
                        ${game.price} • Rating: {game.rating}/10 • Value Score: {game.value_score.toFixed(2)}
                      </div>
                    </div>
                  </div>
                )) || <div className="text-gray-500">Loading...</div>}
              </div>
            </div>

            {/* Most Wishlisted Games */}
            <div className="bg-gray-800 rounded-lg p-6">
              <h2 className="text-2xl font-bold mb-4 flex items-center gap-2">
                <span>💖</span>
                Most Wishlisted Games
              </h2>
              <p className="text-gray-400 mb-4">Games most frequently added to user wishlists</p>
              <div className="space-y-3">
                {analytics.most_wishlisted_games?.map((game, index) => (
                  <div key={game.game_id} className="flex items-center gap-4 bg-gray-700 p-4 rounded">
                    <div className="text-2xl font-bold text-purple-400 w-8">#{index + 1}</div>
                    <div className="flex-1">
                      <Link href={`/games/${game.game_id}`} className="font-semibold text-lg hover:text-blue-400">
                        {game.game_name}
                      </Link>
                      <div className="text-sm text-gray-400">
                        {game.wishlist_count} wishlists • ${game.price} • Rating: {game.rating}/10
                      </div>
                    </div>
                  </div>
                )) || <div className="text-gray-500">Loading...</div>}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
