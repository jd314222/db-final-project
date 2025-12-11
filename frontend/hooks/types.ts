// API Types
export interface Game {
  game_id: number;
  game_name: string;
  genre_name?: string;
  price: number;
  discount_percentage: number;
  rating: number;
  total_reviews?: number;
  release_year?: number;
  storage_gb?: number;
  image_url?: string;
}

export interface GameDetail extends Game {
  positive_reviews?: number;
  steam_url?: string;
  system_requirements?: {
    cpu: string | null;
    gpu: string | null;
    ram: string | null;
    storage: string | null;
    os: string | null;
    directx: string | null;
  };
}

export interface Review {
  review_id: number;
  game_id: number;
  game_name: string;
  user_id: number;
  review_text: string;
  sentiment: string;
  hours_played: number;
  date_posted?: string;
}

export interface Genre {
  genre_id: number;
  genre_name: string;
  game_count?: number;
}

export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

export interface GameFilters {
  search?: string;
  genre?: string;
  price_min?: string | number;
  price_max?: string | number;
  budget?: string;
  release_year?: number;
  ordering?: string;
  page?: number;
}

export interface ReviewFilters {
  game_id?: string;
  search?: string;
  sentiment?: string;
  ordering?: string;
  page?: number;
}

export interface User {
  user_id: number;
  budget: number;
}

export interface UserDetail extends User {
  specs?: {
    cpu: string | null;
    gpu: string | null;
    ram: string | null;
  };
  wishlist?: WishlistItem[];
  library?: LibraryItem[];
}

export interface WishlistItem {
  user: number;
  game: Game;
}

export interface LibraryItem {
  user: number;
  game: Game;
  purchase_date: string;
  price_paid: number;
}
