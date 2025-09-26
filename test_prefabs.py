#!/usr/bin/env python3
"""
Test script to verify our updated prefabs work correctly.
"""
import sys
from pathlib import Path

# Add the current directory to the path for imports
sys.path.insert(0, str(Path(__file__).parent))

def test_prefab_imports():
    """Test that our updated prefabs can be imported and their functions called"""
    try:
        # Import the updated prefabs
        from sevdo_frontend.prefabs.article_layout import render_prefab as article_render
        from sevdo_frontend.prefabs.blog_list import render_prefab as blog_render
        from sevdo_frontend.prefabs.calendar_timeslots import render_prefab as calendar_render
        from sevdo_frontend.prefabs.add_to_cart import render_prefab as cart_render

        print("✅ All prefabs imported successfully!")

        # Test article layout
        result = article_render("", {"title": "Test Article"})
        assert "<Article />" in result
        print("✅ Article layout generates proper React component")

        # Test blog list
        result = blog_render("", {"title": "Test Blog"})
        assert "<BlogList />" in result
        print("✅ Blog list generates proper React component")

        # Test calendar
        result = calendar_render("", {"title": "Test Calendar"})
        assert "<CalendarTimeslots />" in result
        print("✅ Calendar generates proper React component")

        # Test cart
        result = cart_render("", {"title": "Test Cart"})
        assert "<AddToCart />" in result
        print("✅ Cart generates proper React component")

        print("\n🎉 All prefabs successfully converted to React patterns!")
        return True

    except Exception as e:
        print(f"❌ Error testing prefabs: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_prefab_imports()
    sys.exit(0 if success else 1)
