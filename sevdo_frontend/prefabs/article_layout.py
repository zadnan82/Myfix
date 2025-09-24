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

    # Generate JSX structure instead of standalone function
    # This ensures the component can be embedded properly
    js_template = '''
    <article className="max-w-4xl mx-auto px-4 py-8">
      <header className="mb-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">''' + repr(title) + '''</h1>
        <div className="flex items-center text-gray-600 mb-4">
          <span className="mr-4">By ''' + repr(author) + '''</span>
          <span className="mr-4">•</span>
          <span className="mr-4">''' + repr(date) + '''</span>
          <span className="mr-4">•</span>
          <span>''' + repr(reading_time) + ''' min read</span>
        </div>
        <div className="h-64 bg-gray-300 rounded-lg mb-6"></div>
      </header>
      <div className="prose prose-lg max-w-none">
        <p>''' + repr(content) + '''</p>
      </div>
    </article>'''

    return js_template

    # Generate React component with proper hooks instead of DOM manipulation
    # Use safe string formatting to avoid f-string conflicts

    # Create the JavaScript template using string concatenation
    js_template = '''
import { useState, useEffect } from 'react';

function ArticleContent() {
    const [articleData, setArticleData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        // Extract slug from URL path
        const path = window.location.pathname;
        const segments = path.split('/');
        let slug = null;

        if (segments.length >= 3 && segments[1] === 'article') {
            slug = segments[2];
        }

        if (!slug) {
            setError('No article specified');
            setLoading(false);
            return;
        }

        // Load article content from backend
        fetch('http://localhost:8000/api/blog/posts/' + encodeURIComponent(slug))
            .then(response => {
                if (!response.ok) {
                    throw new Error('HTTP error! status: ' + response.status);
                }
                return response.json();
            })
            .then(data => {
                setArticleData(data);
                setLoading(false);
                // Update page title
                document.title = data.title + ' | DevInsights';
            })
            .catch(err => {
                console.error('Error loading article:', err);
                setError('Article not found');
                setLoading(false);
            });
    }, []);

    // Define sharing functions
    const shareOnTwitter = (title, url) => {
        const text = 'Check out this article: ' + title;
        window.open('https://twitter.com/intent/tweet?text=' + encodeURIComponent(text) + '&url=' + encodeURIComponent(url), '_blank');
    };

    const shareOnLinkedIn = (url) => {
        window.open('https://www.linkedin.com/sharing/share-offsite/?url=' + encodeURIComponent(url), '_blank');
    };

    const copyArticleLink = () => {
        navigator.clipboard.writeText(window.location.href).then(() => {
            alert('Article link copied to clipboard!');
        }).catch(() => {
            // Fallback for older browsers
            const textArea = document.createElement('textarea');
            textArea.value = window.location.href;
            document.body.appendChild(textArea);
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
            alert('Article link copied to clipboard!');
        });
    };

    if (loading) {
        return (
            <div>
                <nav className="mb-8">
                    <button onClick={() => window.location.href='/blog'}
                            className="inline-flex items-center text-blue-600 hover:text-blue-700 transition-colors duration-200">
                        <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 19l-7-7 7-7"></path>
                        </svg>
                        ← Back to Blog
                    </button>
                </nav>

                <div className="text-center py-12">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
                    <p className="text-gray-600">Loading article...</p>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div>
                <nav className="mb-8">
                    <button onClick={() => window.location.href='/blog'}
                            className="inline-flex items-center text-blue-600 hover:text-blue-700 transition-colors duration-200">
                        <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 19l-7-7 7-7"></path>
                        </svg>
                        ← Back to Blog
                    </button>
                </nav>

                <div className="text-center py-12">
                    <div className="text-red-400 mb-4">
                        <svg className="w-16 h-16 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.082 16.5c-.77.833.192 2.5 1.732 2.5z"></path>
                        </svg>
                    </div>
                    <h3 className="text-lg font-medium text-gray-900 mb-2">{error}</h3>
                    <p className="text-gray-500 mb-4">The article you're looking for doesn't exist or has been removed.</p>
                    <button onClick={() => window.location.href='/blog'}
                            className="bg-blue-600 hover:bg-blue-700 text-white font-medium px-4 py-2 rounded-lg transition-colors duration-200">
                        ← Back to Blog
                    </button>
                </div>
            </div>
        );
    }

    if (!articleData) return null;

    // Generate tags
    const tagsHtml = articleData.tags && articleData.tags.length > 0 ? (
        <div className="mb-4">
            {articleData.tags.map(articleTag => (
                <span key={articleTag}
                      className="inline-block bg-gray-100 hover:bg-gray-200 text-gray-700 text-sm px-3 py-1 rounded-full mr-2 mb-2 transition-colors cursor-pointer"
                      onClick={() => window.location.href='/blog?tag=' + encodeURIComponent(articleTag)}>
                    {'#' + articleTag}
                </span>
            ))}
        </div>
    ) : null;

    // Generate featured image
    const imageHtml = articleData.featured_image ? (
        <div className="mb-8">
            <img className="w-full h-64 md:h-96 object-cover rounded-lg shadow-md"
                 src={articleData.featured_image}
                 alt={articleData.title} />
        </div>
    ) : null;

    // Format content (split by double newlines for paragraphs)
    const formattedContent = articleData.content
        .split('\\n\\n')
        .map((paragraph, index) => (
            <p key={index} className="mb-4">{paragraph.replace(/\\n/g, <br />)}</p>
        ));

    return (
        <div>
            <nav className="mb-8">
                <button onClick={() => window.location.href='/blog'}
                        className="inline-flex items-center text-blue-600 hover:text-blue-700 transition-colors duration-200">
                    <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 19l-7-7 7-7"></path>
                    </svg>
                    ← Back to Blog
                </button>
            </nav>

            <header className="mb-8">
                {tagsHtml}

                <h1 className="text-3xl md:text-4xl lg:text-5xl font-bold text-gray-900 mb-6 leading-tight">
                    {articleData.title}
                </h1>

                <div className="flex flex-wrap items-center text-gray-600 text-sm mb-6">
                    <div className="flex items-center mr-6 mb-2">
                        <div className="w-8 h-8 bg-gray-300 rounded-full mr-3"></div>
                        <span className="font-medium">{articleData.author_username || 'Anonymous'}</span>
                    </div>

                    <div className="flex items-center mr-6 mb-2">
                        <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                        </svg>
                        <time>{new Date(articleData.created_at).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })}</time>
                    </div>

                    <div className="flex items-center mb-2">
                        <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                        </svg>
                        <span>{articleData.reading_time_minutes || Math.ceil((articleData.word_count || 1000) / 200) || 5} min read</span>
                    </div>
                </div>
            </header>

            {imageHtml}

            <div className="prose prose-lg max-w-none mb-12">
                <div className="text-gray-700 leading-relaxed text-lg">
                    {formattedContent}
                </div>
            </div>

            <footer className="border-t border-gray-200 pt-8">
                <div className="mb-8">
                    <h3 className="text-lg font-semibold text-gray-900 mb-4">Share this article</h3>
                    <div className="flex space-x-4">
                        <button onClick={() => shareOnTwitter(articleData.title, window.location.href)}
                                className="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors duration-200 text-sm">
                            <svg className="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 24 24">
                                <path d="M24 4.557c-.883.392-1.832.656-2.828.775 1.017-.609 1.798-1.574 2.165-2.724-.951.564-2.005.974-3.127 1.195-.897-.957-2.178-1.555-3.594-1.555-3.179 0-5.515 2.966-4.797 6.045-4.091-.205-7.719-2.165-10.148-5.144-1.29 2.213-.669 5.108 1.523 6.574-.806-.026-1.566-.247-2.229-.616-.054 2.281 1.581 4.415 3.949 4.89-.693.188-1.452.232-2.224.084.626 1.956 2.444 3.379 4.6 3.419-2.07 1.623-4.678 2.348-7.29 2.04 2.179 1.397 4.768 2.212 7.548 2.212 9.142 0 14.307-7.721 13.995-14.646.962-.695 1.797-1.562 2.457-2.549z"/>
                            </svg>
                            Twitter
                        </button>

                        <button onClick={() => shareOnLinkedIn(window.location.href)}
                                className="inline-flex items-center px-4 py-2 bg-blue-800 text-white rounded-lg hover:bg-blue-900 transition-colors duration-200 text-sm">
                            <svg className="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 24 24">
                                <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
                            </svg>
                            LinkedIn
                        </button>

                        <button onClick={copyArticleLink}
                                className="inline-flex items-center px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors duration-200 text-sm">
                            <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.367 2.684 3 3 0 00-5.367-2.684z"></path>
                            </svg>
                            Copy Link
                        </button>
                    </div>
                </div>
            </footer>
        </div>
    );
}

export default function Article() {
    return (
        <article className="max-w-4xl mx-auto px-4 py-8">
            <ArticleContent />
        </article>
    );
}'''

    return js_template


# Register with token "al"
COMPONENT_TOKEN = "al"