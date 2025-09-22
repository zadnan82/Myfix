# sevdo_frontend/prefabs/hero_section.py
def render_prefab(args, props):
    # Default values
    title = props.get("title", "Transform Your Business Today")
    subtitle = props.get("subtitle", "Powerful Solutions for Modern Challenges")
    description = props.get("description", "")
    primary_button = props.get("primaryButton", "Get Started Free")
    secondary_button = props.get("secondaryButton", "")
    background = props.get("background", "gradient")  # gradient, image, solid

    # Navigation configuration from template.json
    navigation = props.get("navigation", {})
    nav_actions = navigation.get("actions", {})
    nav_routes = navigation.get("routes", {})

    # Default navigation fallbacks
    primary_link = nav_actions.get("hero_primary_cta", nav_routes.get("blog", "/blog"))
    secondary_link = nav_actions.get(
        "hero_secondary_cta", nav_routes.get("contact", "/contact")
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

            # HACK: Manual parsing för att komma runt SEVDO parser begränsningar
            # Parse t() token manually
            if len(nodes) == 1 and "," in args and "t(" in args:
                t_start = args.find("t(")
                if t_start != -1:
                    depth = 0
                    t_content_start = t_start + 2
                    t_end = t_content_start
                    for i in range(t_content_start, len(args)):
                        if args[i] == "(":
                            depth += 1
                        elif args[i] == ")":
                            if depth == 0:
                                t_end = i
                                break
                            depth -= 1

                    if t_end > t_content_start:
                        subtitle = args[t_content_start:t_end]

            # Parse b() token manually
            if len(nodes) <= 2 and "," in args and "b(" in args:
                b_start = args.find("b(")
                if b_start != -1:
                    depth = 0
                    b_content_start = b_start + 2
                    b_end = b_content_start
                    for i in range(b_content_start, len(args)):
                        if args[i] == "(":
                            depth += 1
                        elif args[i] == ")":
                            if depth == 0:
                                b_end = i
                                break
                            depth -= 1

                    if b_end > b_content_start:
                        primary_button = args[b_content_start:b_end]

            if nodes:
                for node in nodes:
                    if node.token == "h" and node.args:
                        title = node.args
                    elif node.token == "t" and node.args:
                        subtitle = node.args
                    elif node.token == "b" and node.args:
                        primary_button = node.args
        except Exception:
            title = args if args else title

    # Background styling based on background prop
    if background == "gradient":
        bg_class = "bg-gradient-to-br from-blue-600 via-purple-600 to-blue-800"
    elif background == "solid":
        bg_class = "bg-blue-600"
    elif background == "image":
        bg_class = "bg-gray-900 bg-cover bg-center"
        # Note: In real implementation, you'd add background-image via props
    else:
        bg_class = "bg-gradient-to-br from-blue-600 via-purple-600 to-blue-800"

    # Generate primary button with navigation
    primary_button_html = f"""
      <Link to="{primary_link}" className="bg-white text-blue-600 hover:bg-blue-50 font-semibold px-8 py-4 rounded-lg text-lg transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-1">
        {primary_button}
      </Link>"""

    # Generate secondary button only if it exists
    secondary_button_html = ""
    if secondary_button:
        secondary_button_html = f"""
      <Link to="{secondary_link}" className="border-2 border-white text-white hover:bg-white hover:text-blue-600 font-semibold px-8 py-4 rounded-lg text-lg transition-all duration-300">
        {secondary_button}
      </Link>"""

    # Generate description only if it exists
    description_html = ""
    if description:
        description_html = f"""
    <p className="text-lg md:text-xl mb-12 text-blue-100 max-w-4xl mx-auto leading-relaxed">
      {description}
    </p>"""

    return f"""<section className="relative {bg_class} text-white min-h-screen flex items-center">
  <div className="absolute inset-0 bg-black opacity-20"></div>
  <div className="relative z-10 max-w-6xl mx-auto px-4 py-20 text-center">
    <h1 className="text-5xl md:text-7xl font-bold mb-6 leading-tight">
      {title}
    </h1>
    <h2 className="text-xl md:text-2xl font-light mb-8 text-blue-100 max-w-3xl mx-auto">
      {subtitle}
    </h2>{description_html}
    <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
      {primary_button_html}{secondary_button_html}
    </div>

  </div>
  <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2 animate-bounce">
    <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 14l-7 7m0 0l-7-7m7 7V3"></path>
    </svg>
  </div>
</section>"""


# Register with token "ho"
COMPONENT_TOKEN = "ho"
