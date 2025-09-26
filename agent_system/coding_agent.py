from typing import Dict, Any
from fastapi import logger
import requests
import random
import os

from agent_system.rag_integration import AgentRAGService


def compile_tokens(tokens: str, is_frontend: bool) -> Dict[str, Any]:
    """Compile SEVDO tokens to actual code using the compiler APIs."""
    with open(
        f"playground/input_files/generated_code{random.randint(1, 1000000)}.txt",
        "w",
    ) as f:
        f.write(tokens)
    try:
        fe_base = os.environ.get("SEVDO_FRONTEND_URL", "http://sevdo-frontend:8002")
        be_base = os.environ.get("SEVDO_BACKEND_URL", "http://sevdo-backend:8001")
        if is_frontend:
            response = requests.post(
                f"{fe_base}/api/fe-translate/to-s-direct",
                json={
                    "dsl_content": tokens,
                    "component_name": "GeneratedComponent",
                    "include_imports": True,
                },
                timeout=10,
            )
        else:
            token_list = tokens.split()
            response = requests.post(
                f"{be_base}/api/translate/to-s-direct",
                json={"tokens": token_list, "include_imports": True},
                timeout=10,
            )

        if response.status_code == 200:
            return {"success": True, "result": response.json()}
        else:
            return {
                "success": False,
                "error": f"Compiler error: {response.status_code}",
            }

    except requests.exceptions.RequestException as e:
        return {"success": False, "error": f"Connection error: {e}"}
    except Exception as e:
        return {"success": False, "error": f"Compilation error: {e}"}


import re
from typing import Dict, Any, List


def solve_subtask(
    subtask: str,
    rag_service: AgentRAGService,
    model: str = "mistral:instruct",
) -> Dict[str, Any]:
    """
    Coding agent with proper SEVDO syntax editing and aggressive output cleaning
    """

    # Parse task and file content
    parts = subtask.split("\n\nCurrent file content:\n")
    actual_task = parts[0] if len(parts) > 0 else subtask
    current_file = parts[1] if len(parts) > 1 else ""

    rag_context = rag_service.get_relevant_context(actual_task)

    # Determine context
    is_backend = (
        "api" in actual_task.lower()
        or "endpoint" in actual_task.lower()
        or "backend" in actual_task.lower()
    )
    is_frontend = not is_backend

    # Build context from RAG
    context_text = ""
    if rag_context:
        context_text = "\n\nVALID SEVDO PATTERNS FROM KNOWLEDGE BASE:\n"
        for ctx in rag_context[:2]:
            context_text += f"{ctx['content'][:300]}\n"

    system_prompt = (
        "You are a SEVDO code editor. Output ONLY valid SEVDO code, nothing else.\n\n"
        "CRITICAL OUTPUT RULES:\n"
        "1. Output ONLY the complete modified SEVDO file content\n"
        "2. NO explanations, NO comments, NO markdown, NO text\n"
        "3. Start immediately with SEVDO code, end immediately after\n"
        "4. Keep all existing content that isn't being changed\n"
        "5. Only modify what the instruction specifically asks for\n\n"
        "SEVDO SYNTAX:\n"
        "- h(text) = header\n"
        "- t(text) = text/paragraph  \n"
        "- b(text) = button\n"
        "- i(placeholder) = input\n"
        "- mn(...) = menu/navigation\n"
        "- ho(...) = hero section\n"
        "- fl(...) = feature list\n"
        "- Properties: token{prop1=value1,prop2=value2}\n"
        "- Example: h(Title){color=blue,size=large}\n"
        "- Example: ho(h(Header),t(Text),b(Button)){color=green}\n"
        + context_text
        + "\n\nREMEMBER: Output ONLY the complete modified file. No extra text!"
    )

    user_prompt = (
        f"EDITING INSTRUCTION: {actual_task}\n\n"
        f"CURRENT FILE CONTENT:\n{current_file}\n\n"
        f"Output the complete modified file with ONLY the requested changes applied. Start with SEVDO code immediately:"
    )

    base_url = os.environ.get("LLM_GATEWAY_URL", "http://192.168.16.103:8000")

    content = ""
    try:
        resp = requests.post(
            f"{base_url}/ollama",
            json={
                "model_name": model,
                "prompt": user_prompt,
                "system_prompt": system_prompt,
            },
            timeout=60,
        )
        data = resp.json()
        content = (
            (data.get("message", {}) or {}).get("content")
            or data.get("content")
            or data.get("text")
            or ""
        )
    except Exception as e:
        print(f"❌ LLM error: {e}")
        # Return original file on error
        return {
            "subtask": subtask,
            "output": current_file,
            "model": model,
            "compilation": {"success": True},
            "context": {"frontend": is_frontend, "backend": is_backend},
        }

    # AGGRESSIVE OUTPUT CLEANING
    output = content.strip()

    # 1. Remove markdown code blocks
    if "```" in output:
        lines = output.split("\n")
        in_code = False
        code_lines = []
        for line in lines:
            if line.strip().startswith("```"):
                in_code = not in_code
                continue
            if in_code:
                code_lines.append(line)
        if code_lines:
            output = "\n".join(code_lines).strip()

    # 2. Remove common explanation prefixes (case insensitive)
    explanation_prefixes = [
        "here is",
        "output:",
        "result:",
        "the code",
        "here's",
        "modified:",
        "the modified",
        "updated code:",
        "this is",
        "in this example",
        "i've updated",
        "i have",
        "as you can see",
        "the complete",
        "here's the",
        "below is",
        "answer:",
        "response:",
    ]

    output_lower = output.lower()
    for prefix in explanation_prefixes:
        if output_lower.startswith(prefix):
            # Find first valid SEVDO token after the prefix
            for i in range(len(output)):
                char = output[i]
                # Look for pattern: lowercase letter followed by ( or {
                if char.islower() and i + 1 < len(output):
                    next_char = output[i + 1]
                    if next_char == "(" or next_char == "{":
                        output = output[i:].strip()
                        break
            break

    # 3. Remove explanation text at the end
    lines = output.split("\n")
    valid_lines = []

    for line in lines:
        line_stripped = line.strip()

        # Skip empty lines
        if not line_stripped:
            continue

        # Check if line looks like explanation text
        is_explanation = (
            line_stripped[0].isupper()
            and (" " in line_stripped or "." in line_stripped or "," in line_stripped)
            and not any(
                line_stripped.startswith(token + "(")
                or line_stripped.startswith(token + "{")
                for token in [
                    "h",
                    "t",
                    "b",
                    "i",
                    "mn",
                    "ho",
                    "fl",
                    "bl",
                    "tt",
                    "cta",
                    "ns",
                    "apl",
                ]
            )
        )

        if is_explanation:
            print(f"⚠️  Removing explanation line: {line_stripped[:80]}...")
            break

        valid_lines.append(line)

    output = "\n".join(valid_lines).strip()

    # 4. Final validation: must start with valid SEVDO token
    if output and not (output[0].islower() or output[0] == "{"):
        print(f"⚠️  Output doesn't start with valid token, using original file")
        output = current_file

    # 5. Safety check: ensure output isn't empty
    if not output or len(output) < 10:
        print(f"⚠️  Output too short or empty, using original file")
        output = current_file

    # 6. CRITICAL: Check for garbage patterns that break builds
    garbage_patterns = [
        ("_", "underscore in content"),
        ("/token{", "invalid token nesting"),
        ("_ Updated", "explanation marker"),
        ("section _", "explanation text"),
        ("...", "truncation marker"),
        ("/*", "comment block"),
        ("//", "comment line"),
    ]

    for pattern, description in garbage_patterns:
        if pattern in output:
            print(
                f"⚠️  Detected garbage pattern '{pattern}' ({description}), using original file"
            )
            output = current_file
            break

    print(f"📝 Original file ({len(current_file)} chars): {current_file[:100]}...")
    print(f"🎯 Task: {actual_task}")
    print(f"✏️  Modified to ({len(output)} chars): {output[:200]}...")

    # Compile to verify
    compilation = compile_tokens(output, is_frontend)

    if not compilation.get("success"):
        print(f"❌ Compilation failed: {compilation.get('error', 'Unknown')}")
        print(f"🔄 Using original file as fallback")
        output = current_file
        compilation = compile_tokens(output, is_frontend)
    else:
        print(f"✅ Compilation successful")

    return {
        "subtask": subtask,
        "output": output,
        "model": model,
        "compilation": compilation,
        "context": {"frontend": is_frontend, "backend": is_backend},
    }


def get_fallback_for_task(task: str) -> str:
    """Simple fallback SEVDO based on task keywords"""
    task_lower = task.lower()

    if "welcome" in task_lower:
        if "zainab" in task_lower:
            return "h(Welcome to Zainab)"
        return "h(Welcome)"

    if "header" in task_lower or "title" in task_lower:
        return "h(Header Text)"

    if "text" in task_lower or "paragraph" in task_lower:
        return "t(Text content here)"

    if "button" in task_lower:
        return "b(Click Me)"

    if "form" in task_lower:
        return "f(i(Input) b(Submit))"

    # Default
    return "t(Content updated)"


if __name__ == "__main__":
    subtask = "login system"
    rag_service = AgentRAGService()
    model = "gpt-oss:20b"
    solve_subtask(subtask, rag_service, model)
