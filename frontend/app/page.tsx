import Link from 'next/link';

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-900 to-gray-800 text-white">
      <div className="container mx-auto px-4 py-16">
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="text-6xl font-bold mb-6 bg-gradient-to-r from-blue-400 to-purple-600 text-transparent bg-clip-text">
            Steam Game Browser
          </h1>
          <p className="text-xl text-gray-300 mb-12">
            Browse 700+ PC games, read 730,000+ reviews, and find your next adventure
          </p>
          
          <div className="grid md:grid-cols-3 gap-6 mb-12">
            <div className="bg-gray-800 p-6 rounded-lg border border-gray-700">
              <div className="text-4xl mb-2">🎮</div>
              <h3 className="text-xl font-semibold mb-2">Browse Games</h3>
              <p className="text-gray-400">Discover games by genre, price, and more</p>
            </div>
            <div className="bg-gray-800 p-6 rounded-lg border border-gray-700">
              <div className="text-4xl mb-2">⭐</div>
              <h3 className="text-xl font-semibold mb-2">Read Reviews</h3>
              <p className="text-gray-400">See what players really think</p>
            </div>
            <div className="bg-gray-800 p-6 rounded-lg border border-gray-700">
              <div className="text-4xl mb-2">💻</div>
              <h3 className="text-xl font-semibold mb-2">Check Specs</h3>
              <p className="text-gray-400">View system requirements</p>
            </div>
          </div>

          <div className="text-center">
            <Link 
              href="/games"
              className="inline-block px-8 py-3 bg-blue-600 hover:bg-blue-700 rounded-lg font-semibold transition-colors"
            >
              Start Browsing Games
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
