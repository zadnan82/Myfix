"""
template_utils.py - Utility functions for creating default files and templates

This module contains functions for setting up default examples and HTML templates.
"""

from pathlib import Path


def create_default_files(input_dir: Path):
    """Create some default example files if the input directory is empty."""
    if list(input_dir.glob("*.txt")):
        return  # Don't create if files already exist

    examples = {
        "hello_world.txt": """h(Hello World)
t(This is a simple example of the frontend DSL)
b(Say Hello, onClick=alert('Hello!'))""",
        "form_example.txt": """f(
h(Contact Form)
i(Your Name, label=Name)
i(your.email@example.com, label=Email)
sel(home,work, label=Department, home,work)
b(Submit Form, onClick=alert('Form submitted!'))
)""",
        "layout_example.txt": """c(class=gap-6)
h(Main Layout)
c(class=gap-4)
t(This is a nested container example)
b(Button 1)
b(Button 2)
c(class=gap-2)
t(Sub section)
i(Enter text here)
sel(option1,option2,option3)
""",
        "image_example.txt": """c(class=gap-4 items-center)
h(Image Gallery)
img(https://via.placeholder.com/300x200?text=Sample+Image, alt=Sample Image)
t(This is an example of using images in the DSL)
b(View More Images)
""",
    }

    for filename, content in examples.items():
        file_path = input_dir / filename
        file_path.write_text(content, encoding="utf-8")
        print(f"Created example file: {filename}")


def create_default_backend_files(backend_input_dir: Path):
    """Create some default backend example files if the backend input directory is empty."""
    if list(backend_input_dir.glob("*.txt")):
        return  # Don't create if files already exist

    backend_examples = {
        "auth_endpoints.txt": "r l m o",
        "session_management.txt": "t a s k",
        "form_handlers.txt": "cfh lfh rfh emh",
        "chat_system.txt": "cha",
        "basic_api.txt": "r l m",
    }

    for filename, content in backend_examples.items():
        file_path = backend_input_dir / filename
        file_path.write_text(content, encoding="utf-8")
        print(f"Created backend example file: {filename}")


def create_default_index_template(templates_dir: Path):
    """Create a default index.html template if it doesn't exist."""
    index_template = templates_dir / "index.html"
    if index_template.exists():
        return

    template_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SEVDO Playground</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        .file-item { @apply p-3 border rounded-lg hover:bg-gray-50 transition-colors; }
        .compile-btn { @apply px-3 py-1 bg-blue-500 text-white rounded text-sm hover:bg-blue-600; }
        .view-btn { @apply px-3 py-1 bg-green-500 text-white rounded text-sm hover:bg-green-600; }
        .status-indicator { @apply w-3 h-3 rounded-full; }
        .status-compiled { @apply bg-green-500; }
        .status-not-compiled { @apply bg-red-500; }
    </style>
</head>
<body class="bg-gray-100">
    <div class="container mx-auto p-6">
        <header class="mb-8">
            <h1 class="text-3xl font-bold text-gray-800 mb-2">SEVDO Playground</h1>
            <p class="text-gray-600">DSL Compiler Development Environment</p>
            <div class="mt-4 flex gap-4">
                <button onclick="compileAll()" class="compile-btn">Compile All Frontend</button>
                <button onclick="compileAllBackend()" class="compile-btn">Compile All Backend</button>
                <button onclick="startBackend()" class="bg-purple-500 hover:bg-purple-600 px-3 py-1 text-white rounded text-sm">Start Backend</button>
                <a href="/backend/swagger" target="_blank" class="bg-indigo-500 hover:bg-indigo-600 px-3 py-1 text-white rounded text-sm no-underline">API Docs</a>
            </div>
        </header>

        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <!-- Frontend Files -->
            <div class="bg-white rounded-lg shadow p-6">
                <h2 class="text-xl font-semibold mb-4">Frontend Files</h2>
                <div class="space-y-3">
                    {% for file in frontend_files %}
                    <div class="file-item flex items-center justify-between">
                        <div class="flex items-center gap-3">
                            <div class="status-indicator {% if file.exists %}status-compiled{% else %}status-not-compiled{% endif %}"></div>
                            <span class="font-medium">{{ file.name }}</span>
                        </div>
                        <div class="flex gap-2">
                            <button onclick="compileFile('{{ file.name }}')" class="compile-btn">Compile</button>
                            {% if file.exists %}
                            <a href="/view/{{ file.name }}" target="_blank" class="view-btn no-underline">View</a>
                            {% endif %}
                        </div>
                    </div>
                    {% endfor %}
                </div>
            </div>

            <!-- Backend Files -->
            <div class="bg-white rounded-lg shadow p-6">
                <h2 class="text-xl font-semibold mb-4">Backend Files</h2>
                <div class="space-y-3">
                    {% for file in backend_files %}
                    <div class="file-item flex items-center justify-between">
                        <div class="flex items-center gap-3">
                            <div class="status-indicator {% if file.exists %}status-compiled{% else %}status-not-compiled{% endif %}"></div>
                            <span class="font-medium">{{ file.name }}</span>
                        </div>
                        <div class="flex gap-2">
                            <button onclick="compileBackendFile('{{ file.name }}')" class="compile-btn">Compile</button>
                        </div>
                    </div>
                    {% endfor %}
                </div>
                
                <div class="mt-6 p-4 bg-gray-50 rounded-lg">
                    <h3 class="font-medium mb-2">Backend Server Status</h3>
                    <div id="backend-status" class="text-sm text-gray-600">Checking...</div>
                    <div class="mt-2">
                        <button onclick="checkBackendStatus()" class="text-sm text-blue-600 hover:text-blue-800">Refresh Status</button>
                    </div>
                </div>
            </div>
        </div>

        <!-- File Paths Info -->
        <div class="mt-8 bg-white rounded-lg shadow p-6">
            <h3 class="text-lg font-semibold mb-3">Directory Information</h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                <div>
                    <strong>Frontend Input:</strong> {{ input_dir }}<br>
                    <strong>Frontend Output:</strong> {{ output_dir }}
                </div>
                <div>
                    <strong>Backend Input:</strong> {{ backend_input_dir }}<br>
                    <strong>Backend Output:</strong> {{ backend_output_dir }}
                </div>
            </div>
        </div>
    </div>

    <script>
        // WebSocket connection for real-time updates
        const ws = new WebSocket(`ws://${window.location.host}/ws`);
        
        ws.onmessage = function(event) {
            const data = JSON.parse(event.data);
            if (data.type === 'files_changed') {
                location.reload();
            }
        };

        // API functions
        async function compileFile(filename) {
            try {
                const response = await fetch(`/compile/${filename}`, { method: 'POST' });
                const result = await response.json();
                alert(result.message);
            } catch (error) {
                alert('Error compiling file: ' + error.message);
            }
        }

        async function compileAll() {
            try {
                const response = await fetch('/compile-all', { method: 'POST' });
                const result = await response.json();
                alert(result.message);
            } catch (error) {
                alert('Error compiling files: ' + error.message);
            }
        }

        async function compileBackendFile(filename) {
            try {
                const response = await fetch(`/backend/compile/${filename}`, { method: 'POST' });
                const result = await response.json();
                alert(result.message);
            } catch (error) {
                alert('Error compiling backend file: ' + error.message);
            }
        }

        async function compileAllBackend() {
            try {
                const response = await fetch('/backend/compile-all', { method: 'POST' });
                const result = await response.json();
                alert(result.message);
            } catch (error) {
                alert('Error compiling backend files: ' + error.message);
            }
        }

        async function startBackend() {
            try {
                const response = await fetch('/backend/start', { method: 'POST' });
                const result = await response.json();
                alert(result.message);
                checkBackendStatus();
            } catch (error) {
                alert('Error starting backend: ' + error.message);
            }
        }

        async function checkBackendStatus() {
            try {
                const response = await fetch('/backend/status');
                const status = await response.json();
                const statusDiv = document.getElementById('backend-status');
                
                if (status.running) {
                    statusDiv.innerHTML = `
                        <span class="text-green-600 font-medium">✓ Running on port ${status.port}</span><br>
                        <a href="${status.url}/docs" target="_blank" class="text-blue-600 hover:text-blue-800">Open API Docs</a>
                    `;
                } else {
                    statusDiv.innerHTML = '<span class="text-red-600">✗ Not running</span>';
                }
            } catch (error) {
                document.getElementById('backend-status').innerHTML = '<span class="text-red-600">Error checking status</span>';
            }
        }

        // Check backend status on page load
        checkBackendStatus();
    </script>
</body>
</html>
    """

    index_template.write_text(template_content.strip(), encoding="utf-8")
    print(f"Created default index template: {index_template}")
