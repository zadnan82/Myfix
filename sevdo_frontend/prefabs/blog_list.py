# sevdo_frontend/prefabs/blog_list.py
def render_prefab(args, props):
    # Default values
    title = props.get("title", "Latest Articles")
    subtitle = props.get("subtitle", "Thoughts, tutorials, and insights")
    layout = props.get("layout", "grid")  # grid, list
    posts_per_page = props.get("postsPerPage", 6)
    show_filters = props.get("showFilters", "true")
    show_search = props.get("showSearch", "true")

    # Default categories and sample posts
    categories = props.get(
        "categories",
        ["All", "Web Development", "Tutorial", "Design", "JavaScript", "React"],
    )

    # Check if this is called from .s file with props only (no nested DSL)
    has_dsl_content = args is not None and args.strip() != ""
    show_header = not has_dsl_content  # Only show header if no DSL content

    # Generate JSX content that can be embedded in parent components
    # This generates only the JSX content, not a complete component
    js_template = '''
    <section className="py-12 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">''' + repr(title) + '''</h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">''' + repr(subtitle) + '''</p>
        </div>

        {loading && (
          <div className="text-center">
            <p className="text-lg text-gray-600">Loading posts...</p>
          </div>
        )}

        {error && (
          <div className="text-center">
            <p className="text-lg text-red-600">{error}</p>
          </div>
        )}

        {!loading && !error && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {posts.map((post) => (
              <div key={post.id} className="bg-white rounded-lg shadow-md overflow-hidden">
                <div className="h-48 bg-gray-300"></div>
                <div className="p-6">
                  <h3 className="text-xl font-semibold mb-2">{post.title}</h3>
                  <p className="text-gray-600 mb-4">{post.excerpt}</p>
                  <div className="flex flex-wrap gap-2 mb-4">
                    {post.tags.map((tag, index) => (
                      <span key={index} className="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded">
                        {tag}
                      </span>
                    ))}
                  </div>
                  <div className="text-sm text-gray-500 mb-4">
                    By {post.author_username} • {new Date(post.created_at).toLocaleDateString()}
                  </div>
                  <Link
                    to={`/article/${post.slug}`}
                    className="text-blue-600 hover:text-blue-800 font-medium"
                  >
                    Read more
                  </Link>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </section>'''

    return js_template

# Register with token "bl"
COMPONENT_TOKEN = "bl"

# Add metadata for the frontend compiler to know what imports are needed
PREFAB_METADATA = {
    "imports": [
        "import React, { useState, useEffect } from 'react';",
        "import { Link } from 'react-router-dom';",
        "import axios from 'axios';"
    ],
    "state_variables": [
        "const [posts, setPosts] = useState([]);",
        "const [loading, setLoading] = useState(true);",
        "const [error, setError] = useState(null);"
    ],
    "effects": [
        """useEffect(() => {
    const fetchPosts = async () => {
      try {
        const response = await axios.get('/api/blog/posts');
        setPosts(response.data.posts);
      } catch (err) {
        setError('Failed to load blog posts');
        console.error('Error fetching posts:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchPosts();
  }, []);"""
    ]
}