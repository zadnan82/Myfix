# # user_backend/scripts/generate_templates.py

# import asyncio
# import sys
# from pathlib import Path

# # Add the parent directory to Python path
# sys.path.append(str(Path(__file__).parent.parent))

# from app.services.template_generator import template_generator
# import logging

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)


# async def main():
#     """Generate all templates on startup"""
#     logger.info("🚀 Starting template generation process...")

#     try:
#         results = await template_generator.generate_all_templates()

#         success_count = sum(1 for r in results.values() if r.get("success", False))
#         total_count = len(results)

#         logger.info(
#             f"✅ Template generation complete: {success_count}/{total_count} successful"
#         )

#         for template_name, result in results.items():
#             if result.get("success"):
#                 logger.info(f"  ✅ {template_name}: Generated successfully")
#             else:
#                 logger.error(
#                     f"  ❌ {template_name}: {result.get('error', 'Unknown error')}"
#                 )

#         return results

#     except Exception as e:
#         logger.error(f"❌ Template generation failed: {e}")
#         return {}


# if __name__ == "__main__":
#     asyncio.run(main())
