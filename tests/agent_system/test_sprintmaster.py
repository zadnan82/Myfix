import pytest
from unittest.mock import patch, MagicMock
from agent_system.sprintmaster import generate_file_paths


class TestGenerateFilePaths:
    """Tests for the generate_file_paths function."""
    
    def test_basic_functionality_with_mock_ollama(self):
        """Test basic file path generation with mocked Ollama response."""
        # Mock Ollama response
        mock_response = {
            "message": {
                "content": "- templates/user_site/frontend/Profile.s\n- user_frontend/components/UserMenu.jsx\n- user_backend/routes/profile.py"
            }
        }
        
        with patch('agent_system.sprintmaster.ollama.chat', return_value=mock_response):
            with patch('agent_system.sprintmaster.discover_sevdo_files', return_value={}):
                result = generate_file_paths("create user profile")
        
        expected = [
            "templates/user_site/frontend/Profile.s",
            "user_frontend/components/UserMenu.jsx", 
            "user_backend/routes/profile.py"
        ]
        
        assert result == expected

    def test_path_parsing_with_bullet_points(self):
        """Test parsing of different bullet point formats."""
        mock_response = {
            "message": {
                "content": "1. templates/blog/Home.s\n* frontend/components/Blog.jsx\n- backend/api/blog.py"
            }
        }
        
        with patch('agent_system.sprintmaster.ollama.chat', return_value=mock_response):
            with patch('agent_system.sprintmaster.discover_sevdo_files', return_value={}):
                result = generate_file_paths("create blog")
        
        expected = [
            "templates/blog/Home.s",
            "frontend/components/Blog.jsx",
            "backend/api/blog.py"
        ]
        
        assert result == expected

    def test_empty_response_handling(self):
        """Test handling of empty or invalid responses."""
        mock_response = {
            "message": {
                "content": "No files needed for this task."
            }
        }
        
        with patch('agent_system.sprintmaster.ollama.chat', return_value=mock_response):
            with patch('agent_system.sprintmaster.discover_sevdo_files', return_value={}):
                result = generate_file_paths("simple task")
        
        # Should return empty list when no valid paths found
        assert result == []

    def test_ollama_error_handling(self):
        """Test error handling when Ollama call fails."""
        with patch('agent_system.sprintmaster.ollama.chat', side_effect=Exception("Connection failed")):
            with patch('agent_system.sprintmaster.discover_sevdo_files', return_value={}):
                result = generate_file_paths("test task")
        
        # Should return empty list on error
        assert result == []

    def test_with_existing_files_context(self):
        """Test that existing files are included in context."""
        existing_files = {
            "templates/fitness_site/frontend/Home.s": "h t i b lf rf",
            "templates/blog_site/frontend/Contact.s": "h t i b"
        }
        
        mock_response = {
            "message": {
                "content": "- templates/fitness_site/frontend/Programs.s\n- templates/fitness_site/frontend/Home.s"
            }
        }
        
        with patch('agent_system.sprintmaster.ollama.chat', return_value=mock_response) as mock_chat:
            with patch('agent_system.sprintmaster.discover_sevdo_files', return_value=existing_files):
                result = generate_file_paths("add fitness programs")
        
        # Verify that existing files were included in the prompt
        call_args = mock_chat.call_args
        system_prompt = call_args[1]['messages'][0]['content']
        
        assert "Existing files in project:" in system_prompt
        assert "templates/fitness_site/frontend/Home.s" in system_prompt
        assert "templates/blog_site/frontend/Contact.s" in system_prompt
        
        # Verify returned paths
        expected = [
            "templates/fitness_site/frontend/Programs.s",
            "templates/fitness_site/frontend/Home.s"
        ]
        assert result == expected
