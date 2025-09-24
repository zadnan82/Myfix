# sevdo_frontend/prefabs/contact_information.py
def render_prefab(args, props):
    # Default values based on user's specification
    title = props.get("title", "Get In Touch")
    subtitle = props.get(
        "subtitle",
        "Have a question, suggestion, or just want to say hello? I'd love to hear from you!"
    )
    section_title = props.get("sectionTitle", "Contact Information")
    section_content = props.get("sectionContent", "Section content goes here.")

    # Contact details with defaults
    email = props.get("email", "alex@devinsights.com")
    twitter = props.get("twitter", "@devinsights")
    linkedin = props.get("linkedin", "/in/alex-developer")
    location = props.get("location", "San Francisco, CA")

    # Styling options
    background_color = props.get("backgroundColor", "bg-gray-50")
    card_style = props.get("cardStyle", "bg-white shadow-lg")

    # Support for nested components (optional customization)
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
                    elif node.token == "t" and node.args:
                        subtitle = node.args
        except Exception:
            # Fallback to using args as title
            title = args if args else title

    # Handle click actions for contact items
    email_action = props.get("emailAction")
    twitter_action = props.get("twitterAction")
    linkedin_action = props.get("linkedinAction")
    location_action = props.get("locationAction")

    # Email link handler
    email_href = f"mailto:{email}"
    if email_action:
        email_handler = f' onClick={{"() => window.sevdoAct(\'{email_action}\')" }}'
    else:
        email_handler = f' href="{email_href}"'

    # Twitter link handler
    twitter_href = f"https://twitter.com/{twitter.lstrip('@')}"
    if twitter_action:
        twitter_handler = f' onClick={{"() => window.sevdoAct(\'{twitter_action}\')" }}'
    else:
        twitter_handler = f' href="{twitter_href}" target="_blank" rel="noopener noreferrer"'

    # LinkedIn link handler
    linkedin_href = f"https://linkedin.com{linkedin}"
    if linkedin_action:
        linkedin_handler = f' onClick={{"() => window.sevdoAct(\'{linkedin_action}\')" }}'
    else:
        linkedin_handler = f' href="{linkedin_href}" target="_blank" rel="noopener noreferrer"'

    # Location handler (could be Google Maps or custom action)
    if location_action:
        location_handler = f' onClick={{"() => window.sevdoAct(\'{location_action}\')" }}'
    else:
        location_handler = ""

    return f"""<section className="py-16 {background_color}">
  <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">{title}</h2>
      <p className="text-xl text-gray-600 max-w-2xl mx-auto">{subtitle}</p>
    </div>

    <div className="max-w-3xl mx-auto">
      <div className="{card_style} rounded-xl p-8 md:p-10">

        <div className="mb-8">
          <h3 className="text-2xl font-semibold text-gray-900 mb-3">{section_title}</h3>
          <p className="text-gray-600">{section_content}</p>
        </div>

        <div className="grid gap-6 md:grid-cols-1">

          <div className="flex items-center space-x-4 p-4 rounded-lg hover:bg-gray-50 transition-colors duration-200">
            <div className="flex-shrink-0">
              <span className="text-2xl" role="img" aria-label="Email">📧</span>
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-gray-900 mb-1">Email</p>
              <a className="text-lg text-gray-900 hover:text-blue-600 transition-colors duration-200 font-medium"{email_handler}>
                {email}
              </a>
            </div>
          </div>

          <div className="flex items-center space-x-4 p-4 rounded-lg hover:bg-gray-50 transition-colors duration-200">
            <div className="flex-shrink-0">
              <span className="text-2xl" role="img" aria-label="Twitter">🐦</span>
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-gray-900 mb-1">Twitter</p>
              <a className="text-lg text-gray-900 hover:text-blue-600 transition-colors duration-200 font-medium"{twitter_handler}>
                {twitter}
              </a>
            </div>
          </div>

          <div className="flex items-center space-x-4 p-4 rounded-lg hover:bg-gray-50 transition-colors duration-200">
            <div className="flex-shrink-0">
              <span className="text-2xl" role="img" aria-label="LinkedIn">💼</span>
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-gray-900 mb-1">LinkedIn</p>
              <a className="text-lg text-gray-900 hover:text-blue-600 transition-colors duration-200 font-medium"{linkedin_handler}>
                {linkedin}
              </a>
            </div>
          </div>

          <div className="flex items-center space-x-4 p-4 rounded-lg hover:bg-gray-50 transition-colors duration-200">
            <div className="flex-shrink-0">
              <span className="text-2xl" role="img" aria-label="Location">🌍</span>
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-gray-900 mb-1">Location</p>
              <span className="text-lg text-gray-900 font-medium"{location_handler}>
                {location}
              </span>
            </div>
          </div>

        </div>

      </div>
    </div>
  </div>
</section>"""

# Metadata for backend integration
PREFAB_METADATA = {
    "backend_handler": "cih",
    "api_path": "/api/contact-info",
    "method": "GET",
}

# Register with token "ci"
COMPONENT_TOKEN = "ci"
