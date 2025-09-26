from typing import Dict, Any
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
        fe_base = os.environ.get(
            "SEVDO_FRONTEND_URL", "http://sevdo-frontend:8002"
        )
        be_base = os.environ.get(
            "SEVDO_BACKEND_URL", "http://sevdo-backend:8001"
        )
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


def solve_subtask(
    subtask: str,
    rag_service: AgentRAGService,
    model: str = "gpt-oss:20b",
) -> Dict[str, Any]:
    """
    Minimal coding agent that calls Ollama to produce a concise plan or code for a subtask.

    Returns a dict containing the subtask, the generated answer, and basic metadata.
    """

    rag_context = rag_service.get_relevant_context(subtask)

    # Determine context for token filtering with broader keywords
    is_backend = any(
        keyword in subtask.lower()
        for keyword in [
            "api",
            "endpoint",
            "backend",
            "server",
            "database",
            "auth",
            "login system",
            "registration system",
            "credentials",
            "validate",
            "validation",
            "session",
            "token",
            "logout",
            "register",
        ]
    )
    is_frontend = any(
        keyword in subtask.lower()
        for keyword in [
            "html",
            "page",
            "form",
            "ui",
            "frontend",
            "website",
            "structure",
            "layout",
            "button",
            "input",
            "field",
            "username",
            "password",
            "text",
            "header",
            "navigation",
            "user",
            "display",
            "show",
            "render",
            "pattern",
        ]
    )

    # Default to frontend if unclear (most SEVDO use cases are UI)
    if not is_backend and not is_frontend:
        is_frontend = True

    rag_context_text = ""
    if rag_context:
        rag_context_text = "\n\nThis is the relevant context from the knowledge base and are the only valid tokens:\n"
        for ctx in rag_context[:1]:  # Use top 2 most relevant
            rag_context_text += (
                f"- {ctx['title']}: {ctx['content'][:200]}...\n"
            )

    system_prompt = (
        "You are a focused coding agent. Given a subtask, and context, use the language SEVDO "
        "to complete it. You may only follow the context explaining the language SEVDO which "
        "uses letters and groups of letters to represent a code language. "
        "Follow the subtask completely and you can only use the letters given to you as context. "
        "CRITICAL: Output ONLY space-separated tokens. NO explanations whatsoever. Write out the full SEVDO file content as to overwrite file content.\n\n"
        "Do not put any newlines in your output. Only space-separated tokens.\n\n"
        "Examples:\n"
        "User: 'login system'\n"
        "Assistant: l r m\n\n"
        "User: 'login form with inputs'\n"
        "Assistant: lf i i b\n\n"
        "User: 'contact page with form'\n"
        "Assistant: h t cf i b\n\n"
        "User: 'navigation with images'\n"
        "Assistant: n img img h\n" + rag_context_text
    )

    # Use FastAPI LLM gateway endpoint (configurable) with JSON body
    base_url = os.environ.get("LLM_GATEWAY_URL", "http://192.168.16.103:8000")
    url_simple = f"{base_url}/ollama"

    content = ""
    try:
        payload = {
            "model_name": model,
            "prompt": subtask,
            "system_prompt": system_prompt,
        }
        http_resp = requests.post(url_simple, json=payload, timeout=60)
        try:
            data = http_resp.json()
            content = (
                (data.get("message", {}) or {}).get("content")
                or data.get("content")
                or data.get("text")
                or data.get("response")
                or http_resp.text
            )
        except Exception:
            content = http_resp.text
    except Exception:
        content = ""

    print("""THE CODING AGENT OUTPUT: """, content)

    # Attempt to compile tokens to actual code
    compilation_result = compile_tokens(content.strip(), is_frontend)

    return {
        "subtask": subtask,
        "output": content.strip(),
        "model": model,
        "compilation": compilation_result,
        "context": {"frontend": is_frontend, "backend": is_backend},
    }


if __name__ == "__main__":
    subtask = "login system"
    rag_service = AgentRAGService()
    model = "gpt-oss:20b"
    solve_subtask(subtask, rag_service, model)
