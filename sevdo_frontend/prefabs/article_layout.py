# sevdo_frontend/prefabs/article_layout.py
def render_prefab(args, props):
    # Default values (will be overridden by dynamic content)
    title = props.get("title", "Article Title")
    content = props.get("content", "Loading article content...")
    author = props.get("author", "Loading...")
    date = props.get("date", "")
    reading_time = props.get("readingTime", "")
    tags = props.get("tags", [])
    featured_image = props.get("featuredImage", "")

    # Support for nested components (for static content override)
    if args:
        import sys
        import os

        parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if parent_dir not in sys.path:
            sys.path.append(parent_dir)
        from frontend_compiler import parse_dsl, _jsx_for_token

        try:
            nodes = parse_dsl(args)
            if nodes:
                for node in nodes:
                    if node.token == "h" and node.args:
                        title = node.args
                    elif node.token == "t" and node.args:
                        content = node.args
        except Exception:
            title = args if args else title

    # Generate the complete JSX template
    js_template = """
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
    </div>"""

    return js_template


# Register with token "al" (article layout)
COMPONENT_TOKEN = "al"

# Add metadata for the frontend compiler to know what imports are needed
PREFAB_METADATA = {
    "imports": [
        "import React, { useState, useEffect } from 'react';",
        "import { useNavigate, useSearchParams, useParams } from 'react-router-dom';",
    ],
    "state_variables": [
        "const [articleData, setArticleData] = useState(null);",
        "const [articleLoading, setArticleLoading] = useState(true);",
        "const [articleError, setArticleError] = useState(null);",
    ],
    "hooks": [
        "const articleNavigate = useNavigate();",
        "const { slug } = useParams();",
    ],
    "effects": [
        """useEffect(() => {
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
  }, [slug]);""",
        """useEffect(() => {
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
        .split('\\n\\n')
        .map(paragraph => `<p>${paragraph.replace(/\\n/g, '<br>')}</p>`)
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
  }, [articleNavigate]);""",
    ],
}
