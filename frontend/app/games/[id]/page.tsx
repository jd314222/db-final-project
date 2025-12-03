'use client';

import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import { apiClient } from '@/hooks/api';
import { useAuth } from '@/hooks/auth';
import type { GameDetail, Review } from '@/hooks/types';

export default function GameDetailPage() {
  const params = useParams();
  const router = useRouter();
  const gameId = params.id as string;
  const { userId, isAuthenticated } = useAuth();
  const [game, setGame] = useState<GameDetail | null>(null);
  const [reviews, setReviews] = useState<Review[]>([]);
  const [loading, setLoading] = useState(true);
  const [reviewPage, setReviewPage] = useState(1);
  const [addingToWishlist, setAddingToWishlist] = useState(false);

  useEffect(() => {
    const fetchGameData = async () => {
      setLoading(true);
      try {
        const [gameData, reviewsData] = await Promise.all([
          apiClient.getGame(Number(gameId)),
          apiClient.getReviews({ game_id: gameId, page: reviewPage })
        ]);
        setGame(gameData);
        setReviews(reviewsData.results);
      } catch (error) {
        console.error('Failed to fetch game data:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchGameData();
  }, [gameId, reviewPage]);

  const handleAddToWishlist = async () => {
    if (!isAuthenticated || !userId) {
      router.push('/login');
      return;
    }
    
    setAddingToWishlist(true);
    try {
      await apiClient.addToWishlist(userId, Number(gameId));
      alert('Added to wishlist! View your wishlist in your profile.');
    } catch (error: any) {
      if (error.message.includes('400')) {
        alert('This game is already in your wishlist');
      } else {
        alert('Failed to add to wishlist');
      }
    } finally {
      setAddingToWishlist(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-900 text-white flex items-center justify-center">
        <div className="text-xl">Loading game details...</div>
      </div>
    );
  }

  if (!game) {
    return (
      <div className="min-h-screen bg-gray-900 text-white flex items-center justify-center">
        <div className="text-xl">Game not found</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <div className="container mx-auto px-4 py-8">
        {/* Game Header */}
        <div className="bg-gray-800 rounded-lg p-8 mb-8">
          <h1 className="text-4xl font-bold mb-4">{game.game_name}</h1>
          
          <div className="grid md:grid-cols-2 gap-8">
            <div>
              <div className="mb-4">
                <span className="text-3xl font-bold text-blue-400">
                  {game.price === 0 ? 'Free to Play' : `$${game.price}`}
                </span>
                {game.discount_percentage > 0 && (
                  <span className="ml-3 text-lg bg-green-600 px-3 py-1 rounded">
                    -{game.discount_percentage}% OFF
                  </span>
                )}
              </div>

              <button
                onClick={handleAddToWishlist}
                disabled={addingToWishlist}
                className="mb-6 px-6 py-3 bg-purple-600 hover:bg-purple-700 rounded-lg font-semibold transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
              >
                <span>{addingToWishlist ? '⏳' : '💖'}</span>
                {addingToWishlist ? 'Adding...' : 'Add to Wishlist'}
              </button>

              <div className="space-y-2 text-gray-300">
                <div className="flex items-center gap-2">
                  <span className="font-semibold">⭐ Rating:</span>
                  <span>{game.rating}/10</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="font-semibold">💬 Total Reviews:</span>
                  <span>{game.total_reviews?.toLocaleString()}</span>
                </div>
                {game.positive_reviews !== undefined && (
                  <div className="flex items-center gap-2">
                    <span className="font-semibold">👍 Positive:</span>
                    <span>{game.positive_reviews.toLocaleString()} ({Math.round((game.positive_reviews / (game.total_reviews || 1)) * 100)}%)</span>
                  </div>
                )}
                {game.release_year && (
                  <div className="flex items-center gap-2">
                    <span className="font-semibold">📅 Release Year:</span>
                    <span>{game.release_year}</span>
                  </div>
                )}
                {game.storage_gb && (
                  <div className="flex items-center gap-2">
                    <span className="font-semibold">💾 Storage:</span>
                    <span>{game.storage_gb} GB</span>
                  </div>
                )}
              </div>
            </div>

            {/* System Requirements */}
            {game.system_requirements && (
              <div className="bg-gray-700 p-6 rounded">
                <h2 className="text-xl font-semibold mb-4">System Requirements</h2>
                <div className="space-y-2 text-sm">
                  {game.system_requirements.cpu && (
                    <div>
                      <span className="font-semibold">CPU:</span> {game.system_requirements.cpu}
                    </div>
                  )}
                  {game.system_requirements.gpu && (
                    <div>
                      <span className="font-semibold">GPU:</span> {game.system_requirements.gpu}
                    </div>
                  )}
                  {game.system_requirements.ram && (
                    <div>
                      <span className="font-semibold">RAM:</span> {game.system_requirements.ram}
                    </div>
                  )}
                  {game.system_requirements.storage && (
                    <div>
                      <span className="font-semibold">Storage:</span> {game.system_requirements.storage}
                    </div>
                  )}
                  {game.system_requirements.os && (
                    <div>
                      <span className="font-semibold">OS:</span> {game.system_requirements.os}
                    </div>
                  )}
                  {game.system_requirements.directx && (
                    <div>
                      <span className="font-semibold">DirectX:</span> {game.system_requirements.directx}
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Reviews Section */}
        <div>
          <h2 className="text-2xl font-bold mb-4">User Reviews</h2>
          {reviews.length === 0 ? (
            <div className="bg-gray-800 rounded-lg p-8 text-center text-gray-400">
              No reviews yet for this game.
            </div>
          ) : (
            <div className="space-y-4">
              {reviews.map((review) => (
                <div key={review.review_id} className="bg-gray-800 rounded-lg p-6">
                  <div className="flex items-center justify-between mb-3">
                    <div className="flex items-center gap-3">
                      <span className="font-semibold">{review.user_id}</span>
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
                  <p className="text-gray-300">{review.review_text}</p>
                  {review.date_posted && (
                    <div className="text-sm text-gray-500 mt-2">
                      Posted: {new Date(review.date_posted).toLocaleDateString()}
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
