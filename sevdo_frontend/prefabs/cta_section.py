# sevdo_frontend/prefabs/cta_section.py
def render_prefab(args, props):
    # Default values
    title = props.get("title", "Ready to Transform Your Business?")
    subtitle = props.get(
        "subtitle", "Join 10,000+ companies already using our platform"
    )
    description = props.get(
        "description",
        "Start your free trial today. No credit card required. Cancel anytime.",
    )
    primary_button = props.get("primaryButton", "Start Free Trial")
    secondary_button = props.get("secondaryButton", "Book a Demo")
    style = props.get("style", "centered")  # centered, split, gradient, minimal
    urgency = props.get("urgency", "true")  # Show urgency elements
    testimonial = props.get(
        "testimonial", "This platform increased our productivity by 300%"
    )
    testimonial_author = props.get("testimonialAuthor", "Sarah Chen, CEO at TechCorp")

    # Check if content comes from DSL (.s file) or props
    has_dsl_content = False

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
                        has_dsl_content = True

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
                        has_dsl_content = True

            if nodes:
                for node in nodes:
                    if node.token == "h" and node.args:
                        title = node.args
                        has_dsl_content = True
                    elif node.token == "t" and node.args:
                        subtitle = node.args
                        has_dsl_content = True
                    elif node.token == "b" and node.args:
                        primary_button = node.args
                        has_dsl_content = True
        except Exception:
            title = args if args else title
            if args:
                has_dsl_content = True

    # If DSL content was parsed, show minimal version without extras
    if has_dsl_content:
        if style == "split":
            return f"""<section className="py-20 bg-white">
  <div className="max-w-7xl mx-auto px-4">
    <div className="grid lg:grid-cols-2 gap-12 items-center">
      <div>
        <h2 className="text-4xl font-bold text-gray-900 mb-6">{title}</h2>
        <p className="text-xl text-gray-600 mb-8">{subtitle}</p>
        <div className="flex flex-col sm:flex-row gap-4">
          <button className="bg-blue-600 hover:bg-blue-700 text-white font-bold px-8 py-4 rounded-xl text-lg transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-1">
            {primary_button}
          </button>
        </div>
      </div>
      <div className="relative">
        <div className="bg-gradient-to-br from-blue-500 to-purple-600 rounded-3xl p-8 text-white">
          <div className="text-center">
            <div className="text-6xl mb-4">🚀</div>
            <h3 className="text-2xl font-bold mb-4">Ready to Connect?</h3>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>"""
        elif style == "minimal":
            return f"""<section className="py-16 bg-gray-50">
  <div className="max-w-3xl mx-auto px-4 text-center">
    <h2 className="text-3xl font-bold text-gray-900 mb-4">{title}</h2>
    <p className="text-lg text-gray-600 mb-8">{subtitle}</p>
    <button className="bg-blue-600 hover:bg-blue-700 text-white font-semibold px-6 py-3 rounded-lg transition-colors duration-200">
      {primary_button}
    </button>
  </div>
</section>"""
        else:  # centered or default
            return f"""<section className="py-20 bg-gradient-to-r from-blue-600 to-purple-600 text-white">
  <div className="max-w-4xl mx-auto px-4 text-center">
    <h2 className="text-4xl md:text-5xl font-bold mb-6">{title}</h2>
    <p className="text-xl text-blue-100 mb-8">{subtitle}</p>
    <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
      <button className="bg-white text-blue-600 hover:bg-blue-50 font-bold px-8 py-4 rounded-xl text-lg transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-1">
        {primary_button}
      </button>
    </div>
  </div>
</section>"""

    # Otherwise show full CTA with all features (urgency, testimonials, etc.)
    urgency_html = ""
    if urgency == "true":
        urgency_html = """
        <div className="flex items-center justify-center space-x-6 mb-8 text-sm">
            <div className="flex items-center text-green-600">
                <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                </svg>
                14-day free trial
            </div>
            <div className="flex items-center text-green-600">
                <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                </svg>
                No credit card required
            </div>
            <div className="flex items-center text-green-600">
                <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                </svg>
                Cancel anytime
            </div>
        </div>"""

    # Generate full CTA based on style (with all default features)
    if style == "centered":
        return f"""<section className="py-20 bg-gradient-to-r from-blue-600 to-purple-600 text-white">
  <div className="max-w-4xl mx-auto px-4 text-center">
    <h2 className="text-4xl md:text-5xl font-bold mb-6">{title}</h2>
    <p className="text-xl text-blue-100 mb-4">{subtitle}</p>
    <p className="text-lg text-blue-100 mb-8">{description}</p>
    {urgency_html}
    <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-8">
      <button className="bg-white text-blue-600 hover:bg-blue-50 font-bold px-8 py-4 rounded-xl text-lg transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-1">
        {primary_button}
      </button>
      <button className="border-2 border-white text-white hover:bg-white hover:text-blue-600 font-semibold px-8 py-4 rounded-xl text-lg transition-all duration-300">
        {secondary_button}
      </button>
    </div>
    <div className="bg-white bg-opacity-10 rounded-2xl p-6 backdrop-blur-sm">
      <p className="text-blue-100 italic mb-3">"{testimonial}"</p>
      <p className="text-blue-200 font-semibold">{testimonial_author}</p>
    </div>
  </div>
</section>"""

    elif style == "minimal":
        return f"""<section className="py-16 bg-gray-50">
  <div className="max-w-3xl mx-auto px-4 text-center">
    <h2 className="text-3xl font-bold text-gray-900 mb-4">{title}</h2>
    <p className="text-lg text-gray-600 mb-8">{subtitle}</p>
    <button className="bg-blue-600 hover:bg-blue-700 text-white font-semibold px-6 py-3 rounded-lg transition-colors duration-200">
      {primary_button}
    </button>
  </div>
</section>"""

    elif style == "split":
        return f"""<section className="py-20 bg-white">
  <div className="max-w-7xl mx-auto px-4">
    <div className="grid lg:grid-cols-2 gap-12 items-center">
      <div>
        <h2 className="text-4xl font-bold text-gray-900 mb-6">{title}</h2>
        <p className="text-xl text-gray-600 mb-4">{subtitle}</p>
        <p className="text-lg text-gray-600 mb-8">{description}</p>
        {urgency_html}
        <div className="flex flex-col sm:flex-row gap-4 mb-8">
          <button className="bg-blue-600 hover:bg-blue-700 text-white font-bold px-8 py-4 rounded-xl text-lg transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-1">
            {primary_button}
          </button>
          <button className="border-2 border-gray-300 text-gray-700 hover:bg-gray-100 font-semibold px-8 py-4 rounded-xl text-lg transition-all duration-300">
            {secondary_button}
          </button>
        </div>
        <div className="bg-white rounded-2xl p-6 shadow-sm border border-gray-200">
          <p className="text-gray-700 italic mb-3">"{testimonial}"</p>
          <p className="text-gray-600 font-semibold">{testimonial_author}</p>
        </div>
      </div>
      <div className="relative">
        <div className="bg-gradient-to-br from-blue-500 to-purple-600 rounded-3xl p-8 text-white">
          <div className="text-center">
            <div className="text-6xl mb-4">🚀</div>
            <h3 className="text-2xl font-bold mb-4">Ready to Launch?</h3>
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div className="bg-white bg-opacity-20 rounded-lg p-3">
                <div className="font-bold text-2xl">10K+</div>
                <div>Happy Users</div>
              </div>
              <div className="bg-white bg-opacity-20 rounded-lg p-3">
                <div className="font-bold text-2xl">99.9%</div>
                <div>Uptime</div>
              </div>
              <div className="bg-white bg-opacity-20 rounded-lg p-3">
                <div className="font-bold text-2xl">24/7</div>
                <div>Support</div>
              </div>
              <div className="bg-white bg-opacity-20 rounded-lg p-3">
                <div className="font-bold text-2xl">5min</div>
                <div>Setup</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>"""

    else:  # gradient (default)
        return f"""<section className="py-20 bg-gradient-to-br from-blue-600 via-purple-600 to-blue-800 text-white relative overflow-hidden">
  <div className="absolute inset-0 bg-black opacity-20"></div>
  <div className="relative z-10 max-w-4xl mx-auto px-4 text-center">
    <h2 className="text-4xl md:text-5xl font-bold mb-6">{title}</h2>
    <p className="text-xl text-blue-100 mb-4">{subtitle}</p>
    <p className="text-lg text-blue-100 mb-8">{description}</p>
    {urgency_html}
    <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-8">
      <button className="bg-white text-blue-600 hover:bg-blue-50 font-bold px-8 py-4 rounded-xl text-lg transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-1">
        {primary_button}
      </button>
      <button className="border-2 border-white text-white hover:bg-white hover:text-blue-600 font-semibold px-8 py-4 rounded-xl text-lg transition-all duration-300">
        {secondary_button}
      </button>
    </div>
    <div className="bg-white bg-opacity-10 rounded-2xl p-6 backdrop-blur-sm">
      <p className="text-blue-100 italic mb-3">"{testimonial}"</p>
      <p className="text-blue-200 font-semibold">{testimonial_author}</p>
    </div>
  </div>
</section>"""


# Register with token "cta"
COMPONENT_TOKEN = "cta"
