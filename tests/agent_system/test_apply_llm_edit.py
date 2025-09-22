import pytest
import tempfile
import requests
from pathlib import Path
from unittest.mock import patch, MagicMock
from agent_system.llm_editor import (
    apply_llm_edit, 
    LLMEditResult,
    _get_allowed_tokens,
    _build_system_prompt,
    _parse_change_from_task,
    _sevdo_rules_summary,
    _apply_token_arg_replacement,
    _extract_text_from_gpu_response,
    _post_and_parse,
    _call_gpu_endpoint_edit,
    _call_llm_edit
)


class TestApplyLLMEdit:
    """Tests for the apply_llm_edit function that handles specific file editing."""
    
    def test_apply_llm_edit_basic_functionality(self):
        """Test basic file editing functionality with mocked LLM."""
        # Create temporary test file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.s', delete=False) as f:
            f.write("h t i b")
            temp_path = f.name
        
        try:
            # Mock the LLM call to return modified content
            with patch('agent_system.llm_editor._call_llm_edit') as mock_llm:
                mock_llm.return_value = "h t i b lf"  # Added login form
                
                result = apply_llm_edit(
                    task="add login form",
                    file_path=temp_path,
                    dry_run=True  # Don't actually write to file
                )
            
            # Verify result structure
            assert isinstance(result, LLMEditResult)
            assert result.success is True
            assert result.modified is True
            assert result.original_code == "h t i b"
            assert result.modified_code == "h t i b lf"
            assert result.wrote_file is False  # dry_run=True
            assert result.file_path == temp_path
            
        finally:
            # Cleanup
            Path(temp_path).unlink()

    def test_apply_llm_edit_with_code_string(self):
        """Test editing with code string instead of file path."""
        original_code = "h t i"
        
        with patch('agent_system.llm_editor._call_llm_edit') as mock_llm:
            mock_llm.return_value = "h t i b"  # Added button
            
            result = apply_llm_edit(
                task="add button",
                code=original_code,
                dry_run=True
            )
        
        assert result.success is True
        assert result.modified is True
        assert result.original_code == "h t i"
        assert result.modified_code == "h t i b"
        assert result.file_path is None

    def test_apply_llm_edit_file_not_found(self):
        """Test error handling when file doesn't exist."""
        result = apply_llm_edit(
            task="add something",
            file_path="/nonexistent/file.s"
        )
        
        assert result.success is False
        assert result.message == "File not found."
        assert result.wrote_file is False

    def test_apply_llm_edit_no_file_or_code(self):
        """Test error handling when neither file_path nor code provided."""
        result = apply_llm_edit(task="add something")
        
        assert result.success is False
        assert result.message == "Provide either file_path or code."
        assert result.wrote_file is False

    def test_apply_llm_edit_actual_file_write(self):
        """Test actual file writing when dry_run=False."""
        # Create temporary test file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.s', delete=False) as f:
            f.write("h t i")
            temp_path = f.name
        
        try:
            with patch('agent_system.llm_editor._call_llm_edit') as mock_llm:
                mock_llm.return_value = "h t i b"  # Added button
                
                result = apply_llm_edit(
                    task="add button",
                    file_path=temp_path,
                    dry_run=False  # Actually write to file
                )
            
            # Verify file was actually modified
            assert result.success is True
            assert result.wrote_file is True
            
            # Check file contents
            with open(temp_path, 'r') as f:
                content = f.read()
            assert content == "h t i b"
            
        finally:
            # Cleanup
            Path(temp_path).unlink()

    def test_apply_llm_edit_llm_call_error(self):
        """Test error handling when LLM call fails."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.s', delete=False) as f:
            f.write("h t i")
            temp_path = f.name
        
        try:
            with patch('agent_system.llm_editor._call_llm_edit') as mock_llm:
                mock_llm.side_effect = Exception("LLM connection failed")
                
                result = apply_llm_edit(
                    task="add something",
                    file_path=temp_path,
                    dry_run=True
                )
            
            assert result.success is False
            assert "LLM connection failed" in result.message
            assert result.wrote_file is False
            
        finally:
            Path(temp_path).unlink()

    def test_apply_llm_edit_with_gpu_base_url(self):
        """Test that GPU base URL is passed through correctly."""
        original_code = "h t"
        gpu_url = "http://192.168.16.103:8000"
        
        with patch('agent_system.llm_editor._call_llm_edit') as mock_llm:
            mock_llm.return_value = "h t i"
            
            result = apply_llm_edit(
                task="add input",
                code=original_code,
                gpu_base_url=gpu_url,
                dry_run=True
            )
        
        # Verify GPU URL was passed to the LLM call
        mock_llm.assert_called_once()
        call_args = mock_llm.call_args
        assert call_args[1]['gpu_base_url'] == gpu_url
        
        assert result.success is True
        assert result.modified is True

    def test_apply_llm_edit_result_serialization(self):
        """Test that LLMEditResult can be serialized to dict properly."""
        with patch('agent_system.llm_editor._call_llm_edit') as mock_llm:
            mock_llm.return_value = "h t i b"
            
            result = apply_llm_edit(
                task="add button",
                code="h t i",
                dry_run=True
            )
        
        # Test serialization
        result_dict = result.to_response()
        
        assert isinstance(result_dict, dict)
        assert result_dict['status'] == 'success'
        assert result_dict['success'] is True
        assert result_dict['modified'] is True
        assert result_dict['original_code'] == "h t i"
        assert result_dict['modified_code'] == "h t i b"
        assert result_dict['error'] is None


class TestLLMEditorHelperFunctions:
    """Tests for helper functions in llm_editor module to improve coverage."""
    
    def test_get_allowed_tokens(self):
        """Test that allowed tokens are loaded correctly."""
        with patch('agent_system.llm_editor.AgentRAGService') as mock_rag:
            # Mock RAG service to return some tokens
            mock_service = MagicMock()
            mock_service.get_all_tokens.return_value = ['h', 't', 'i', 'b', 'lf', 'rf']
            mock_rag.return_value = mock_service
            
            tokens = _get_allowed_tokens()
            
            assert isinstance(tokens, list)
            assert len(tokens) > 0
            assert 'h' in tokens
            assert 't' in tokens

    def test_get_allowed_tokens_no_rag(self):
        """Test fallback when RAG service is not available."""
        with patch('agent_system.llm_editor.AgentRAGService', None):
            tokens = _get_allowed_tokens()
            
            assert isinstance(tokens, list)
            # Should return empty list or basic fallback tokens
            
    def test_build_system_prompt(self):
        """Test system prompt generation with allowed tokens."""
        test_tokens = ["h", "t", "i", "b", "lf"]
        
        prompt = _build_system_prompt(test_tokens)
        
        assert isinstance(prompt, str)
        assert len(prompt) > 0
        assert "SEVDO" in prompt
        assert "b, h, i, lf, t" in prompt  # Should be alphabetically sorted
        assert "precise" in prompt.lower()

    def test_sevdo_rules_summary(self):
        """Test SEVDO rules summary generation."""
        rules = _sevdo_rules_summary()
        
        assert isinstance(rules, str)
        assert len(rules) > 0
        assert "SEVDO" in rules
        assert any(word in rules.lower() for word in ["token", "rule", "format"])

    def test_parse_change_from_task_simple(self):
        """Test parsing simple task strings."""
        # Test simple add task
        token, search, replace = _parse_change_from_task("add button")
        assert search is None or replace is None  # Simple task format
        
        # Test more complex task
        token, search, replace = _parse_change_from_task("change login to register")
        # Depending on implementation, may extract search/replace pairs
        
    def test_parse_change_from_task_complex(self):
        """Test parsing complex change tasks."""
        task = "modify h token: change 'Welcome' to 'Hello'"
        token, search, replace = _parse_change_from_task(task)
        
        # Test that function handles complex parsing
        # (exact behavior depends on implementation)
        assert isinstance(token, (str, type(None)))
        assert isinstance(search, (str, type(None))) 
        assert isinstance(replace, (str, type(None)))

    def test_apply_token_arg_replacement(self):
        """Test token argument replacement functionality."""
        original_text = "Welcome to the site"
        
        result = _apply_token_arg_replacement(
            text=original_text,
            token="h",
            search="Welcome",
            replace="Hello"
        )
        
        # Function returns (modified_text, replacement_count)
        assert isinstance(result, tuple)
        assert len(result) == 2
        modified_text, count = result
        assert isinstance(modified_text, str)
        assert isinstance(count, int)
        
    def test_apply_token_arg_replacement_no_token(self):
        """Test token replacement when no token specified."""
        original_text = "Welcome to the site"
        
        result = _apply_token_arg_replacement(
            text=original_text,
            token=None,
            search="Welcome", 
            replace="Hello"
        )
        
        # Function returns (modified_text, replacement_count)
        assert isinstance(result, tuple)
        assert len(result) == 2
        modified_text, count = result
        assert isinstance(modified_text, str)
        assert isinstance(count, int)

    def test_extract_text_from_gpu_response_string(self):
        """Test extracting text from GPU response when it's a string."""
        response = "This is the response content"
        
        result = _extract_text_from_gpu_response(response)
        
        assert result == "This is the response content"

    def test_extract_text_from_gpu_response_dict_message(self):
        """Test extracting text from GPU response with message structure."""
        response = {
            "message": {
                "content": "This is the actual content"
            }
        }
        
        result = _extract_text_from_gpu_response(response)
        
        assert result == "This is the actual content"

    def test_extract_text_from_gpu_response_dict_content(self):
        """Test extracting text from GPU response with direct content."""
        response = {
            "content": "Direct content response"
        }
        
        result = _extract_text_from_gpu_response(response)
        
        assert result == "Direct content response"

    def test_extract_text_from_gpu_response_dict_text(self):
        """Test extracting text from GPU response with text field."""
        response = {
            "text": "Text field response"
        }
        
        result = _extract_text_from_gpu_response(response)
        
        assert result == "Text field response"

    def test_extract_text_from_gpu_response_fallback(self):
        """Test extraction fallback for unknown response format."""
        response = {
            "unknown_field": "some value",
            "status": "success"
        }
        
        result = _extract_text_from_gpu_response(response)
        
        # Should return empty string or some fallback value
        assert isinstance(result, str)


class TestLLMEditorGPUIntegration:
    """Tests for GPU server integration and HTTP calls to improve coverage."""
    
    @patch('agent_system.llm_editor.requests.post')
    def test_post_and_parse_success(self, mock_post):
        """Test successful HTTP POST to GPU endpoint."""
        # Mock successful response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"content": "Modified SEVDO code"}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        result = _post_and_parse("http://test.com/endpoint", timeout=30)
        
        assert result == "Modified SEVDO code"
        mock_post.assert_called_once_with("http://test.com/endpoint", timeout=30)

    @patch('agent_system.llm_editor.requests.post')
    def test_post_and_parse_404_error(self, mock_post):
        """Test 404 error handling in HTTP POST."""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_post.return_value = mock_response
        
        with pytest.raises(requests.HTTPError):
            _post_and_parse("http://test.com/endpoint", timeout=30)

    @patch('agent_system.llm_editor.requests.post')
    def test_post_and_parse_network_error(self, mock_post):
        """Test network error handling in HTTP POST."""
        mock_post.side_effect = requests.ConnectionError("Connection failed")
        
        with pytest.raises(RuntimeError, match="Network error"):
            _post_and_parse("http://test.com/endpoint", timeout=30)

    @patch('agent_system.llm_editor.requests.post')
    def test_post_and_parse_http_error(self, mock_post):
        """Test HTTP error status codes."""
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_response.raise_for_status.side_effect = requests.HTTPError("500 Server Error")
        mock_post.return_value = mock_response
        
        with pytest.raises(RuntimeError, match="GPU endpoint returned 500"):
            _post_and_parse("http://test.com/endpoint", timeout=30)

    @patch('agent_system.llm_editor.requests.post')
    def test_post_and_parse_json_error(self, mock_post):
        """Test handling of non-JSON response."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_response.text = "Plain text response"
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        result = _post_and_parse("http://test.com/endpoint", timeout=30)
        
        assert result == "Plain text response"

    @patch('agent_system.llm_editor.requests.post')
    def test_post_and_parse_empty_response(self, mock_post):
        """Test handling of empty response."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"message": {"content": ""}}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        with pytest.raises(RuntimeError, match="did not contain usable"):
            _post_and_parse("http://test.com/endpoint", timeout=30)

    @patch('agent_system.llm_editor._post_and_parse')
    def test_call_gpu_endpoint_edit_success(self, mock_post_parse):
        """Test successful GPU endpoint call."""
        mock_post_parse.return_value = "h t i b lf"
        
        result = _call_gpu_endpoint_edit(
            base_url="http://192.168.16.103:8000",
            model="llama3.2:3b", 
            prompt_text="Add login form to: h t i"
        )
        
        assert result == "h t i b lf"
        assert mock_post_parse.call_count >= 1  # May try multiple endpoints

    @patch('agent_system.llm_editor._post_and_parse')
    def test_call_gpu_endpoint_edit_fallback(self, mock_post_parse):
        """Test GPU endpoint fallback to different URLs."""
        # Create proper 404 HTTPError with response
        error_404 = requests.HTTPError("404 Not Found")
        mock_response = MagicMock()
        mock_response.status_code = 404
        error_404.response = mock_response
        
        # First call fails with 404, second succeeds
        mock_post_parse.side_effect = [
            error_404,
            "h t i b"
        ]
        
        result = _call_gpu_endpoint_edit(
            base_url="http://192.168.16.103:8000",
            model="llama3.2:3b",
            prompt_text="Add button: h t i"
        )
        
        assert result == "h t i b"
        assert mock_post_parse.call_count == 2

    @patch('agent_system.llm_editor.ollama.chat')
    def test_call_llm_edit_local_ollama(self, mock_ollama):
        """Test local Ollama call when no GPU URL provided."""
        mock_ollama.return_value = {
            "message": {
                "content": "h t i b"
            }
        }
        
        result = _call_llm_edit(
            task="add button",
            code="h t i",
            model="deepseek-coder:6.7b",
            allowed_tokens=["h", "t", "i", "b"],
            gpu_base_url=None  # Use local Ollama
        )
        
        assert result == "h t i b"
        mock_ollama.assert_called_once()

    @patch('agent_system.llm_editor.ollama.chat')
    def test_call_llm_edit_ollama_error(self, mock_ollama):
        """Test error handling in local Ollama call."""
        mock_ollama.side_effect = Exception("Ollama connection failed")
        
        with pytest.raises(Exception, match="Ollama connection failed"):
            _call_llm_edit(
                task="add button",
                code="h t i", 
                model="deepseek-coder:6.7b",
                allowed_tokens=["h", "t", "i", "b"],
                gpu_base_url=None
            )

    @patch('agent_system.llm_editor._call_gpu_endpoint_edit')
    def test_call_llm_edit_gpu_path(self, mock_gpu_call):
        """Test GPU path in _call_llm_edit."""
        mock_gpu_call.return_value = "h t i b lf"
        
        result = _call_llm_edit(
            task="add login form",
            code="h t i",
            model="llama3.2:3b",
            allowed_tokens=["h", "t", "i", "b", "lf"],
            gpu_base_url="http://192.168.16.103:8000"
        )
        
        assert result == "h t i b lf"
        mock_gpu_call.assert_called_once()

    def test_get_allowed_tokens_exception_handling(self):
        """Test exception handling in _get_allowed_tokens."""
        with patch('agent_system.llm_editor.AgentRAGService') as mock_rag:
            # Make RAG service initialization raise an exception
            mock_rag.side_effect = Exception("RAG initialization failed")
            
            # Should fall back to default tokens
            tokens = _get_allowed_tokens()
            
            assert isinstance(tokens, list)
            assert len(tokens) > 0
            # Should contain fallback tokens
            assert "h" in tokens
            assert "t" in tokens
