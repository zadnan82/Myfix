# user_backend/app/services/template_generator.py

import subprocess
import shutil
import json
import asyncio
from pathlib import Path
from typing import Dict, List, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class TemplateGeneratorService:
    """Service to pre-generate template outputs and manage live previews"""

    def __init__(self, base_dir: str = "/app"):
        self.base_dir = Path(base_dir)
        # In user_backend/app/services/template_generator.py, change line 14:
        self.templates_dir = (
            self.base_dir / "user_backend" / "app" / "templates"
        )  # Add the correct path
        self.generated_dir = self.base_dir / "generated_templates"
        self.previews_dir = self.base_dir / "static" / "template_previews"
        self.integrator_path = self.base_dir / "sevdo_integrator.py"

        # Ensure directories exist
        self.generated_dir.mkdir(exist_ok=True)
        self.previews_dir.mkdir(parents=True, exist_ok=True)

        # Cache for generated templates
        self._generated_cache = {}

    async def generate_all_templates(self) -> Dict[str, Dict]:
        """Generate all available templates and create preview data"""
        results = {}

        if not self.templates_dir.exists():
            logger.error(f"Templates directory not found: {self.templates_dir}")
            return results

        # Find all template directories
        template_dirs = [
            d
            for d in self.templates_dir.iterdir()
            if d.is_dir() and (d / "template.json").exists()
        ]

        logger.info(f"Found {len(template_dirs)} templates to generate")

        for template_dir in template_dirs:
            template_name = template_dir.name
            try:
                result = await self.generate_template_preview(template_name)
                results[template_name] = result
                logger.info(f"✅ Generated preview for {template_name}")
            except Exception as e:
                logger.error(f"❌ Failed to generate {template_name}: {e}")
                results[template_name] = {"error": str(e), "success": False}

        return results

    async def generate_template_preview(self, template_name: str) -> Dict:
        """Generate a single template and create preview files"""
        template_dir = self.templates_dir / template_name

        if not template_dir.exists():
            raise FileNotFoundError(f"Template {template_name} not found")

        # Load template metadata
        metadata_file = template_dir / "template.json"
        if not metadata_file.exists():
            raise FileNotFoundError(f"template.json not found for {template_name}")

        with open(metadata_file) as f:
            template_metadata = json.load(f)

        # Generate output directory
        output_dir = self.generated_dir / f"{template_name}_generated"

        # Remove existing if present
        if output_dir.exists():
            shutil.rmtree(output_dir)

        # Run the integrator
        cmd = ["python", str(self.integrator_path), template_name, str(output_dir)]

        logger.info(f"🚀 Running integrator for {template_name}")
        logger.info(f"Command: {' '.join(cmd)}")

        result = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=str(self.base_dir),
        )

        stdout, stderr = await result.communicate()

        if result.returncode != 0:
            error_msg = stderr.decode() if stderr else "Unknown error"
            logger.error(f"Integrator failed for {template_name}: {error_msg}")
            raise RuntimeError(f"Integration failed: {error_msg}")

        # Process the generated output
        preview_data = await self._process_generated_output(
            template_name, output_dir, template_metadata
        )

        # Cache the result
        self._generated_cache[template_name] = {
            "generated_at": datetime.now().isoformat(),
            "output_dir": str(output_dir),
            "preview_data": preview_data,
            "metadata": template_metadata,
            "success": True,
        }

        logger.info(f"✅ Successfully generated {template_name}")
        return self._generated_cache[template_name]

    async def _process_generated_output(
        self, template_name: str, output_dir: Path, metadata: Dict
    ) -> Dict:
        """Process the generated template output and create preview data"""
        preview_data = {
            "template_name": template_name,
            "has_frontend": False,
            "has_backend": False,
            "frontend_files": [],
            "backend_files": [],
            "preview_html": None,
            "screenshot_url": None,
            "demo_url": None,
            "download_size": 0,
        }

        if not output_dir.exists():
            return preview_data

        # Check frontend
        frontend_dir = output_dir / "frontend"
        if frontend_dir.exists():
            preview_data["has_frontend"] = True

            # Find React components
            src_dir = frontend_dir / "src"
            if src_dir.exists():
                for file_path in src_dir.rglob("*.jsx"):
                    preview_data["frontend_files"].append(
                        {
                            "name": file_path.name,
                            "path": str(file_path.relative_to(output_dir)),
                            "size": file_path.stat().st_size,
                        }
                    )

            # Create HTML preview
            await self._create_html_preview(template_name, frontend_dir, preview_data)

        # Check backend
        backend_dir = output_dir / "backend"
        if backend_dir.exists():
            preview_data["has_backend"] = True

            for file_path in backend_dir.rglob("*.py"):
                if "__pycache__" not in str(file_path):
                    preview_data["backend_files"].append(
                        {
                            "name": file_path.name,
                            "path": str(file_path.relative_to(output_dir)),
                            "size": file_path.stat().st_size,
                        }
                    )

        # Calculate total size
        total_size = sum(
            f.stat().st_size
            for f in output_dir.rglob("*")
            if f.is_file() and "__pycache__" not in str(f)
        )
        preview_data["download_size"] = total_size

        return preview_data

    async def _create_html_preview(
        self, template_name: str, frontend_dir: Path, preview_data: Dict
    ):
        """Create a static HTML preview of the React app"""
        preview_html_dir = self.previews_dir / template_name
        preview_html_dir.mkdir(exist_ok=True)

        # Find the main App.js or index.html
        app_js = frontend_dir / "src" / "App.js"
        index_html = frontend_dir / "public" / "index.html"

        if index_html.exists():
            # Copy the HTML file and create a simple preview
            with open(index_html) as f:
                html_content = f.read()

            # Create a static preview version
            preview_html = self._create_static_preview(template_name, html_content)

            preview_file = preview_html_dir / "index.html"
            with open(preview_file, "w") as f:
                f.write(preview_html)

            preview_data["preview_html"] = (
                f"/static/template_previews/{template_name}/index.html"
            )

            # Copy any assets
            public_dir = frontend_dir / "public"
            if public_dir.exists():
                for asset_file in public_dir.rglob("*"):
                    if asset_file.is_file() and asset_file.name != "index.html":
                        dest_file = preview_html_dir / asset_file.name
                        shutil.copy2(asset_file, dest_file)

    def _create_static_preview(self, template_name: str, html_content: str) -> str:
        """Create a static HTML preview with mock data"""
        # This is a simplified version - you might want to use a proper React SSR solution
        preview_html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{template_name.title()} - Live Preview</title>
            <script src="https://cdn.tailwindcss.com"></script>
            <style>
                body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }}
                .preview-badge {{ 
                    position: fixed; top: 20px; right: 20px; z-index: 1000;
                    background: rgba(59, 130, 246, 0.9); color: white; 
                    padding: 8px 16px; border-radius: 20px; font-size: 14px;
                }}
            </style>
        </head>
        <body>
            <div class="preview-badge">
                🔍 Live Preview - {template_name.replace("_", " ").title()}
            </div>
            
            <!-- Generated content will be inserted here -->
            <div id="preview-content">
                {self._get_template_preview_content(template_name)}
            </div>
            
            <script>
                // Add some interactivity
                document.addEventListener('DOMContentLoaded', function() {{
                    // Make buttons clickable with preview behavior
                    document.querySelectorAll('button, .btn').forEach(btn => {{
                        btn.addEventListener('click', function(e) {{
                            e.preventDefault();
                            alert('This is a preview! Generate your own version to get full functionality.');
                        }});
                    }});
                    
                    // Make forms show preview behavior
                    document.querySelectorAll('form').forEach(form => {{
                        form.addEventListener('submit', function(e) {{
                            e.preventDefault();
                            alert('Form submission works in the generated version!');
                        }});
                    }});
                }});
            </script>
        </body>
        </html>
        """
        return preview_html

    def _get_template_preview_content(self, template_name: str) -> str:
        """Generate preview content based on template type"""
        if "restaurant" in template_name.lower():
            return """
            <div class="bg-white">
                <!-- Navigation -->
                <nav class="bg-white shadow-sm border-b">
                    <div class="max-w-7xl mx-auto px-4">
                        <div class="flex justify-between items-center h-16">
                            <div class="text-2xl font-bold text-gray-900">Bella Vista</div>
                            <div class="hidden md:flex space-x-8">
                                <a href="#" class="text-gray-600 hover:text-gray-900">Home</a>
                                <a href="#" class="text-gray-600 hover:text-gray-900">Menu</a>
                                <a href="#" class="text-gray-600 hover:text-gray-900">About</a>
                                <a href="#" class="text-gray-600 hover:text-gray-900">Contact</a>
                            </div>
                        </div>
                    </div>
                </nav>
                
                <!-- Hero Section -->
                <div class="bg-gradient-to-r from-amber-50 to-orange-50 py-20">
                    <div class="max-w-7xl mx-auto px-4 text-center">
                        <h1 class="text-5xl font-bold text-gray-900 mb-6">
                            Authentic Italian Cuisine
                        </h1>
                        <p class="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
                            Experience the finest flavors of Italy with our traditional recipes 
                            and fresh, locally sourced ingredients.
                        </p>
                        <div class="space-x-4">
                            <button class="bg-orange-600 text-white px-8 py-3 rounded-lg text-lg font-medium hover:bg-orange-700 transition">
                                View Menu
                            </button>
                            <button class="border-2 border-orange-600 text-orange-600 px-8 py-3 rounded-lg text-lg font-medium hover:bg-orange-50 transition">
                                Make Reservation
                            </button>
                        </div>
                    </div>
                </div>
                
                <!-- Features -->
                <div class="py-16 bg-white">
                    <div class="max-w-7xl mx-auto px-4">
                        <div class="text-center mb-12">
                            <h2 class="text-3xl font-bold text-gray-900 mb-4">Why Choose Bella Vista</h2>
                        </div>
                        <div class="grid md:grid-cols-3 gap-8">
                            <div class="text-center">
                                <div class="text-4xl mb-4">🍝</div>
                                <h3 class="text-xl font-semibold mb-2">Authentic Recipes</h3>
                                <p class="text-gray-600">Traditional Italian recipes passed down through generations</p>
                            </div>
                            <div class="text-center">
                                <div class="text-4xl mb-4">🌟</div>
                                <h3 class="text-xl font-semibold mb-2">Fresh Ingredients</h3>
                                <p class="text-gray-600">Locally sourced, premium ingredients in every dish</p>
                            </div>
                            <div class="text-center">
                                <div class="text-4xl mb-4">🏆</div>
                                <h3 class="text-xl font-semibold mb-2">Award Winning</h3>
                                <p class="text-gray-600">Recognized as the best Italian restaurant in the city</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            """

        # Add more template types as needed
        return f"""
        <div class="min-h-screen bg-gray-50 py-12">
            <div class="max-w-4xl mx-auto text-center">
                <h1 class="text-4xl font-bold text-gray-900 mb-8">
                    {template_name.replace("_", " ").title()} Template
                </h1>
                <p class="text-xl text-gray-600 mb-8">
                    This is a live preview of the generated website template.
                </p>
                <button class="bg-blue-600 text-white px-8 py-3 rounded-lg text-lg font-medium">
                    Get Started
                </button>
            </div>
        </div>
        """

    def get_generated_template(self, template_name: str) -> Optional[Dict]:
        """Get cached generated template data"""
        return self._generated_cache.get(template_name)

    def list_generated_templates(self) -> Dict[str, Dict]:
        """List all generated templates with their data"""
        return self._generated_cache.copy()

    async def regenerate_template(self, template_name: str) -> Dict:
        """Force regeneration of a template"""
        if template_name in self._generated_cache:
            del self._generated_cache[template_name]
        return await self.generate_template_preview(template_name)

    def get_template_download_path(self, template_name: str) -> Optional[Path]:
        """Get the path to download the generated template"""
        if template_name in self._generated_cache:
            return Path(self._generated_cache[template_name]["output_dir"])
        return None


# Create singleton instance
template_generator = TemplateGeneratorService()
