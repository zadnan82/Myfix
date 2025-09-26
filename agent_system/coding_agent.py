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
    model: str = "mistral:instruct",  # FIXED: Use working model
) -> Dict[str, Any]:
    """
    Coding agent with proper SEVDO syntax examples
    """

    rag_context = rag_service.get_relevant_context(subtask)

    # Determine context
    is_backend = (
        "api" in subtask.lower()
        or "endpoint" in subtask.lower()
        or "backend" in subtask.lower()
    )
    is_frontend = not is_backend

    # Build context from RAG
    context_text = ""
    if rag_context:
        context_text = "\n\nVALID SEVDO TOKENS:\n"
        for ctx in rag_context[:2]:
            context_text += f"{ctx['content'][:400]}\n"

    system_prompt = (
        "You are a SEVDO code generator. Output ONLY valid SEVDO syntax.\n\n"
        "SEVDO SYNTAX RULES:\n"
        "- token(arg) for single argument: h(Welcome)\n"
        "- token(arg1,arg2) for multiple: i(username,email)\n"
        "- token{prop=value} for properties: b{color=green}\n"
        "- Combine: token(arg){prop=value}\n"
        "- Containers can nest: ho(h(Title),t(Text),b(Action))\n\n"
        "CORRECT EXAMPLES:\n"
        "Task: 'add welcome header' → h(Welcome to Site)\n"
        "Task: 'create hero section' → ho(h(Welcome),t(Description),b(Get Started))\n"
        "Task: 'login form' → lf i(Username) i(Password) b(Login)\n"
        "Task: 'change color to green' → ho(h(Title),t(Text)){color=green}\n\n"
        "WRONG (DO NOT DO THIS):\n"
        "- h('primary-color') = 'green' ❌\n"
        "- l r m ❌\n"
        "- primary-color: green ❌\n\n"
        + context_text
        + "\n\nOutput ONLY valid SEVDO code following the syntax above. No explanations."
    )

    base_url = os.environ.get("LLM_GATEWAY_URL", "http://192.168.16.103:8000")

    content = ""
    try:
        resp = requests.post(
            f"{base_url}/ollama",
            json={
                "model_name": model,
                "prompt": f"Task: {subtask}\n\nOutput valid SEVDO code:",
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
        print(f"LLM error: {e}")
        content = "h(Welcome)"

    # Clean output
    output = content.strip()

    # Remove explanation prefixes
    for prefix in ["here is", "output:", "result:", "the code", "here's"]:
        if output.lower().startswith(prefix):
            for i, char in enumerate(output):
                if char.isalpha() and (i == 0 or output[i - 1].isspace()):
                    output = output[i:]
                    break

    # Remove markdown
    if output.startswith("```"):
        lines = output.split("\n")
        output = "\n".join(lines[1:-1]) if len(lines) > 2 else output

    output = output.strip()

    print(f"📝 LLM OUTPUT: {content[:200]}...")
    print(f"✂️  CLEANED: {output[:200]}...")

    # Compile
    compilation = compile_tokens(output, is_frontend)

    if compilation.get("success"):
        print(f"✅ Compilation successful")
    else:
        print(f"❌ Compilation failed: {compilation.get('error', 'Unknown')}")
        fallback = get_fallback_for_task(subtask)
        print(f"🔄 Trying fallback: {fallback}")
        compilation = compile_tokens(fallback, is_frontend)
        if compilation.get("success"):
            output = fallback
            print(f"✅ Fallback worked!")

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
