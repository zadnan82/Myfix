import pytest
import json
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock
from agent_system.sprintmaster import plan_subtasks, execute_task, discover_sevdo_files, generate_file_paths


class TestPlanSubtasksLLMCalls:
    """Tests for LLM calling functionality in plan_subtasks."""
    
    def test_plan_subtasks_successful_llm_call(self):
        """Test successful LLM call with proper JSON response."""
        # Mock structured JSON response from Ollama
        mock_response = {
            "message": {
                "content": json.dumps({
                    "subtasks": [
                        {"task": "Create login form component", "difficulty": 2},
                        {"task": "Add authentication logic", "difficulty": 3},
                        {"task": "Update navigation menu", "difficulty": 1}
                    ]
                })
            }
        }
        
        with patch('agent_system.sprintmaster.ollama.chat', return_value=mock_response) as mock_chat:
            with patch('agent_system.sprintmaster.discover_sevdo_files', return_value={}):
                result = plan_subtasks("create user login system")
        
        # Verify LLM was called correctly
        mock_chat.assert_called_once()
        call_args = mock_chat.call_args
        
        # Check that proper messages were sent
        messages = call_args[1]['messages']
        assert len(messages) == 2
        assert messages[0]['role'] == 'system'
        assert messages[1]['role'] == 'user'
        assert 'sprintmaster' in messages[0]['content'].lower()
        assert 'create user login system' in messages[1]['content']
        
        # Check JSON format was specified
        assert 'format' in call_args[1]
        format_spec = call_args[1]['format']
        assert format_spec['type'] == 'object'
        assert 'subtasks' in format_spec['properties']
        
        # Check model and options
        assert call_args[1]['model'] == 'llama3.2:latest'
        assert call_args[1]['options']['temperature'] == 0.5
        
        # Verify parsed result
        assert 'subtasks' in result
        assert len(result['subtasks']) == 3
        assert result['subtasks'][0]['task'] == "Create login form component"
        assert result['subtasks'][0]['difficulty'] == 2

    def test_plan_subtasks_with_existing_files_context(self):
        """Test that existing files are included in LLM prompt."""
        existing_files = {
            "templates/user_site/frontend/Home.s": "h t i b",
            "templates/user_site/frontend/Login.s": "h t i lf rf"
        }
        
        mock_response = {
            "message": {
                "content": json.dumps({
                    "subtasks": [
                        {"task": "Modify templates/user_site/frontend/Login.s: add validation", "difficulty": 2}
                    ]
                })
            }
        }
        
        with patch('agent_system.sprintmaster.ollama.chat', return_value=mock_response) as mock_chat:
            with patch('agent_system.sprintmaster.discover_sevdo_files', return_value=existing_files):
                result = plan_subtasks("improve login validation")
        
        # Check that file context was included in system prompt
        call_args = mock_chat.call_args
        system_prompt = call_args[1]['messages'][0]['content']
        
        assert "Existing SEVDO files in project:" in system_prompt
        assert "templates/user_site/frontend/Home.s: h t i b" in system_prompt
        assert "templates/user_site/frontend/Login.s: h t i lf rf" in system_prompt
        assert "reference them specifically in subtasks" in system_prompt

    def test_plan_subtasks_json_parsing_error(self):
        """Test error handling when LLM returns invalid JSON."""
        # Mock invalid JSON response
        mock_response = {
            "message": {
                "content": "This is not valid JSON - just plain text response"
            }
        }
        
        with patch('agent_system.sprintmaster.ollama.chat', return_value=mock_response):
            with patch('agent_system.sprintmaster.discover_sevdo_files', return_value={}):
                result = plan_subtasks("create something")
        
        # Should fall back to default subtask structure
        assert 'subtasks' in result
        assert len(result['subtasks']) == 1
        assert result['subtasks'][0]['description'] == "Complete the task"
        assert result['subtasks'][0]['difficulty'] == 2

    def test_plan_subtasks_missing_subtasks_key(self):
        """Test error handling when JSON is valid but missing 'subtasks' key."""
        # Mock valid JSON but wrong structure
        mock_response = {
            "message": {
                "content": json.dumps({
                    "tasks": [  # Wrong key name
                        {"task": "Do something", "difficulty": 1}
                    ]
                })
            }
        }
        
        with patch('agent_system.sprintmaster.ollama.chat', return_value=mock_response):
            with patch('agent_system.sprintmaster.discover_sevdo_files', return_value={}):
                result = plan_subtasks("create feature")
        
        # Should fall back to default structure
        assert 'subtasks' in result
        assert len(result['subtasks']) == 1
        assert result['subtasks'][0]['description'] == "Complete the task"

    def test_plan_subtasks_ollama_connection_error(self):
        """Test error handling when Ollama call fails completely."""
        with patch('agent_system.sprintmaster.ollama.chat', side_effect=Exception("Connection to Ollama failed")):
            with patch('agent_system.sprintmaster.discover_sevdo_files', return_value={}):
                # Should raise the exception (no fallback for connection errors)
                with pytest.raises(Exception, match="Connection to Ollama failed"):
                    plan_subtasks("create feature")

    def test_plan_subtasks_different_models(self):
        """Test that different models can be specified."""
        mock_response = {
            "message": {
                "content": json.dumps({
                    "subtasks": [{"task": "Test task", "difficulty": 1}]
                })
            }
        }
        
        with patch('agent_system.sprintmaster.ollama.chat', return_value=mock_response) as mock_chat:
            with patch('agent_system.sprintmaster.discover_sevdo_files', return_value={}):
                plan_subtasks("test task", model="deepseek-coder:6.7b")
        
        # Verify correct model was used
        call_args = mock_chat.call_args
        assert call_args[1]['model'] == "deepseek-coder:6.7b"

    def test_plan_subtasks_temperature_setting(self):
        """Test that temperature is set correctly for creative planning."""
        mock_response = {
            "message": {
                "content": json.dumps({
                    "subtasks": [{"task": "Creative task", "difficulty": 2}]
                })
            }
        }
        
        with patch('agent_system.sprintmaster.ollama.chat', return_value=mock_response) as mock_chat:
            with patch('agent_system.sprintmaster.discover_sevdo_files', return_value={}):
                plan_subtasks("be creative")
        
        # Verify temperature is 0.5 (more creative than file paths at 0.3)
        call_args = mock_chat.call_args
        assert call_args[1]['options']['temperature'] == 0.5


class TestExecuteTaskLLMIntegration:
    """Tests for LLM integration in execute_task coordination."""
    
    def test_execute_task_full_llm_pipeline(self):
        """Test complete LLM pipeline from planning to execution."""
        # Mock plan_subtasks response
        mock_plan_response = {
            "message": {
                "content": json.dumps({
                    "subtasks": [
                        {"task": "Create login form", "difficulty": 2},
                        {"task": "Add authentication", "difficulty": 3}
                    ]
                })
            }
        }
        
        # Mock solve_subtask results
        mock_subtask_results = [
            {"task": "Create login form", "success": True, "tokens": "h t i lf rf"},
            {"task": "Add authentication", "success": True, "tokens": "l r m o"}
        ]
        
        with patch('agent_system.sprintmaster.ollama.chat', return_value=mock_plan_response):
            with patch('agent_system.sprintmaster.discover_sevdo_files', return_value={}):
                with patch('agent_system.sprintmaster.solve_subtask', side_effect=mock_subtask_results):
                    result = execute_task("create user authentication system")
        
        # Verify complete pipeline worked
        assert result['task'] == "create user authentication system"
        assert len(result['subtasks']) == 2
        assert len(result['results']) == 2
        
        # Check that subtasks were executed
        assert result['results'][0]['task'] == "Create login form"
        assert result['results'][1]['task'] == "Add authentication"

    def test_execute_task_with_rag_service(self):
        """Test that RAG service is properly initialized and used."""
        mock_plan_response = {
            "message": {
                "content": json.dumps({
                    "subtasks": [{"task": "Use RAG context", "difficulty": 1}]
                })
            }
        }
        
        with patch('agent_system.sprintmaster.ollama.chat', return_value=mock_plan_response):
            with patch('agent_system.sprintmaster.discover_sevdo_files', return_value={}):
                with patch('agent_system.sprintmaster.AgentRAGService') as mock_rag_class:
                    with patch('agent_system.sprintmaster.solve_subtask') as mock_solve:
                        mock_rag_instance = MagicMock()
                        mock_rag_class.return_value = mock_rag_instance
                        mock_solve.return_value = {"task": "Done", "success": True}
                        
                        result = execute_task("test rag integration")
        
        # Verify RAG service was initialized
        mock_rag_class.assert_called_once()
        
        # Verify solve_subtask was called with RAG service
        mock_solve.assert_called()
        call_args = mock_solve.call_args
        assert call_args[0][1] == mock_rag_instance  # Second argument should be RAG service

    def test_execute_task_handles_subtask_format_compatibility(self):
        """Test handling of different subtask formats (dict vs string)."""
        # Mock plan_subtasks to return mixed format
        mock_plan_response = {
            "message": {
                "content": json.dumps({
                    "subtasks": [
                        {"task": "Dict format task", "difficulty": 2},
                        "String format task"  # Sometimes fallback creates strings
                    ]
                })
            }
        }
        
        with patch('agent_system.sprintmaster.ollama.chat', return_value=mock_plan_response):
            with patch('agent_system.sprintmaster.discover_sevdo_files', return_value={}):
                with patch('agent_system.sprintmaster.solve_subtask') as mock_solve:
                    mock_solve.return_value = {"success": True}
                    
                    result = execute_task("mixed format test")
        
        # Verify both formats were handled
        assert mock_solve.call_count == 2
        call1_task = mock_solve.call_args_list[0][0][0]
        call2_task = mock_solve.call_args_list[1][0][0]
        
        assert call1_task == "Dict format task"
        assert call2_task == "String format task"

    def test_execute_task_different_models(self):
        """Test execute_task with different LLM models."""
        mock_plan_response = {
            "message": {
                "content": json.dumps({
                    "subtasks": [{"task": "Test task", "difficulty": 1}]
                })
            }
        }
        
        with patch('agent_system.sprintmaster.ollama.chat', return_value=mock_plan_response) as mock_chat:
            with patch('agent_system.sprintmaster.discover_sevdo_files', return_value={}):
                with patch('agent_system.sprintmaster.solve_subtask') as mock_solve:
                    mock_solve.return_value = {"success": True}
                    
                    execute_task(
                        "test different models",
                        master_model="llama3.2:3b",
                        code_model="deepseek-coder:latest"
                    )
        
        # Verify planning used master_model
        call_args = mock_chat.call_args
        assert call_args[1]['model'] == "llama3.2:3b"
        
        # Verify coding used code_model
        solve_call_args = mock_solve.call_args
        assert solve_call_args[1]['model'] == "deepseek-coder:latest"

    def test_execute_task_error_propagation(self):
        """Test that LLM errors are properly propagated."""
        with patch('agent_system.sprintmaster.ollama.chat', side_effect=Exception("LLM service down")):
            with patch('agent_system.sprintmaster.discover_sevdo_files', return_value={}):
                with pytest.raises(Exception, match="LLM service down"):
                    execute_task("this will fail")

    def test_execute_task_rag_initialization_failure(self):
        """Test error propagation when RAG service initialization fails."""
        with patch('agent_system.sprintmaster.AgentRAGService', side_effect=Exception("RAG initialization failed")):
            # Should propagate the RAG initialization error
            with pytest.raises(Exception, match="RAG initialization failed"):
                execute_task("test rag failure")


class TestSprintmasterUtilityFunctions:
    """Tests for utility functions to improve sprintmaster.py coverage."""
    
    def test_discover_sevdo_files_basic_functionality(self):
        """Test discover_sevdo_files basic functionality."""
        # Create a simple mock of file system
        mock_files = ["templates/test/Home.s", "templates/test/Login.s"]
        mock_content = {"Home.s": "h t i b", "Login.s": "h t i lf rf"}
        
        with patch('agent_system.sprintmaster.Path') as mock_path:
            # Mock the path traversal
            mock_root = MagicMock()
            mock_templates = MagicMock()
            mock_templates.exists.return_value = True
            
            # Mock rglob to return mock file paths
            mock_file_paths = []
            for file_name in mock_files:
                mock_file = MagicMock()
                mock_file.read_text.return_value = mock_content.get(file_name.split("/")[-1], "")
                mock_file.relative_to.return_value = file_name
                mock_file_paths.append(mock_file)
            
            mock_templates.rglob.return_value = mock_file_paths
            mock_root.__truediv__.return_value = mock_templates
            mock_path.return_value.parent.parent = mock_root
            
            result = discover_sevdo_files()
        
        # Should return dictionary with file paths and content
        assert isinstance(result, dict)

    def test_discover_sevdo_files_no_templates_dir(self):
        """Test discover_sevdo_files when templates directory doesn't exist."""
        with patch('agent_system.sprintmaster.Path') as mock_path:
            mock_root = MagicMock()
            mock_templates = MagicMock()
            mock_templates.exists.return_value = False
            mock_root.__truediv__.return_value = mock_templates
            mock_path.return_value.parent.parent = mock_root
            
            result = discover_sevdo_files()
        
        assert result == {}

    def test_discover_sevdo_files_read_error(self):
        """Test discover_sevdo_files handles file read errors."""
        with patch('agent_system.sprintmaster.Path') as mock_path:
            mock_root = MagicMock()
            mock_templates = MagicMock()
            mock_templates.exists.return_value = True
            
            # Mock a file that raises exception when reading
            mock_file = MagicMock()
            mock_file.read_text.side_effect = Exception("Permission denied")
            mock_file.relative_to.return_value = "templates/error/File.s"
            
            mock_templates.rglob.return_value = [mock_file]
            mock_root.__truediv__.return_value = mock_templates
            mock_path.return_value.parent.parent = mock_root
            
            # Should handle error gracefully
            result = discover_sevdo_files()
            assert isinstance(result, dict)

    def test_generate_file_paths_empty_content(self):
        """Test generate_file_paths with empty AI response."""
        mock_response = {
            "message": {
                "content": ""
            }
        }
        
        with patch('agent_system.sprintmaster.ollama.chat', return_value=mock_response):
            with patch('agent_system.sprintmaster.discover_sevdo_files', return_value={}):
                result = generate_file_paths("empty test")
        
        assert result == []

    def test_generate_file_paths_whitespace_content(self):
        """Test generate_file_paths with whitespace-only response."""
        mock_response = {
            "message": {
                "content": "   \n\n   \t   \n   "
            }
        }
        
        with patch('agent_system.sprintmaster.ollama.chat', return_value=mock_response):
            with patch('agent_system.sprintmaster.discover_sevdo_files', return_value={}):
                result = generate_file_paths("whitespace test")
        
        assert result == []

    def test_generate_file_paths_mixed_content(self):
        """Test generate_file_paths with mixed valid/invalid content."""
        mock_response = {
            "message": {
                "content": """
                Here are the files:
                - templates/Home.s
                Some explanatory text
                - components/Button.jsx
                More text without paths
                - api/routes.py
                """
            }
        }
        
        with patch('agent_system.sprintmaster.ollama.chat', return_value=mock_response):
            with patch('agent_system.sprintmaster.discover_sevdo_files', return_value={}):
                result = generate_file_paths("mixed content test")
        
        expected = [
            "templates/Home.s",
            "components/Button.jsx", 
            "api/routes.py"
        ]
        assert result == expected

    def test_generate_file_paths_backtick_extraction(self):
        """Test backtick extraction in generate_file_paths."""
        mock_response = {
            "message": {
                "content": """
                Files to create:
                `templates/Profile.s` - User profile
                `utils/helpers.py` - Utility functions
                File path: `components/Nav.jsx`
                """
            }
        }
        
        with patch('agent_system.sprintmaster.ollama.chat', return_value=mock_response):
            with patch('agent_system.sprintmaster.discover_sevdo_files', return_value={}):
                result = generate_file_paths("backtick test")
        
        expected = [
            "templates/Profile.s",
            "utils/helpers.py",
            "components/Nav.jsx"
        ]
        assert result == expected

    def test_generate_file_paths_complex_bullet_points(self):
        """Test complex bullet point cleaning."""
        mock_response = {
            "message": {
                "content": """
                1. templates/Home.s
                2. components/Header.jsx
                * api/users.py
                - utils/validation.py
                • templates/Login.s
                5. backend/models.py
                """
            }
        }
        
        with patch('agent_system.sprintmaster.ollama.chat', return_value=mock_response):
            with patch('agent_system.sprintmaster.discover_sevdo_files', return_value={}):
                result = generate_file_paths("complex bullets test")
        
        # Note: • bullet point is not cleaned by current code
        expected = [
            "templates/Home.s",
            "components/Header.jsx",
            "api/users.py",
            "utils/validation.py",
            "backend/models.py"
        ]
        assert result == expected

    def test_generate_file_paths_with_existing_context(self):
        """Test that existing files appear in system prompt."""
        existing_files = {
            "templates/existing/Home.s": "h t i",
            "templates/existing/About.s": "h t i b"
        }
        
        mock_response = {
            "message": {
                "content": "- templates/existing/Contact.s"
            }
        }
        
        with patch('agent_system.sprintmaster.ollama.chat', return_value=mock_response) as mock_chat:
            with patch('agent_system.sprintmaster.discover_sevdo_files', return_value=existing_files):
                result = generate_file_paths("add contact page")
        
        # Verify existing files context in system prompt
        call_args = mock_chat.call_args
        system_prompt = call_args[1]['messages'][0]['content']
        assert "Existing files in project:" in system_prompt
        assert "templates/existing/Home.s" in system_prompt
        assert "templates/existing/About.s" in system_prompt
        
        assert result == ["templates/existing/Contact.s"]

    def test_generate_file_paths_no_existing_files(self):
        """Test generate_file_paths when no existing files found."""
        mock_response = {
            "message": {
                "content": "- templates/new/Page.s"
            }
        }
        
        with patch('agent_system.sprintmaster.ollama.chat', return_value=mock_response) as mock_chat:
            with patch('agent_system.sprintmaster.discover_sevdo_files', return_value={}):
                result = generate_file_paths("create new page")
        
        # Verify no file context added to prompt when no existing files
        call_args = mock_chat.call_args
        system_prompt = call_args[1]['messages'][0]['content']
        assert "Existing files in project:" not in system_prompt
        
        assert result == ["templates/new/Page.s"]
