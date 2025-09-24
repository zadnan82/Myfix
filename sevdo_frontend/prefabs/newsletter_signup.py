# sevdo_frontend/prefabs/newsletter_signup.py
def render_prefab(args, props):
    # Default values
    title = props.get("title", "Subscribe to Our Newsletter")
    subtitle = props.get(
        "subtitle",
        "Get the latest articles and updates delivered directly to your inbox",
    )
    email_label = props.get("emailLabel", "Email Address")
    name_label = props.get("nameLabel", "Name (Optional)")
    button_text = props.get("buttonText", "Subscribe")
    privacy_text = props.get(
        "privacyText", "We respect your privacy. Unsubscribe at any time."
    )

    # Backend action-related props
    submit_path = props.get("submitPath")  # e.g., /api/newsletter
    submit_method = (props.get("submitMethod") or "POST").upper()
    submit_action = props.get("submitAction")  # fallback: direct action string

    # Navigation configuration from template.json
    navigation = props.get("navigation", {})
    nav_actions = navigation.get("actions", {})
    nav_routes = navigation.get("routes", {})

    # Get success redirect path (optional)
    success_redirect = nav_actions.get(
        "newsletter_success", nav_routes.get("home", "/")
    )

    # Support for nested components
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
                        subtitle = node.args
                    elif node.token == "b" and node.args:
                        button_text = node.args
        except Exception:
            title = args if args else title

    # Build form submission handler
    email_id = "ns-email"
    name_id = "ns-name"

    if submit_action:
        safe = submit_action.replace("\\", "\\\\").replace("'", "\\'")
        submit_handler = f" onClick={{() => window.sevdoAct('{safe}')}}"
    else:
        endpoint = submit_path or "/api/newsletter"
        # Enhanced handler with form validation and success feedback
        submit_handler = (
            " onClick={(event) => {"
            + f"const emailInput = document.getElementById('{email_id}');"
            + f"const nameInput = document.getElementById('{name_id}');"
            + "const email = emailInput.value.trim();"
            + "const name = nameInput.value.trim();"
            + "if (!email) { alert('Please enter your email address'); return; }"
            + "const emailRegex = /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/;"
            + "if (!emailRegex.test(email)) { alert('Please enter a valid email address'); return; }"
            + "const formData = { email: email, name: name || null };"
            + f"const btn = event.target; btn.disabled = true; btn.textContent = 'Subscribing...';"
            + f"fetch('http://localhost:8000{endpoint}', {{"
            + f"method: '{submit_method}', "
            + "headers: {'Content-Type': 'application/json'}, "
            + "body: JSON.stringify(formData)"
            + "}).then(response => response.json()).then(result => {"
            + "console.log('Newsletter response:', result);"
            + "if (result.msg || result.message) {"
            + "alert(result.msg || result.message);"
            + "if (result.status === 'subscribed' || result.status === 'reactivated') {"
            + "emailInput.value = ''; nameInput.value = '';"
            + "}"
            + "}"
            + "btn.disabled = false; btn.textContent = '"
            + button_text
            + "';"
            + "}).catch(error => {"
            + "console.error('Newsletter error:', error);"
            + "alert('Error: Could not subscribe. Please try again.');"
            + "btn.disabled = false; btn.textContent = '"
            + button_text
            + "';"
            + "});"
            + "}}"
        )

    return f"""<section className="py-12 bg-gradient-to-br from-blue-50 to-indigo-100">
  <div className="max-w-2xl mx-auto px-4">
    <div className="bg-white rounded-2xl shadow-xl p-8">
      <div className="text-center mb-8">
        <div className="w-16 h-16 bg-blue-600 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
          </svg>
        </div>
        <h2 className="text-3xl font-bold text-gray-900 mb-4">{title}</h2>
        <p className="text-lg text-gray-600">{subtitle}</p>
      </div>
      
      <form className="space-y-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">{email_label} *</label>
          <input 
            id="{email_id}"
            name="email"
            type="email" 
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors"
            placeholder="Enter your email address" 
            required 
          />
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">{name_label}</label>
          <input 
            id="{name_id}"
            name="name"
            type="text" 
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors"
            placeholder="Enter your name (optional)" 
          />
        </div>
        
        <button 
          type="button" 
          className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-lg transition-all duration-200 transform hover:scale-105 shadow-lg hover:shadow-xl"
          {submit_handler}
        >
          <div className="flex items-center justify-center">
            <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"></path>
            </svg>
            {button_text}
          </div>
        </button>
      </form>
      
      <div className="mt-6 text-center">
        <p className="text-sm text-gray-500 flex items-center justify-center">
          <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path>
          </svg>
          {privacy_text}
        </p>
      </div>
      
      <!-- Newsletter Benefits -->
      <div className="mt-8 pt-6 border-t border-gray-200">
        <h3 className="text-lg font-semibold text-gray-900 mb-4 text-center">What you'll get:</h3>
        <div className="grid md:grid-cols-3 gap-4 text-center">
          <div className="flex flex-col items-center">
            <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mb-2">
              <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
              </svg>
            </div>
            <p className="text-sm font-medium text-gray-700">Latest Articles</p>
          </div>
          <div className="flex flex-col items-center">
            <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mb-2">
              <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
              </svg>
            </div>
            <p className="text-sm font-medium text-gray-700">Exclusive Tips</p>
          </div>
          <div className="flex flex-col items-center">
            <div className="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center mb-2">
              <svg className="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            </div>
            <p className="text-sm font-medium text-gray-700">Weekly Updates</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>"""


# Metadata för backend-koppling
PREFAB_METADATA = {
    "backend_handler": "nlh",
    "api_path": "/api/newsletter",
    "method": "POST",
}

# Register with token "ns"
COMPONENT_TOKEN = "ns"
