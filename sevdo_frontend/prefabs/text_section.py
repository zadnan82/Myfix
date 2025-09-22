# sevdo_frontend/prefabs/text_section.py
def render_prefab(args, props):
    # Default values
    title = props.get("title", "Section Title")
    text = props.get("text", "Section content goes here.")
    title_level = props.get("titleLevel", "h2")  # h1, h2, h3, h4, h5, h6
    align = props.get("align", "left")  # left, center, right
    max_width = props.get(
        "maxWidth", "4xl"
    )  # sm, md, lg, xl, 2xl, 3xl, 4xl, 5xl, 6xl, 7xl

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
                        text = args[t_content_start:t_end]
                        has_dsl_content = True

            if nodes:
                for node in nodes:
                    if node.token == "h" and node.args:
                        title = node.args
                        has_dsl_content = True
                    elif node.token == "t" and node.args:
                        text = node.args
                        has_dsl_content = True
        except Exception:
            title = args if args else title
            if args:
                has_dsl_content = True

    # Title level mapping
    title_tag = (
        title_level if title_level in ["h1", "h2", "h3", "h4", "h5", "h6"] else "h2"
    )

    # Title size classes based on level
    title_sizes = {
        "h1": "text-4xl md:text-5xl font-bold",
        "h2": "text-3xl md:text-4xl font-bold",
        "h3": "text-2xl md:text-3xl font-bold",
        "h4": "text-xl md:text-2xl font-semibold",
        "h5": "text-lg md:text-xl font-semibold",
        "h6": "text-base md:text-lg font-semibold",
    }
    title_class = title_sizes.get(title_tag, title_sizes["h2"])

    # Alignment classes
    align_classes = {
        "left": "text-left",
        "center": "text-center",
        "right": "text-right",
    }
    align_class = align_classes.get(align, "text-left")

    # Max width classes
    max_width_class = f"max-w-{max_width}"

    return f"""<section className="py-8">
  <div className="mx-auto px-4 {max_width_class}">
    <div className="{align_class}">
      <{title_tag} className="{title_class} text-gray-900 mb-4">
        {title}
      </{title_tag}>
      <p className="text-lg text-gray-600 leading-relaxed">
        {text}
      </p>
    </div>
  </div>
</section>"""


# Register with token "ts"
COMPONENT_TOKEN = "ts"
