# sevdo_frontend/prefabs/login_form.py
def render_prefab(args, props):
    # Default values
    title = "Login to Your Account"
    email_label = props.get("emailLabel", "Username")
    password_label = props.get("passwordLabel", "Password")
    signin_text = props.get("buttonText", "Sign In")
    forgot_text = props.get("forgotText", "Forgot Password?")
    # Action-related props
    sign_in_path = props.get("signInPath", "/api/login")  # Changed to /api/login-form
    sign_in_method = (props.get("signInMethod") or "POST").upper()
    signin_action = props.get("signinAction")  # fallback: direct action string
    forgot_action = props.get("forgotAction")

    # Support for nested components
    # If the args is a nested structure like "b(Custom Button Text)"
    # we can extract and use those values
    if args:
        # Import parser when needed to avoid circular imports
        import sys
        import os

        # Get the parent directory path
        parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if parent_dir not in sys.path:
            sys.path.append(parent_dir)
        # Import directly from the file
        from frontend_compiler import parse_dsl

        try:
            # Try to parse args as DSL
            nodes = parse_dsl(args)
            if nodes:
                for node in nodes:
                    # Replace button text if b() token is found
                    if node.token == "b" and node.args:
                        signin_text = node.args
                    # Replace title if h() token is found
                    elif node.token == "h" and node.args:
                        title = node.args
        except Exception:
            # If parsing fails, just use args as the title
            title = args

    # Build handlers
    # Inputs will have stable ids to collect values
    email_id = "lf-email"
    password_id = "lf-password"

    # Direct fetch handler instead of sevdoAct
    signin_handler = f"""
 onClick={{(e) => {{
   e.preventDefault();
   const username = document.getElementById('{email_id}').value;
   const password = document.getElementById('{password_id}').value;
   
   if (!username || !password) {{
     alert('Please enter both username and password');
     return;
   }}
   
   console.log('Attempting login...');
   
   fetch('{sign_in_path}', {{
     method: '{sign_in_method}',
     headers: {{'Content-Type': 'application/json'}},
     body: JSON.stringify({{username: username, password: password, remember_me: false}})
   }})
   .then(response => {{
     console.log('Response status:', response.status);
     return response.json();
   }})
   .then(data => {{
     console.log('Login response:', data);
     if (data.session_token) {{
       localStorage.setItem('authToken', data.session_token);
       console.log('Token saved, redirecting to admin...');
       window.location.href = '/admin';
     }} else {{
       alert(data.detail || 'Login failed');
     }}
   }})
   .catch(error => {{
     console.error('Login error:', error);
     alert('Login failed. Please try again.');
   }});
 }}}}"""

    if forgot_action:
        safe_f = forgot_action.replace("\\", "\\\\").replace("'", "\\'")
        forgot_handler = f" onClick={{() => window.sevdoAct('{safe_f}')}}"
    else:
        forgot_handler = ""

    # Style customization with optional extra classes
    form_class = "max-w-md mx-auto p-6"
    if props.get("formClass"):
        form_class = f"{form_class} {props.get('formClass')}"
    title_class = "text-xl font-bold mb-4"
    if props.get("titleClass"):
        title_class = f"{title_class} {props.get('titleClass')}"
    container_class = "flex flex-col gap-4"
    if props.get("containerClass"):
        container_class = f"{container_class} {props.get('containerClass')}"
    label_class = "block"
    if props.get("labelClass"):
        label_class = f"{label_class} {props.get('labelClass')}"
    input_class = "border rounded px-3 py-2 w-full"
    if props.get("inputClass"):
        input_class = f"{input_class} {props.get('inputClass')}"
    actions_class = "flex flex-row gap-2 mt-4"
    if props.get("actionsClass"):
        actions_class = f"{actions_class} {props.get('actionsClass')}"
    signin_class = (
        "bg-blue-600 hover:bg-blue-700 text-white font-medium px-4 py-2 rounded"
    )
    if props.get("signinClass"):
        signin_class = f"{signin_class} {props.get('signinClass')}"
    forgot_class = (
        "bg-gray-500 hover:bg-gray-600 text-white font-medium px-4 py-2 rounded"
    )
    if props.get("forgotClass"):
        forgot_class = f"{forgot_class} {props.get('forgotClass')}"

    # Generate full form with customized parts
    return f"""<form className="{form_class}">
  <h1 className="{title_class}">{title}</h1>
  <div className="{container_class}">
    <label className="{label_class}">
      <span className="mb-1 block">{email_label}</span>
      <input id="{email_id}" name="username" className="{input_class}" placeholder="Enter your username" />
    </label>
    <label className="{label_class}">
      <span className="mb-1 block">{password_label}</span>
      <input id="{password_id}" name="password" className="{input_class}" type="password" placeholder="Enter your password" />
    </label>
    <div className="{actions_class}">
      <button type="button" className="{signin_class}"{signin_handler}>{signin_text}</button>
      <button type="button" className="{forgot_class}"{forgot_handler}>{forgot_text}</button>
    </div>
  </div>
</form>"""


# Register with token "lf"
COMPONENT_TOKEN = "lf"
