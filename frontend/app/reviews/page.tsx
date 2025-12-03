'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { apiClient } from '@/hooks/api';
import type { Review, ReviewFilters } from '@/hooks/types';

export default function ReviewsPage() {
  const [reviews, setReviews] = useState<Review[]>([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState<ReviewFilters>({});
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

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

  const handleFilterChange = (newFilters: Partial<ReviewFilters>) => {
    setFilters({ ...filters, ...newFilters });
    setPage(1);
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <div className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-6">Review Hub</h1>
          
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
        </div>

        {/* Reviews List */}
        {loading ? (
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
        )}
      </div>
    </div>
  );
}
