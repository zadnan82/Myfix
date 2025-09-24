# sevdo_frontend/prefabs/admin_post_list.py
def render_prefab(args, props):
    # Default values
    title = props.get("title", "Manage Posts")

    # API configuration
    api_path = props.get("api_path", "/api/admin/blog/posts")

    # Navigation actions
    navigation = props.get("navigation", {})
    back_action = navigation.get("actions", {}).get("admin_back", "/admin")
    create_action = navigation.get("actions", {}).get(
        "admin_create_post", "/admin/editor"
    )

    # Support for nested components
    if args:
        import sys
        import os

        parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if parent_dir not in sys.path:
            sys.path.append(parent_dir)
        from frontend_compiler import parse_dsl

        try:
            nodes = parse_dsl(args)
            if nodes:
                for node in nodes:
                    if node.token == "h" and node.args:
                        title = node.args
        except Exception:
            title = args if args else title

    return f"""<div className="min-h-screen bg-gray-50">
  <header className="bg-white shadow-sm border-b">
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div className="flex justify-between items-center py-4">
        <div className="flex items-center space-x-4">
          <button 
            onClick={{() => window.location.href = '{back_action}'}}
            className="text-gray-500 hover:text-gray-700 p-2 rounded-lg hover:bg-gray-100"
            title="Back to dashboard"
          >
            ←
          </button>
          <div>
            <h1 className="text-2xl font-bold text-gray-900">{title}</h1>
            <p className="text-sm text-gray-500" id="posts-count">Loading posts...</p>
          </div>
        </div>
        <div className="flex items-center space-x-4">
          <button 
            onClick={{() => window.location.href = '{create_action}'}}
            className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors flex items-center space-x-2"
          >
            <span>➕</span>
            <span>New Post</span>
          </button>
        </div>
      </div>
    </div>
  </header>

  <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
    <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6 mb-6">
      <div className="flex flex-col sm:flex-row gap-4">
        <div className="flex-1">
          <input
            type="text"
            id="search-input"
            placeholder="Search posts by title or content..."
            className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            onInput={{() => {{
              clearTimeout(window.searchTimeout);
              window.searchTimeout = setTimeout(() => {{
                window.loadPosts();
              }}, 500);
            }}}}
          />
        </div>
        
        <div>
          <select
            id="status-filter"
            className="border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            onChange={{() => window.loadPosts()}}
          >
            <option value="">All Posts</option>
            <option value="true">Published</option>
            <option value="false">Drafts</option>
          </select>
        </div>
        
        <div>
          <select
            id="sort-filter"
            className="border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            onChange={{() => window.loadPosts()}}
          >
            <option value="created_desc">Newest First</option>
            <option value="created_asc">Oldest First</option>
            <option value="updated_desc">Recently Updated</option>
            <option value="title_asc">Title A-Z</option>
          </select>
        </div>
      </div>
    </div>

    <div id="bulk-actions" className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6 hidden">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <span className="text-sm text-blue-700" id="selected-count">0 posts selected</span>
          <div className="flex space-x-2">
            <button 
              onClick={{() => {{
                const selectedIds = Array.from(document.querySelectorAll('.post-checkbox:checked')).map(cb => cb.value);
                if (selectedIds.length === 0) return;
                if (!window.confirm('Publish ' + selectedIds.length + ' posts?')) return;
                
                Promise.all(selectedIds.map(id => 
                  fetch('{api_path}/' + id, {{
                    method: 'PUT',
                    headers: {{'Content-Type': 'application/json'}},
                    body: JSON.stringify({{published: true}})
                  }})
                )).then(() => {{
                  window.loadPosts();
                  alert('Posts published successfully');
                }});
              }}}}
              className="bg-green-600 hover:bg-green-700 text-white px-3 py-1 rounded text-sm transition-colors"
            >
              Publish
            </button>
            <button 
              onClick={{() => {{
                const selectedIds = Array.from(document.querySelectorAll('.post-checkbox:checked')).map(cb => cb.value);
                if (selectedIds.length === 0) return;
                if (!window.confirm('Unpublish ' + selectedIds.length + ' posts?')) return;
                
                Promise.all(selectedIds.map(id => 
                  fetch('{api_path}/' + id, {{
                    method: 'PUT',
                    headers: {{'Content-Type': 'application/json'}},
                    body: JSON.stringify({{published: false}})
                  }})
                )).then(() => {{
                  window.loadPosts();
                  alert('Posts unpublished successfully');
                }});
              }}}}
              className="bg-yellow-600 hover:bg-yellow-700 text-white px-3 py-1 rounded text-sm transition-colors"
            >
              Unpublish
            </button>
            <button 
              onClick={{() => {{
                const selectedIds = Array.from(document.querySelectorAll('.post-checkbox:checked')).map(cb => cb.value);
                if (selectedIds.length === 0) return;
                if (!window.confirm('Delete ' + selectedIds.length + ' posts? This cannot be undone.')) return;
                
                Promise.all(selectedIds.map(id => 
                  fetch('{api_path}/' + id, {{method: 'DELETE'}})
                )).then(() => {{
                  window.loadPosts();
                  alert('Posts deleted successfully');
                }});
              }}}}
              className="bg-red-600 hover:bg-red-700 text-white px-3 py-1 rounded text-sm transition-colors"
            >
              Delete
            </button>
          </div>
        </div>
        <button 
          onClick={{() => {{
            document.querySelectorAll('.post-checkbox').forEach(cb => cb.checked = false);
            document.getElementById('select-all').checked = false;
            document.getElementById('bulk-actions').classList.add('hidden');
          }}}}
          className="text-blue-600 hover:text-blue-700 text-sm"
        >
          Clear Selection
        </button>
      </div>
    </div>

    <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
      <div className="px-6 py-4 border-b border-gray-100 bg-gray-50">
        <div className="flex items-center">
          <input
            type="checkbox"
            id="select-all"
            className="rounded border-gray-300 text-blue-600 focus:ring-blue-500 mr-4"
            onChange={{() => {{
              const selectAll = document.getElementById('select-all');
              const checkboxes = document.querySelectorAll('.post-checkbox');
              checkboxes.forEach(cb => cb.checked = selectAll.checked);
              
              const selectedCount = selectAll.checked ? checkboxes.length : 0;
              const bulkActions = document.getElementById('bulk-actions');
              const selectedCountEl = document.getElementById('selected-count');
              
              if (selectedCount > 0) {{
                bulkActions.classList.remove('hidden');
                selectedCountEl.textContent = selectedCount + ' posts selected';
              }} else {{
                bulkActions.classList.add('hidden');
              }}
            }}}}
          />
          <span className="text-sm font-medium text-gray-700">Select All</span>
        </div>
      </div>
      
      <div id="posts-table" className="divide-y divide-gray-100">
        <div className="text-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-500">Loading posts...</p>
        </div>
      </div>
    </div>

    <div id="pagination" className="mt-8 flex items-center justify-between">
      <div className="flex items-center space-x-2">
        <span className="text-sm text-gray-700">Show</span>
        <select
          id="per-page"
          className="border border-gray-300 rounded px-2 py-1 text-sm"
          onChange={{() => window.loadPosts()}}
        >
          <option value="10">10</option>
          <option value="25" selected>25</option>
          <option value="50">50</option>
        </select>
        <span className="text-sm text-gray-700">per page</span>
      </div>
      
      <div id="pagination-buttons" className="flex space-x-2">
      </div>
      
      <div className="text-sm text-gray-700" id="pagination-info">
      </div>
    </div>
  </div>

  <img 
    src="data:image/gif;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs=" 
    className="hidden"
    onLoad={{() => {{
      window.currentPage = 1;
      
      window.loadPosts = function(page = 1) {{
        const search = document.getElementById('search-input').value;
        const published = document.getElementById('status-filter').value;
        const sort = document.getElementById('sort-filter').value;
        const limit = parseInt(document.getElementById('per-page').value);
        
        window.currentPage = page;
        
        const params = new URLSearchParams({{
          page: page,
          limit: limit,
          sort: sort
        }});
        
        if (search) params.set('search', search);
        if (published !== '') params.set('published', published);
        
        fetch('{api_path}?' + params)
          .then(response => response.json())
          .then(data => {{
            const container = document.getElementById('posts-table');
            const postsCount = document.getElementById('posts-count');
            const paginationInfo = document.getElementById('pagination-info');
            const paginationButtons = document.getElementById('pagination-buttons');
            
            if (postsCount) {{
              const published = data.posts ? data.posts.filter(p => p.published).length : 0;
              const drafts = data.posts ? data.posts.length - published : 0;
              postsCount.textContent = data.total + ' posts (' + published + ' published, ' + drafts + ' drafts)';
            }}
            
            if (data.posts && data.posts.length > 0) {{
              container.innerHTML = data.posts.map(post => 
                '<div class="flex items-center px-6 py-4 hover:bg-gray-50 transition-colors">' +
                  '<input type="checkbox" class="post-checkbox rounded border-gray-300 text-blue-600 focus:ring-blue-500 mr-4" value="' + post.id + '" onchange="window.updateBulkActions()" />' +
                  '<div class="flex-1 grid grid-cols-1 lg:grid-cols-12 gap-4 items-center">' +
                    '<div class="lg:col-span-6">' +
                      '<h3 class="font-medium text-gray-900 hover:text-blue-600 cursor-pointer line-clamp-1" onclick="window.location.href=\\'/admin/editor/' + post.id + '\\'">' +
                        post.title +
                      '</h3>' +
                      (post.excerpt ? '<p class="text-sm text-gray-500 mt-1 line-clamp-2">' + post.excerpt + '</p>' : '') +
                      '<div class="flex items-center space-x-2 mt-2">' +
                        '<span class="inline-flex items-center px-2 py-1 rounded-full text-xs ' + (post.published ? 'bg-green-100 text-green-700' : 'bg-yellow-100 text-yellow-700') + '">' +
                          (post.published ? 'Published' : 'Draft') +
                        '</span>' +
                        '<span class="text-xs text-gray-500">' + (post.word_count || 0) + ' words</span>' +
                        '<span class="text-xs text-gray-500">' + (post.reading_time_minutes || 0) + ' min read</span>' +
                      '</div>' +
                    '</div>' +
                    '<div class="lg:col-span-2">' +
                      '<span class="text-sm text-gray-600">' + post.author_username + '</span>' +
                    '</div>' +
                    '<div class="lg:col-span-2">' +
                      '<div class="text-sm text-gray-500">' +
                        '<div>Created: ' + new Date(post.created_at).toLocaleDateString() + '</div>' +
                        '<div>Updated: ' + new Date(post.updated_at).toLocaleDateString() + '</div>' +
                      '</div>' +
                    '</div>' +
                    '<div class="lg:col-span-2">' +
                      '<div class="flex items-center space-x-2">' +
                        '<button onclick="window.location.href=\\'/admin/editor/' + post.id + '\\'" class="text-blue-600 hover:text-blue-700 p-2 rounded hover:bg-blue-50" title="Edit post">✏️</button>' +
                        '<button onclick="window.togglePublish(' + post.id + ', ' + !post.published + ')" class="text-gray-600 hover:text-gray-700 p-2 rounded hover:bg-gray-50" title="' + (post.published ? 'Unpublish' : 'Publish') + '">' + (post.published ? '👁️' : '👁️‍🗨️') + '</button>' +
                        '<button onclick="window.deletePost(' + post.id + ')" class="text-red-600 hover:text-red-700 p-2 rounded hover:bg-red-50" title="Delete post">🗑️</button>' +
                      '</div>' +
                    '</div>' +
                  '</div>' +
                '</div>'
              ).join('');
            }} else {{
              container.innerHTML = '<div class="text-center py-12"><span class="text-4xl">📝</span><p class="mt-4 text-gray-500">No posts found</p><button onclick="window.location.href=\\'{create_action}\\'" class="mt-4 text-blue-600 hover:text-blue-700">Create your first post</button></div>';
            }}
            
            if (paginationInfo && data.total !== undefined) {{
              const start = ((page - 1) * limit) + 1;
              const end = Math.min(page * limit, data.total);
              paginationInfo.textContent = 'Showing ' + start + '-' + end + ' of ' + data.total + ' posts';
            }}
            
            if (paginationButtons && data.total > limit) {{
              const totalPages = Math.ceil(data.total / limit);
              let buttons = '';
              
              if (page > 1) {{
                buttons += '<button onclick="window.loadPosts(' + (page - 1) + ')" class="px-3 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors">Previous</button>';
              }}
              
              const startPage = Math.max(1, page - 2);
              const endPage = Math.min(totalPages, page + 2);
              
              for (let i = startPage; i <= endPage; i++) {{
                const isActive = i === page;
                buttons += '<button onclick="window.loadPosts(' + i + ')" class="px-3 py-2 border rounded-lg transition-colors ' + 
                  (isActive ? 'bg-blue-600 text-white border-blue-600' : 'border-gray-300 hover:bg-gray-50') + '">' + i + '</button>';
              }}
              
              if (page < totalPages) {{
                buttons += '<button onclick="window.loadPosts(' + (page + 1) + ')" class="px-3 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors">Next</button>';
              }}
              
              paginationButtons.innerHTML = buttons;
            }}
          }})
          .catch(error => {{
            console.log('Failed to load posts:', error);
            document.getElementById('posts-table').innerHTML = '<div class="text-center py-12 text-red-500">Failed to load posts</div>';
          }});
      }};
      
      window.updateBulkActions = function() {{
        const selectedIds = document.querySelectorAll('.post-checkbox:checked');
        const bulkActions = document.getElementById('bulk-actions');
        const selectedCountEl = document.getElementById('selected-count');
        
        if (selectedIds.length > 0) {{
          bulkActions.classList.remove('hidden');
          selectedCountEl.textContent = selectedIds.length + ' posts selected';
        }} else {{
          bulkActions.classList.add('hidden');
        }}
      }};
      
      window.togglePublish = function(postId, publish) {{
        fetch('{api_path}/' + postId + '/publish', {{
          method: 'PATCH'
        }}).then(response => {{
          if (response.ok) {{
            window.loadPosts(window.currentPage);
          }} else {{
            alert('Failed to update post status');
          }}
        }});
      }};
      
      window.deletePost = function(postId) {{
        if (!window.confirm('Are you sure you want to delete this post? This action cannot be undone.')) return;
        
        fetch('{api_path}/' + postId, {{
          method: 'DELETE'
        }}).then(response => {{
          if (response.ok) {{
            window.loadPosts(window.currentPage);
          }} else {{
            alert('Failed to delete post');
          }}
        }});
      }};
      
      window.loadPosts();
    }}}}
    alt=""
  />
</div>"""


# Register with token "apl" (admin post list)
COMPONENT_TOKEN = "apl"
