import asyncio
from datetime import datetime, timezone
import os
from typing import Any, Dict, List
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from fastapi import Query  # noqa: F401 (reserved for future query param utilities)

import subprocess
from pathlib import Path
from sqlalchemy.orm import Session
from sqlalchemy import select

from user_backend.app.models import (
    AIConversation,
    ProjectType,
    User,
    Project,
)
from user_backend.app.schemas import (
    AIChatMessageSchema,
    AIChatResponseSchema,
    AIProjectFromDescriptionResultSchema,
    AIProjectFromDescriptionSchema,
    ProjectFeatureSchema,
    ChangeProjectRequest,
)
from user_backend.app.core.security import get_current_active_user
from user_backend.app.db_setup import get_db
from user_backend.app.core.logging_config import StructuredLogger
from agent_system.sprintmaster import execute_task

router = APIRouter()
logger = StructuredLogger(__name__)

# Feature mapping: tokens to user-friendly features
FEATURE_MAPPING = {
    # Authentication features
    "r": ProjectFeatureSchema(
        name="User Registration",
        description="Allow users to create accounts with email and password",
        category="User Management",
        complexity="Basic",
        icon="👤",
    ),
    "l": ProjectFeatureSchema(
        name="User Login",
        description="Secure user authentication and session management",
        category="User Management",
        complexity="Basic",
        icon="🔐",
    ),
    "m": ProjectFeatureSchema(
        name="User Profiles",
        description="User profile management and account information",
        category="User Management",
        complexity="Basic",
        icon="👤",
    ),
    "o": ProjectFeatureSchema(
        name="User Logout",
        description="Secure user logout and session cleanup",
        category="User Management",
        complexity="Basic",
        icon="🚪",
    ),
    "u": ProjectFeatureSchema(
        name="Profile Updates",
        description="Allow users to update their profile information",
        category="User Management",
        complexity="Intermediate",
        icon="✏️",
    ),
    # Session management
    "t": ProjectFeatureSchema(
        name="Session Management",
        description="Advanced session handling and token refresh",
        category="Security",
        complexity="Advanced",
        icon="🔄",
    ),
    "a": ProjectFeatureSchema(
        name="Multi-Device Logout",
        description="Logout from all devices and sessions",
        category="Security",
        complexity="Advanced",
        icon="📱",
    ),
    "s": ProjectFeatureSchema(
        name="Session Monitoring",
        description="View and manage active user sessions",
        category="Security",
        complexity="Advanced",
        icon="📊",
    ),
    # Website features
    "c": ProjectFeatureSchema(
        name="Contact Form",
        description="Contact form with email notifications",
        category="Communication",
        complexity="Basic",
        icon="📧",
    ),
    "b": ProjectFeatureSchema(
        name="Blog System",
        description="Content management system for blog posts and news",
        category="Content",
        complexity="Intermediate",
        icon="📝",
    ),
    "e": ProjectFeatureSchema(
        name="E-commerce",
        description="Online store with shopping cart and payments",
        category="E-commerce",
        complexity="Advanced",
        icon="🛒",
    ),
    "f": ProjectFeatureSchema(
        name="File Upload",
        description="File upload and management system",
        category="File Management",
        complexity="Intermediate",
        icon="📁",
    ),
}

# AI suggestion logic: description keywords to tokens
DESCRIPTION_TO_TOKENS = {
    # E-commerce keywords
    "shop": ["r", "l", "m", "e", "c"],
    "store": ["r", "l", "m", "e", "c"],
    "ecommerce": ["r", "l", "m", "e", "c"],
    "e-commerce": ["r", "l", "m", "e", "c"],
    "buy": ["r", "l", "m", "e"],
    "sell": ["r", "l", "m", "e"],
    "cart": ["r", "l", "e"],
    "payment": ["r", "l", "e"],
    # Restaurant keywords
    "restaurant": ["c", "b", "f"],
    "menu": ["b", "c"],
    "food": ["c", "b"],
    "order": ["r", "l", "e", "c"],
    # Blog/Content keywords
    "blog": ["b", "c"],
    "news": ["b", "c"],
    "article": ["b"],
    "content": ["b"],
    "post": ["b"],
    # Business keywords
    "business": ["c", "b", "f"],
    "company": ["c", "b", "f"],
    "corporate": ["c", "b", "f"],
    # Portfolio keywords
    "portfolio": ["c", "f", "b"],
    "gallery": ["f", "b"],
    "showcase": ["f", "b"],
    # User account keywords
    "login": ["r", "l", "m", "o"],
    "register": ["r", "l", "m"],
    "account": ["r", "l", "m", "u"],
    "user": ["r", "l", "m"],
    "profile": ["r", "l", "m", "u"],
    # Contact keywords
    "contact": ["c"],
    "email": ["c"],
    "form": ["c"],
}


def suggest_tokens_from_description(
    description: str, project_type: ProjectType = None
) -> List[str]:
    """AI-powered token suggestion based on description"""
    description_lower = description.lower()
    suggested_tokens = set()

    # Analyze keywords in description
    for keyword, tokens in DESCRIPTION_TO_TOKENS.items():
        if keyword in description_lower:
            suggested_tokens.update(tokens)

    # Add default tokens based on project type
    if project_type == ProjectType.WEB_APP:
        suggested_tokens.update(["c"])  # Most websites need contact
    elif project_type == ProjectType.API_BACKEND:
        suggested_tokens.update(["r", "l", "m"])  # APIs usually need auth

    # Convert to list and ensure logical dependencies
    tokens = list(suggested_tokens)

    # Add dependencies
    if "e" in tokens and "r" not in tokens:  # E-commerce needs user accounts
        tokens.extend(["r", "l", "m"])
    if "u" in tokens and "l" not in tokens:  # Profile updates need login
        tokens.extend(["r", "l", "m"])

    return list(set(tokens))  # Remove duplicates


def tokens_to_features(tokens: List[str]) -> List[ProjectFeatureSchema]:
    """Convert internal tokens to user-friendly features"""
    features = []
    for token in tokens:
        if token in FEATURE_MAPPING:
            features.append(FEATURE_MAPPING[token])
    return features


def validate_token_combination(tokens: List[str]) -> dict:
    """Validate that tokens work together"""
    errors = []
    warnings = []
    suggestions = []

    # Check for required dependencies
    if "e" in tokens and "r" not in tokens:
        suggestions.append("E-commerce usually requires user accounts")
    if "u" in tokens and ("r" not in tokens or "l" not in tokens):
        errors.append("Profile updates require user registration and login")

    # Check for conflicts (none currently defined)

    return {
        "is_valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "suggestions": suggestions,
    }


@router.post(
    "/project-from-description",
    response_model=AIProjectFromDescriptionResultSchema,
)
async def create_project_from_description(
    ai_request: AIProjectFromDescriptionSchema,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Convert natural language description to project features (not tokens)"""
    try:
        logger.info(
            f"AI project generation request from user {current_user.id}",
            description=ai_request.description,
            project_type=ai_request.project_type,
        )

        # Use AI to suggest tokens based on description
        suggested_tokens = suggest_tokens_from_description(
            ai_request.description, ai_request.project_type
        )

        # Validate token combination
        validation = validate_token_combination(suggested_tokens)

        if not validation["is_valid"]:
            # Fix issues automatically where possible
            if "e" in suggested_tokens and "r" not in suggested_tokens:
                suggested_tokens.extend(["r", "l", "m"])
                validation = validate_token_combination(suggested_tokens)

        # Convert tokens to user-friendly features
        suggested_features = tokens_to_features(suggested_tokens)

        # Generate project name from description
        words = ai_request.description.split()[:3]
        suggested_name = " ".join(word.capitalize() for word in words)
        if len(suggested_name) < 5:
            suggested_name += " Website"

        # Calculate confidence based on keyword matches
        confidence = min(0.95, 0.4 + (len(suggested_tokens) * 0.1))

        # Create reasoning
        feature_names = [f.name for f in suggested_features]
        reasoning = f"Based on your description, I suggest these features: {', '.join(feature_names)}"

        # Store tokens in project internally (create the project)
        new_project = Project(
            name=suggested_name,
            description=ai_request.description,
            project_type=ai_request.project_type or ProjectType.WEB_APP,
            tokens=suggested_tokens,  # Store tokens internally
            user_id=current_user.id,
        )

        db.add(new_project)
        db.commit()
        db.refresh(new_project)

        logger.info(
            "AI project created successfully",
            project_id=new_project.id,
            suggested_tokens=suggested_tokens,
            confidence=confidence,
        )

        return AIProjectFromDescriptionResultSchema(
            suggested_name=suggested_name,
            suggested_description=ai_request.description,
            suggested_features=suggested_features,  # Return features, not tokens
            confidence=confidence,
            reasoning=reasoning,
            project_type=ai_request.project_type or ProjectType.WEB_APP,
        )

    except Exception as e:
        logger.error(f"AI project generation failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process project description",
        )


@router.post("/chat", response_model=AIChatResponseSchema)
async def ai_chat(
    chat_request: AIChatMessageSchema,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Enhanced AI chat with better responses"""
    try:
        # Find or create conversation
        conversation_id = chat_request.conversation_id
        if not conversation_id:
            conversation = AIConversation(
                user_id=current_user.id, project_id=chat_request.project_id
            )
            db.add(conversation)
            db.commit()
            db.refresh(conversation)
            conversation_id = conversation.id
        else:
            conversation = db.execute(
                select(AIConversation).where(AIConversation.id == conversation_id)
            ).scalar_one_or_none()

            if not conversation:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Conversation not found",
                )

        # Add user message to conversation
        conversation.messages.append(
            {
                "role": "user",
                "content": chat_request.message,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        )

        # Analyze message for feature suggestions
        suggested_tokens = suggest_tokens_from_description(chat_request.message)
        suggested_features = tokens_to_features(suggested_tokens)

        # Generate contextual AI response
        if suggested_tokens:
            feature_names = [f.name for f in suggested_features]
            response_content = f"Great idea! For '{chat_request.message}', I recommend adding: {', '.join(feature_names)}. "
            response_content += "These features will work well together and provide a complete solution."
        else:
            response_content = (
                f"I understand you want to {chat_request.message.lower()}. "
            )
            response_content += "Can you provide more details about the specific functionality you need?"

        # Add AI response to conversation
        conversation.messages.append(
            {
                "role": "assistant",
                "content": response_content,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "suggested_features": [f.dict() for f in suggested_features],
            }
        )

        db.commit()

        # Generate follow-up suggestions
        suggestions = [
            "What specific features do you need?",
            "Should users be able to create accounts?",
            "Do you need a contact form?",
            "Will you need file uploads?",
        ]

        return AIChatResponseSchema(
            response=response_content,
            suggestions=suggestions,
            suggested_tokens=suggested_tokens,  # Keep for backward compatibility
            conversation_id=conversation_id,
        )

    except Exception as e:
        logger.error(f"AI chat failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="AI chat processing failed",
        )


@router.post("/analyze-website-description")
async def analyze_website_description(
    request: Dict[str, Any],
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Analyze user description and detect website components"""
    try:
        description = request.get("description", "")
        # analysis_type reserved for future use
        _ = request.get("analysis_type", "website_components")

        # Your AI analysis logic here
        # This could integrate with OpenAI, Claude, or your own ML model

        # For now, return structured analysis
        detected_elements = analyze_description_advanced(description)

        return {
            "success": True,
            "detected_elements": detected_elements,
            "confidence": 0.85,
            "suggestions": [
                "Consider adding more details about your target audience",
                "Specify the main goal of your website",
            ],
        }

    except Exception as e:
        logger.error(f"Website description analysis failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Analysis failed",
        )


def analyze_description_advanced(description: str) -> dict:
    """Advanced description analysis with business intelligence"""
    # Implement your AI logic here
    # This is where you'd integrate with your preferred AI service

    return {
        "navigation": True,
        "hero": True,
        "services": "service" in description.lower(),
        "contact": "contact" in description.lower(),
        "businessType": detect_business_type(description),
    }


def detect_business_type(description: str) -> str:
    """Detect the type of business from description"""
    desc_lower = description.lower()

    business_keywords = {
        "restaurant": ["restaurant", "food", "menu", "dining"],
        "medical": ["doctor", "medical", "health", "clinic"],
        "ecommerce": ["shop", "store", "products", "buy"],
        "portfolio": ["portfolio", "work", "showcase", "gallery"],
        # Add more business types as needed
    }

    for business_type, keywords in business_keywords.items():
        if any(keyword in desc_lower for keyword in keywords):
            return business_type

    return "general"


# user_backend/app/api/v1/ai.py - FIXED rebuild logic
@router.post("/change-project-from-description")
async def change_project_from_description(
    request: ChangeProjectRequest,
):
    """Apply changes and trigger rebuild"""
    try:
        logger.info(
            "🎯 AI edit request",
            description=request.description[:120],
            project_name=request.project_name,
        )

        # Execute the task using agent system
        response = execute_task(request.description, request.project_name)

        # Count successful changes
        amount = len(response["results"])
        amount_success = sum(
            1
            for result in response["results"]
            if result.get("compilation", {}).get("success")
        )

        logger.info(f"📊 Changes: {amount_success}/{amount} successful")

        if amount_success > 0:
            # Changes were made - now trigger rebuild
            logger.info("🔨 Triggering frontend rebuild...")

            # Get the actual project path
            projects_root = Path(os.getenv("PROJECTS_ROOT", "/app/generated_websites"))
            project_path = None

            # Find the project directory
            for dir_path in projects_root.iterdir():
                if request.project_name in dir_path.name:
                    project_path = dir_path
                    break

            if project_path:
                frontend_dir = project_path / "frontend"

                # Compile the .s files to JSX
                from sevdo_frontend.frontend_compiler import dsl_to_jsx

                s_dir = frontend_dir / ".s"
                if s_dir.exists():
                    for s_file in s_dir.glob("*.s"):
                        try:
                            dsl_content = s_file.read_text(encoding="utf-8")
                            component_name = s_file.stem.capitalize()

                            jsx_code = dsl_to_jsx(
                                dsl_content,
                                include_imports=True,
                                component_name=component_name,
                            )

                            # Write to components directory
                            jsx_file = (
                                frontend_dir
                                / "src"
                                / "components"
                                / f"{component_name}.jsx"
                            )
                            jsx_file.write_text(jsx_code, encoding="utf-8")

                            logger.info(
                                f"   ✅ Compiled {s_file.name} → {component_name}.jsx"
                            )

                        except Exception as e:
                            logger.error(f"   ❌ Failed to compile {s_file.name}: {e}")

                # Trigger hot reload by touching a file
                try:
                    import httpx

                    # Call preview manager to trigger reload
                    async with httpx.AsyncClient() as client:
                        await client.post(
                            "http://preview-manager:8080/reload",
                            json={"project_id": request.project_name},
                        )

                    logger.info("🔄 Hot reload triggered")

                except Exception as e:
                    logger.warning(f"Could not trigger hot reload: {e}")

            return {
                **response,
                "message": f"Applied {amount_success} changes successfully",
                "rebuild_triggered": True,
            }

        return {
            **response,
            "message": "No changes were applied",
            "rebuild_triggered": False,
        }

    except Exception as e:
        logger.error(f"AI edit failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to apply changes: {str(e)}",
        )


def simple_rebuild(project_name: str, frontend_path: str):
    import subprocess

    try:
        print(f"{'=' * 80}")
        print(f"REBUILD: {project_name}")
        print(f"{'=' * 80}")

        result = subprocess.run(
            ["npm", "run", "build"],
            cwd=frontend_path,
            capture_output=True,
            text=True,
            timeout=300,
        )

        print(f"Return code: {result.returncode}")
        print(f"STDOUT: {result.stdout}")

        if result.returncode == 0:
            print(f"✅ Rebuild successful")
        else:
            print(f"❌ Rebuild failed: {result.stderr}")

    except Exception as e:
        print(f"❌ Error: {e}")


async def send_websocket_notification(
    generation_id: str, message: str, status: str, progress: int, changes: list = None
):
    """
    Send WebSocket notification to connected clients
    """
    try:
        from user_backend.app.api.v1.websockets import manager

        notification_data = {
            "type": "preview_update",
            "data": {
                "generation_id": generation_id,
                "message": message,
                "status": status,
                "progress": progress,
                "changes": changes or [],
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
        }

        await manager.broadcast(notification_data)
        logger.info(f"WebSocket notification sent: {message}")

    except Exception as e:
        logger.error(f"Failed to send WebSocket notification: {str(e)}")


# Add this test endpoint to your ai.py to debug the issue


@router.post("/test-edit")
async def test_ai_edit(request: ChangeProjectRequest):
    """
    Test endpoint to diagnose AI edit issues
    """
    try:
        logger.info(
            f"Test edit called: {request.description}, project: {request.project_name}"
        )

        # Check if project exists
        project_path = Path(f"generated_websites/{request.project_name}")

        response = {
            "status": "test",
            "project_name": request.project_name,
            "description": request.description,
            "project_exists": project_path.exists(),
            "project_path": str(project_path),
        }

        if project_path.exists():
            # List .s files
            frontend_s_dir = project_path / "frontend" / ".s"
            if frontend_s_dir.exists():
                s_files = list(frontend_s_dir.glob("*.s"))
                response["s_files"] = [f.name for f in s_files]
            else:
                response["s_files"] = []
                response["error"] = "No .s directory found"

        logger.info(f"Test response: {response}")
        return response

    except Exception as e:
        logger.error(f"Test failed: {str(e)}")
        return {"status": "error", "error": str(e)}


@router.post("/simple-edit")
async def simple_ai_edit(
    request: ChangeProjectRequest, background_tasks: BackgroundTasks
):
    """
    Simplified AI edit without the complex retry logic
    """
    try:
        logger.info(f"Simple edit: {request.description} for {request.project_name}")

        # Validate project
        project_path = Path(f"generated_websites/{request.project_name}")
        if not project_path.exists():
            raise HTTPException(
                status_code=404, detail=f"Project not found: {request.project_name}"
            )

        # Try ONE execution
        try:
            response = execute_task(
                task=request.description, project_name=request.project_name
            )
        except Exception as task_error:
            logger.error(f"Task execution error: {task_error}")
            raise HTTPException(
                status_code=500, detail=f"Task execution failed: {str(task_error)}"
            )

        # Count successes
        if not response or "results" not in response:
            raise HTTPException(
                status_code=500, detail="Invalid response from task execution"
            )

        success_count = 0
        for result in response.get("results", []):
            if result.get("compilation", {}).get("success"):
                success_count += 1

        # Schedule rebuild if we have successes
        if success_count > 0:
            frontend_path = project_path / "frontend"
            if frontend_path.exists():
                background_tasks.add_task(
                    simple_rebuild,
                    project_name=request.project_name,
                    frontend_path=str(frontend_path),
                )
                response["rebuild_scheduled"] = True

        response["success_count"] = success_count
        response["total_count"] = len(response.get("results", []))

        return response

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Simple edit failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Add this to your ai.py for direct testing


@router.post("/direct-edit")
async def direct_edit(request: Dict[str, Any], background_tasks: BackgroundTasks):
    """
    Direct edit that bypasses AI - just replace text directly
    Useful for testing the rebuild flow
    """
    try:
        project_name = request.get("project_name")
        file_path = request.get("file_path", "frontend/.s/Home.s")
        old_text = request.get("old_text", "")
        new_text = request.get("new_text", "")

        if not all([project_name, old_text, new_text]):
            raise HTTPException(400, "Missing required fields")

        # Find the file
        project_path = Path(f"generated_websites/{project_name}")
        full_path = project_path / file_path

        if not full_path.exists():
            raise HTTPException(404, f"File not found: {full_path}")

        # Read current content
        content = full_path.read_text()

        # Replace text
        if old_text not in content:
            raise HTTPException(400, f"Text '{old_text}' not found in file")

        new_content = content.replace(old_text, new_text)

        # Write back
        full_path.write_text(new_content)

        logger.info(
            f"Direct edit: replaced '{old_text}' with '{new_text}' in {file_path}"
        )

        # Recompile the .s file to React
        try:
            import requests as req

            compile_response = req.post(
                "http://sevdo-frontend:8002/api/fe-translate/to-s-direct",
                json={
                    "dsl_content": new_content,
                    "component_name": full_path.stem.capitalize(),
                    "include_imports": True,
                },
                timeout=10,
            )

            if compile_response.status_code == 200:
                react_code = compile_response.json()["code"]

                # Write React component
                react_path = (
                    project_path
                    / "frontend"
                    / "src"
                    / "components"
                    / f"{full_path.stem.capitalize()}.jsx"
                )
                react_path.write_text(react_code)

                logger.info(f"✅ Recompiled {full_path.stem}.jsx")

                # Schedule rebuild
                frontend_path = project_path / "frontend"
                background_tasks.add_task(
                    simple_rebuild,
                    project_name=project_name,
                    frontend_path=str(frontend_path),
                )

                return {
                    "success": True,
                    "message": "Edit applied successfully",
                    "old_text": old_text,
                    "new_text": new_text,
                    "file_path": str(full_path),
                    "rebuild_scheduled": True,
                }
            else:
                raise Exception(f"Compilation failed: {compile_response.text}")

        except Exception as e:
            logger.error(f"Compilation/rebuild failed: {e}")
            return {
                "success": True,
                "message": "Edit applied but compilation failed",
                "error": str(e),
                "old_text": old_text,
                "new_text": new_text,
            }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Direct edit failed: {e}")
        raise HTTPException(500, str(e))
