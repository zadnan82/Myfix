import React, { useEffect, useState } from 'react';
import { useNavigate, useSearchParams, useParams } from 'react-router-dom';
import { Link } from 'react-router-dom';

export default function Blog_SiteArticlePage() {
  const articleNavigate = useNavigate();
  const [searchParams, setSearchParams] = useSearchParams();
  const { slug } = useParams();
  const navigate = useNavigate();

  const [articleData, setArticleData] = useState(null);
  const [articleLoading, setArticleLoading] = useState(true);
  const [articleError, setArticleError] = useState(null);
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [filteredPosts, setFilteredPosts] = useState([]);

  useEffect(() => {
    if (!slug) {
      setArticleError('No article specified');
      setArticleLoading(false);
      return;
    }

    const fetchArticle = async () => {
      try {
        setArticleLoading(true);
        const response = await fetch(`http://localhost:8000/api/blog/posts/${encodeURIComponent(slug)}`);
        
        if (!response.ok) {
          if (response.status === 404) {
            throw new Error('Article not found');
          }
          throw new Error('Failed to load article');
        }
        
        const data = await response.json();
        setArticleData(data);
        
        // Update page title
        document.title = `${data.title} | DevInsights`;
      } catch (err) {
        console.error('Error loading article:', err);
        setArticleError(err.message || 'Failed to load article');
      } finally {
        setArticleLoading(false);
      }
    };

    fetchArticle();
  }, [slug]);
  useEffect(() => {
    // Define utility functions with article prefix
    window.formatArticleDate = (dateString) => {
      return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      });
    };
    
    window.formatArticleContent = (content) => {
      if (!content) return '';
      return content
        .split('\n\n')
        .map(paragraph => `<p>${paragraph.replace(/\n/g, '<br>')}</p>`)
        .join('');
    };
    
    window.handleArticleTagClick = (tag) => {
      articleNavigate(`/blog?tag=${encodeURIComponent(tag)}`);
    };
    
    window.shareArticleOnTwitter = (title, url) => {
      const text = `Check out this article: ${title}`;
      window.open(`https://twitter.com/intent/tweet?text=${encodeURIComponent(text)}&url=${encodeURIComponent(url)}`, '_blank');
    };
    
    window.shareArticleOnLinkedIn = (url) => {
      window.open(`https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(url)}`, '_blank');
    };
    
    window.copyArticleLink = async () => {
      try {
        await navigator.clipboard.writeText(window.location.href);
        alert('Article link copied to clipboard!');
      } catch (err) {
        const textArea = document.createElement('textarea');
        textArea.value = window.location.href;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);
        alert('Article link copied to clipboard!');
      }
    };
  }, [articleNavigate]);
  useEffect(() => {
    const fetchPosts = async () => {
      try {
        setLoading(true);
        const response = await fetch('http://localhost:8000/api/blog/posts?published=true&include_content=false');
        if (!response.ok) {
          throw new Error('Failed to fetch posts');
        }
        const data = await response.json();
        setPosts(data.posts || []);
        setTotalPages(Math.ceil((data.total || 0) / (data.limit || 10)));
      } catch (err) {
        setError('Failed to load blog posts');
        console.error('Error fetching posts:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchPosts();
  }, []);
  useEffect(() => {
    // Filter posts based on search and category
    let filtered = posts;
    
    // Apply search filter
    if (searchQuery.trim()) {
      filtered = filtered.filter(post =>
        post.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        post.excerpt?.toLowerCase().includes(searchQuery.toLowerCase()) ||
        post.tags.some(tag => tag.toLowerCase().includes(searchQuery.toLowerCase()))
      );
    }
    
    // Apply category filter
    if (selectedCategory !== 'All') {
      filtered = filtered.filter(post =>
        post.tags.includes(selectedCategory)
      );
    }
    
    setFilteredPosts(filtered);
    setCurrentPage(1); // Reset to first page when filtering
  }, [posts, searchQuery, selectedCategory]);
  useEffect(() => {
    // Handle URL params for search and category
    const searchParam = searchParams.get('q');
    const categoryParam = searchParams.get('category') || searchParams.get('tag');
    
    if (searchParam) {
      setSearchQuery(searchParam);
    }
    if (categoryParam) {
      setSelectedCategory(categoryParam);
    }
  }, [searchParams]);
  useEffect(() => {
    // Define navigation and handler functions
    window.navigateToArticle = (slug) => {
      navigate(`/article/${slug}`);
    };
    
    window.handleTagClick = (tag) => {
      setSelectedCategory(tag);
      setSearchParams({ tag: tag });
    };
  }, [navigate, setSelectedCategory, setSearchParams]);

  return (
    <>
      <nav className="bg-white shadow-sm border-b border-gray-200">
  <div className="max-w-6xl mx-auto px-4">
    <div className="flex justify-between items-center py-4">
      <div className="flex items-center">
        <Link to="/" className="text-xl font-bold text-gray-800 hover:text-blue-600 transition-colors duration-200">DevInsights</Link>
      </div>
      <div className="hidden md:flex space-x-1">
        <Link to="/" className="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200">Home</Link>
        <Link to="/blog" className="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200">Blog</Link>
        <Link to="/about" className="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200">About</Link>
        <Link to="/contact" className="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200">Contact</Link>
        <Link to="/admin" className="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200">Admin</Link>
      </div>
      <div className="md:hidden">
        <button className="text-gray-700 hover:text-blue-600 focus:outline-none">
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16M4 18h16"></path>
          </svg>
        </button>
      </div>
    </div>
  </div>
</nav>
      
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto px-4 py-8">
        {/* Navigation */}
        <nav className="mb-8">
          <button 
            onClick={() => articleNavigate('/blog')}
            className="inline-flex items-center text-blue-600 hover:text-blue-700 transition-colors duration-200 font-medium"
          >
            <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 19l-7-7 7-7"></path>
            </svg>
            ← Back to Blog
          </button>
        </nav>

        {articleLoading && (
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <p className="text-gray-600">Loading article...</p>
          </div>
        )}

        {articleError && (
          <div className="text-center py-12">
            <div className="text-red-400 mb-4">
              <svg className="w-16 h-16 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.082 16.5c-.77.833.192 2.5 1.732 2.5z"></path>
              </svg>
            </div>
            <h3 className="text-lg font-medium text-gray-900 mb-2">{articleError}</h3>
            <p className="text-gray-500 mb-4">The article you're looking for doesn't exist or has been removed.</p>
            <button 
              onClick={() => articleNavigate('/blog')}
              className="bg-blue-600 hover:bg-blue-700 text-white font-medium px-4 py-2 rounded-lg transition-colors duration-200"
            >
              ← Back to Blog
            </button>
          </div>
        )}

        {!articleLoading && !articleError && articleData && (
          <article className="bg-white rounded-xl shadow-sm overflow-hidden">
            {/* Featured Image */}
            {articleData.featured_image && (
              <div className="mb-8">
                <img 
                  className="w-full h-64 md:h-96 object-cover rounded-t-xl"
                  src={articleData.featured_image}
                  alt={articleData.title}
                />
              </div>
            )}

            <div className="p-8 md:p-12">
              {/* Tags */}
              {articleData.tags && articleData.tags.length > 0 && (
                <div className="mb-6">
                  <div className="flex flex-wrap gap-2">
                    {articleData.tags.map((tag, index) => (
                      <button
                        key={index}
                        className="inline-block bg-blue-100 hover:bg-blue-200 text-blue-700 text-sm px-3 py-1 rounded-full transition-colors cursor-pointer"
                        onClick={() => window.handleArticleTagClick && window.handleArticleTagClick(tag)}
                      >
                        #{tag}
                      </button>
                    ))}
                  </div>
                </div>
              )}

              {/* Article Header */}
              <header className="mb-8">
                <h1 className="text-3xl md:text-4xl lg:text-5xl font-bold text-gray-900 mb-6 leading-tight">
                  {articleData.title}
                </h1>

                <div className="flex flex-wrap items-center text-gray-600 text-sm mb-6">
                  {/* Author */}
                  <div className="flex items-center mr-6 mb-2">
                    <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full mr-3 flex items-center justify-center">
                      <span className="text-white font-medium text-sm">
                        {articleData.author_username ? articleData.author_username.charAt(0).toUpperCase() : 'A'}
                      </span>
                    </div>
                    <div>
                      <p className="font-medium text-gray-900">{articleData.author_username || 'Anonymous'}</p>
                      <p className="text-gray-500 text-xs">{articleData.author_email || 'Author'}</p>
                    </div>
                  </div>

                  {/* Date */}
                  <div className="flex items-center mr-6 mb-2">
                    <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                    </svg>
                    <time>{window.formatArticleDate && articleData.created_at ? window.formatArticleDate(articleData.created_at) : new Date(articleData.created_at).toLocaleDateString()}</time>
                  </div>

                  {/* Reading Time */}
                  {articleData.reading_time_minutes && (
                    <div className="flex items-center mb-2">
                      <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                      </svg>
                      <span>{articleData.reading_time_minutes} min read</span>
                    </div>
                  )}
                </div>

                {/* Social Share */}
                <div className="flex items-center space-x-4 pb-6 border-b border-gray-200">
                  <span className="text-sm text-gray-500 font-medium">Share:</span>
                  <button
                    onClick={() => window.shareArticleOnTwitter && window.shareArticleOnTwitter(articleData.title, window.location.href)}
                    className="flex items-center space-x-1 text-gray-500 hover:text-blue-500 transition-colors"
                    title="Share on Twitter"
                  >
                    <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M23.953 4.57a10 10 0 01-2.825.775 4.958 4.958 0 002.163-2.723c-.951.555-2.005.959-3.127 1.184a4.92 4.92 0 00-8.384 4.482C7.69 8.095 4.067 6.13 1.64 3.162a4.822 4.822 0 00-.666 2.475c0 1.71.87 3.213 2.188 4.096a4.904 4.904 0 01-2.228-.616v.06a4.923 4.923 0 003.946 4.827 4.996 4.996 0 01-2.212.085 4.936 4.936 0 004.604 3.417 9.867 9.867 0 01-6.102 2.105c-.39 0-.779-.023-1.17-.067a13.995 13.995 0 007.557 2.209c9.053 0 13.998-7.496 13.998-13.985 0-.21 0-.42-.015-.63A9.935 9.935 0 0024 4.59z"/>
                    </svg>
                  </button>
                  <button
                    onClick={() => window.shareArticleOnLinkedIn && window.shareArticleOnLinkedIn(window.location.href)}
                    className="flex items-center space-x-1 text-gray-500 hover:text-blue-600 transition-colors"
                    title="Share on LinkedIn"
                  >
                    <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
                    </svg>
                  </button>
                  <button
                    onClick={() => window.copyArticleLink && window.copyArticleLink()}
                    className="flex items-center space-x-1 text-gray-500 hover:text-green-600 transition-colors"
                    title="Copy link"
                  >
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"></path>
                    </svg>
                  </button>
                </div>
              </header>

              {/* Article Content */}
              <div className="prose prose-lg prose-blue max-w-none">
                {articleData.excerpt && (
                  <div className="text-xl text-gray-600 font-medium mb-8 p-4 bg-gray-50 rounded-lg border-l-4 border-blue-500">
                    {articleData.excerpt}
                  </div>
                )}
                
                <div 
                  className="article-content"
                  dangerouslySetInnerHTML={{ __html: window.formatArticleContent && articleData.content ? window.formatArticleContent(articleData.content) : articleData.content }}
                />
              </div>

              {/* Article Footer */}
              <footer className="mt-12 pt-8 border-t border-gray-200">
                <div className="flex items-center justify-between">
                  <div className="flex items-center">
                    <span className="text-sm text-gray-500 mr-4">
                      Published {window.formatArticleDate && articleData.created_at ? window.formatArticleDate(articleData.created_at) : new Date(articleData.created_at).toLocaleDateString()}
                    </span>
                    {articleData.updated_at !== articleData.created_at && (
                      <span className="text-sm text-gray-500">
                        • Updated {window.formatArticleDate && articleData.updated_at ? window.formatArticleDate(articleData.updated_at) : new Date(articleData.updated_at).toLocaleDateString()}
                      </span>
                    )}
                  </div>
                  
                  {articleData.word_count && (
                    <span className="text-sm text-gray-500">
                      {articleData.word_count} words
                    </span>
                  )}
                </div>
              </footer>
            </div>
          </article>
        )}

        {/* Related Articles or Back to Blog */}
        {!articleLoading && !articleError && (
          <div className="mt-12 text-center">
            <button
              onClick={() => articleNavigate('/blog')}
              className="inline-flex items-center px-6 py-3 border border-gray-300 rounded-lg text-gray-700 bg-white hover:bg-gray-50 transition-colors duration-200"
            >
              <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 19l-7-7 7-7"></path>
              </svg>
              Browse More Articles
            </button>
          </div>
        )}
      </div>
    </div>
      <h1 className="text-3xl md:text-4xl font-bold text-gray-900 text-left">Header</h1>
      
    <section className="py-12 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">'Latest Articles'</h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">'Thoughts, tutorials, and insights'</p>
        </div>

        {/* Search and Filter Section */}
        

        {loading && (
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <p className="text-lg text-gray-600">Loading articles...</p>
          </div>
        )}

        {error && (
          <div className="text-center py-12">
            <div className="bg-red-50 border border-red-200 rounded-lg p-6 max-w-md mx-auto">
              <p className="text-lg text-red-600">{error}</p>
            </div>
          </div>
        )}

        {!loading && !error && filteredPosts.length === 0 && (
          <div className="text-center py-12">
            <div className="text-gray-400 mb-4">
              <svg className="w-16 h-16 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9.172 16.172a4 4 0 015.656 0M9 12h6m-6-4h6m2 5.291A7.962 7.962 0 0112 15c-2.34 0-4.467.881-6.063 2.328C5.203 17.873 5 18.446 5 19v2h14v-2c0-.554-.203-1.127-.937-1.672A7.962 7.962 0 0012 15z"></path>
              </svg>
            </div>
            <h3 className="text-xl font-medium text-gray-900 mb-2">No articles found</h3>
            <p className="text-gray-500">Try adjusting your search or filter criteria.</p>
          </div>
        )}

        {!loading && !error && filteredPosts.length > 0 && (
          <>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mb-12">
              {filteredPosts.map((post) => (
                <article key={post.id} className="bg-white rounded-lg shadow-md hover:shadow-xl transition-all duration-300 overflow-hidden group">
                  {/* Featured Image */}
                  {post.featured_image ? (
                    <div className="h-48 bg-gradient-to-br from-blue-500 to-purple-600 relative overflow-hidden">
                      <img 
                        src={post.featured_image} 
                        alt={post.title}
                        className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                      />
                    </div>
                  ) : (
                    <div className="h-48 bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center">
                      <svg className="w-12 h-12 text-white opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                      </svg>
                    </div>
                  )}

                  <div className="p-6">
                    {/* Tags */}
                    <div className="flex flex-wrap gap-2 mb-3">
                      {post.tags.slice(0, 3).map((tag, index) => (
                        <button
                          key={index} 
                          className="inline-block bg-blue-100 hover:bg-blue-200 text-blue-800 text-xs px-2 py-1 rounded-full transition-colors cursor-pointer"
                          onClick={(e) => {
                            e.preventDefault();
                            e.stopPropagation();
                            window.handleTagClick && window.handleTagClick(tag);
                          }}
                        >
                          #{tag}
                        </button>
                      ))}
                    </div>

                    {/* Title - Clickable */}
                    <h3 
                      className="text-xl font-semibold mb-3 group-hover:text-blue-600 transition-colors cursor-pointer line-clamp-2"
                      onClick={() => window.navigateToArticle && window.navigateToArticle(post.slug)}
                    >
                      {post.title}
                    </h3>

                    {/* Excerpt */}
                    <p className="text-gray-600 mb-4 line-clamp-3">{post.excerpt}</p>

                    {/* Author and Date */}
                    <div className="flex items-center justify-between text-sm text-gray-500 mb-4">
                      <div className="flex items-center">
                        <div className="w-8 h-8 bg-gray-300 rounded-full mr-3 flex items-center justify-center">
                          <span className="text-xs font-medium text-gray-600">
                            {post.author_username ? post.author_username.charAt(0).toUpperCase() : 'A'}
                          </span>
                        </div>
                        <span>By {post.author_username || 'Anonymous'}</span>
                      </div>
                      <time className="flex items-center">
                        <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                        </svg>
                        {new Date(post.created_at).toLocaleDateString()}
                      </time>
                    </div>

                    {/* Read More Button */}
                    <button
                      onClick={() => window.navigateToArticle && window.navigateToArticle(post.slug)}
                      className="inline-flex items-center text-blue-600 hover:text-blue-800 font-medium transition-colors group-hover:translate-x-1 transform duration-200"
                    >
                      Read More
                      <svg className="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5l7 7-7 7"></path>
                      </svg>
                    </button>
                  </div>
                </article>
              ))}
            </div>

            {/* Pagination */}
            {totalPages > 1 && (
              <div className="flex justify-center items-center space-x-2">
                <button
                  onClick={() => setCurrentPage(Math.max(1, currentPage - 1))}
                  disabled={currentPage === 1}
                  className="px-4 py-2 text-sm font-medium text-gray-500 bg-white border border-gray-300 rounded-l-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  Previous
                </button>
                
                {[...Array(Math.min(5, totalPages))].map((_, index) => {
                  const pageNum = Math.max(1, Math.min(totalPages - 4, currentPage - 2)) + index;
                  return (
                    <button
                      key={pageNum}
                      onClick={() => setCurrentPage(pageNum)}
                      className={`px-4 py-2 text-sm font-medium border ${
                        currentPage === pageNum
                          ? 'z-10 bg-blue-50 border-blue-500 text-blue-600'
                          : 'bg-white border-gray-300 text-gray-500 hover:bg-gray-50'
                      }`}
                    >
                      {pageNum}
                    </button>
                  );
                })}

                <button
                  onClick={() => setCurrentPage(Math.min(totalPages, currentPage + 1))}
                  disabled={currentPage === totalPages}
                  className="px-4 py-2 text-sm font-medium text-gray-500 bg-white border border-gray-300 rounded-r-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  Next
                </button>
              </div>
            )}
          </>
        )}
      </div>
    </section>
      <section className="py-20 bg-gradient-to-r from-blue-600 to-purple-600 text-white">
  <div className="max-w-4xl mx-auto px-4 text-center">
    <h2 className="text-4xl md:text-5xl font-bold mb-6">Enjoyed This Article?</h2>
    <p className="text-xl text-blue-100 mb-8">Get more tutorials and insights delivered to your inbox</p>
    <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
      <Link to="/blog" className="bg-white text-blue-600 hover:bg-blue-50 font-bold px-8 py-4 rounded-xl text-lg transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-1">
        Subscribe for Updates
      </Link>
    </div>
  </div>
</section>
    </>
  );
}
