# sevdo_frontend/prefabs/contact_form.py
def render_prefab(args, props):
    # Default values
    title = props.get("title", "Get in Touch")
    subtitle = props.get(
        "subtitle",
        "We'd love to hear from you. Send us a message and we'll respond as soon as possible.",
    )
    name_label = props.get("nameLabel", "Full Name")
    email_label = props.get("emailLabel", "Email Address")
    subject_label = props.get("subjectLabel", "Subject")
    message_label = props.get("messageLabel", "Message")
    button_text = props.get("buttonText", "Send Message")

    # Backend action-related props
    submit_path = props.get("submitPath")  # e.g., /api/contact
    submit_method = (props.get("submitMethod") or "POST").upper()
    submit_action = props.get("submitAction")  # fallback: direct action string

    # Navigation configuration from template.json
    navigation = props.get("navigation", {})
    nav_actions = navigation.get("actions", {})
    nav_routes = navigation.get("routes", {})

    # Get success redirect path
    success_redirect = nav_actions.get(
        "contact_form_success", nav_routes.get("home", "/")
    )

    # Support for nested components (optional title/button overrides)
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

    # Build form submission handler (ALWAYS defined)
    name_id = "cf-name"
    email_id = "cf-email"
    subject_id = "cf-subject"
    message_id = "cf-message"

    if submit_action:
        safe = submit_action.replace("\\", "\\\\").replace("'", "\\'")
        submit_handler = f" onClick={{() => window.sevdoAct('{safe}')}}"
    else:
        endpoint = submit_path or "/api/contact"
        # Enhanced handler with proper React Router navigation
        submit_handler = (
            " onClick={(event) => {"
            + "const formData = {"
            + f"name: document.getElementById('{name_id}').value, "
            + f"email: document.getElementById('{email_id}').value, "
            + f"subject: document.getElementById('{subject_id}').value, "
            + f"message: document.getElementById('{message_id}').value"
            + "}; "
            + f"const btn = event.target; btn.disabled = true; btn.textContent = 'Sending...';"
            + f"fetch('http://localhost:8000{endpoint}', {{"
            + f"method: '{submit_method}', "
            + "headers: {'Content-Type': 'application/json'}, "
            + "body: JSON.stringify(formData)"
            + "}).then(response => response.json()).then(result => {"
            + "console.log('Contact form response:', result); "
            + "if (result.msg || result.message) {"
            + "alert(result.msg || result.message); "
            + f"setTimeout(() => {{ navigate('{success_redirect}'); }}, 2000);"
            + "} btn.disabled = false; btn.textContent = '"
            + button_text
            + "';"
            + "}).catch(error => {"
            + "console.error('Contact form error:', error); "
            + "alert('Error: Could not send message. Please try again.'); "
            + "btn.disabled = false; btn.textContent = '"
            + button_text
            + "';"
            + "});"
            + "}}"
        )

    return f"""<section className="py-12 bg-gray-50">
  <div className="max-w-2xl mx-auto px-4">
    <div className="text-center mb-8">
      <h2 className="text-3xl font-bold text-gray-900 mb-4">{title}</h2>
      <p className="text-gray-600">{subtitle}</p>
    </div>
    
    <form className="bg-white rounded-lg shadow-md p-8">
      <div className="grid md:grid-cols-2 gap-6 mb-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">{name_label}</label>
          <input 
            id="{name_id}"
            name="name"
            type="text" 
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="Enter your full name" 
            required 
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">{email_label}</label>
          <input 
            id="{email_id}"
            name="email"
            type="email" 
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="Enter your email address" 
            required 
          />
        </div>
      </div>
      
      <div className="mb-6">
        <label className="block text-sm font-medium text-gray-700 mb-2">{subject_label}</label>
        <input 
          id="{subject_id}"
          name="subject"
          type="text" 
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          placeholder="What is this about?" 
          required 
        />
      </div>
      
      <div className="mb-6">
        <label className="block text-sm font-medium text-gray-700 mb-2">{message_label}</label>
        <textarea 
          id="{message_id}"
          name="message"
          rows="5" 
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-vertical"
          placeholder="Tell us more about your inquiry..." 
          required
        ></textarea>
      </div>
      
      <button 
        type="button" 
        className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-3 px-6 rounded-md transition-colors duration-200"
        {submit_handler}
      >
        {button_text}
      </button>
    </form>
  </div>
</section>"""


# Metadata för backend-koppling
PREFAB_METADATA = {
    "backend_handler": "cfh",
    "api_path": "/api/contact",
    "method": "POST",
    "imports": [
        "import { useNavigate } from 'react-router-dom';"
    ],
    "hooks": [
        "const navigate = useNavigate();"
    ]
}

# Register with token "cf"
COMPONENT_TOKEN = "cf"
