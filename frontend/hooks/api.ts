import { Game, GameDetail, Review, Genre, PaginatedResponse, GameFilters, ReviewFilters } from './types';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

class APIClient {
  private baseURL: string;

  constructor(baseURL: string) {
    this.baseURL = baseURL;
  }

  private async request<T>(endpoint: string, options?: RequestInit): Promise<T> {
    const url = `${this.baseURL}${endpoint}`;
    
    try {
      const response = await fetch(url, {
        ...options,
        headers: {
          'Content-Type': 'application/json',
          ...options?.headers,
        },
      });

      if (!response.ok) {
        throw new Error(`API Error: ${response.status} ${response.statusText}`);
      }

      // Handle empty responses (e.g., 204 No Content for DELETE)
      const text = await response.text();
      return text ? JSON.parse(text) : {} as T;
    } catch (error) {
      console.error('API Request failed:', error);
      throw error;
    }
  }

  // Games
  async getGames(filters?: GameFilters): Promise<PaginatedResponse<Game>> {
    const params = new URLSearchParams();
    
    if (filters) {
      Object.entries(filters).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
          params.append(key, value.toString());
        }
      });
    }

    const query = params.toString();
    return this.request<PaginatedResponse<Game>>(`/games/${query ? `?${query}` : ''}`);
  }

  async getGame(id: number): Promise<GameDetail> {
    return this.request<GameDetail>(`/games/${id}/`);
  }

  async getGameStats() {
    return this.request<{
      total_games: number;
      avg_price: number;
      games_with_price: number;
    }>('/games/stats/');
  }

  // Reviews
  async getReviews(filters?: ReviewFilters): Promise<PaginatedResponse<Review>> {
    const params = new URLSearchParams();
    
    if (filters) {
      Object.entries(filters).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
          params.append(key, value.toString());
        }
      });
    }

    const query = params.toString();
    return this.request<PaginatedResponse<Review>>(`/reviews/${query ? `?${query}` : ''}`);
  }

  async getReview(id: number): Promise<Review> {
    return this.request<Review>(`/reviews/${id}/`);
  }

  // Genres
  async getGenres(): Promise<PaginatedResponse<Genre>> {
    return this.request<PaginatedResponse<Genre>>('/genres/');
  }

  async getGenre(id: number): Promise<Genre> {
    return this.request<Genre>(`/genres/${id}/`);
  }

  // Users
  async getUser(id: number): Promise<any> {
    return this.request<any>(`/users/${id}/`);
  }

  async getUsers(): Promise<PaginatedResponse<any>> {
    return this.request<PaginatedResponse<any>>('/users/');
  }

  // Wishlist
  async getWishlist(userId?: number): Promise<PaginatedResponse<any>> {
    const endpoint = userId ? `/wishlist/?user=${userId}` : '/wishlist/';
    return this.request<PaginatedResponse<any>>(endpoint);
  }

  async addToWishlist(userId: number, gameId: number): Promise<any> {
    return this.request<any>('/wishlist/', {
      method: 'POST',
      body: JSON.stringify({ user: userId, game: gameId }),
    });
  }

  async removeFromWishlist(userId: number, gameId: number): Promise<void> {
    return this.request<void>(`/wishlist/${userId}_${gameId}/`, {
      method: 'DELETE',
    });
  }

  // Analytics
  async getTopReviewedGames(): Promise<any[]> {
    return this.request<any[]>('/analytics/top_reviewed/');
  }

  async getBestValueGames(): Promise<any[]> {
    return this.request<any[]>('/analytics/best_value/');
  }

  async getMostWishlistedGames(): Promise<any[]> {
    return this.request<any[]>('/analytics/most_wishlisted/');
  }
}

export const apiClient = new APIClient(API_URL);
export const api = apiClient;
