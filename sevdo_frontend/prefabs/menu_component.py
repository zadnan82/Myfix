# sevdo_frontend/prefabs/menu_component.py
def render_prefab(args, props):
    # Initial values
    orientation = props.get("orientation", "horizontal")
    brand_text = None
    items = None

    # Support for nested components
    if args:
        import sys
        import os

        parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if parent_dir not in sys.path:
            sys.path.append(parent_dir)
        from frontend_compiler import parse_dsl, _jsx_for_token

        nodes = parse_dsl(args)

        # HACK: Since SEVDO parser only gets first token, let's manually parse the rest
        if len(nodes) == 1 and "," in args and "m(" in args:
            # Extract m() content manually
            m_start = args.find("m(")
            if m_start != -1:
                m_end = args.rfind(")")
                if m_end != -1:
                    m_content = args[m_start + 2 : m_end]
                    items = [item.strip() for item in m_content.split(",")]

        if nodes:
            for node in nodes:
                if node.token == "h" and node.args:
                    brand_text = node.args
                elif node.token == "o" and node.args:
                    orientation = node.args
                elif node.token == "m" and node.args:
                    items = [item.strip() for item in node.args.split(",")]

    # Set fallbacks ONLY if nothing was parsed
    if brand_text is None:
        brand_text = props.get("brandText", "Brand")

    if items is None:
        items = props.get("items", ["Home", "About", "Services", "Contact"])

    def get_route_path(item):
        """Convert menu item to React Router path"""
        if item == "Home":
            return "/"
        else:
            return f"/{item.lower()}"

    # Generate menu items with React Router Links
    if orientation == "vertical":
        menu_items = "\n".join(
            [
                f'    <li><Link to="{get_route_path(item)}" className="block px-4 py-2 text-gray-700 hover:bg-gray-100 hover:text-blue-600 transition-colors duration-200">{item}</Link></li>'
                for item in items
            ]
        )

        return f"""<div className="w-64 bg-white border-r border-gray-200 shadow-sm">
  <div className="px-6 py-4 border-b border-gray-200">
    <h2 className="text-lg font-semibold text-gray-800">{brand_text}</h2>
  </div>
  <nav className="py-4">
    <ul className="space-y-1">
{menu_items}
    </ul>
  </nav>
</div>"""

    else:
        menu_items = "\n".join(
            [
                f'        <Link to="{get_route_path(item)}" className="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200">{item}</Link>'
                for item in items
            ]
        )

        return f"""<nav className="bg-white shadow-sm border-b border-gray-200">
  <div className="max-w-6xl mx-auto px-4">
    <div className="flex justify-between items-center py-4">
      <div className="flex items-center">
        <Link to="/" className="text-xl font-bold text-gray-800 hover:text-blue-600 transition-colors duration-200">{brand_text}</Link>
      </div>
      <div className="hidden md:flex space-x-1">
{menu_items}
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
</nav>"""


# Register with token "mn"
COMPONENT_TOKEN = "mn"

# Add metadata for the frontend compiler to know what imports are needed
PREFAB_METADATA = {
    "imports": [
        "import { Link } from 'react-router-dom';"
    ]
}
