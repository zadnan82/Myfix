# user_backend/app/models/template_models.py

from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List
from datetime import datetime


class TemplateCustomizations(BaseModel):
    """Template customization options"""

    company_name: Optional[str] = Field(
        None, description="Company or brand name", max_length=100
    )
    primary_color: Optional[str] = Field(
        "#3b82f6", description="Primary color in hex format", regex=r"^#[0-9A-Fa-f]{6}$"
    )
    description: Optional[str] = Field(
        None, description="Website description", max_length=500
    )
    contact_email: Optional[str] = Field(None, description="Contact email address")
    phone: Optional[str] = Field(None, description="Phone number", max_length=20)
    address: Optional[str] = Field(None, description="Physical address", max_length=200)
    social_media: Optional[Dict[str, str]] = Field(
        None, description="Social media links"
    )
    logo_url: Optional[str] = Field(None, description="Logo image URL")

    class Config:
        extra = "allow"  # Allow additional customization fields
        schema_extra = {
            "example": {
                "company_name": "Bella Vista Restaurant",
                "primary_color": "#e97434",
                "description": "Authentic Italian cuisine in the heart of the city",
                "contact_email": "info@bellavista.com",
                "phone": "(555) 123-4567",
                "address": "123 Main St, City, State 12345",
            }
        }


class TemplateGenerateRequest(BaseModel):
    """Request model for generating a custom template"""

    project_name: str = Field(
        ..., min_length=1, max_length=100, description="Project name"
    )
    customizations: TemplateCustomizations = Field(
        default_factory=TemplateCustomizations, description="Template customizations"
    )
    include_docker: bool = Field(True, description="Include Docker configuration")
    include_readme: bool = Field(True, description="Include README documentation")
    include_env_example: bool = Field(True, description="Include .env.example file")

    class Config:
        schema_extra = {
            "example": {
                "project_name": "My Restaurant Website",
                "customizations": {
                    "company_name": "Bella Vista Restaurant",
                    "primary_color": "#e97434",
                    "description": "Authentic Italian cuisine in the heart of the city",
                    "contact_email": "info@bellavista.com",
                    "phone": "(555) 123-4567",
                },
                "include_docker": True,
                "include_readme": True,
                "include_env_example": True,
            }
        }


class TemplatePreviewData(BaseModel):
    """Template preview data structure"""

    has_frontend: bool = Field(False, description="Template has frontend components")
    has_backend: bool = Field(False, description="Template has backend components")
    preview_html: Optional[str] = Field(None, description="URL to preview HTML")
    demo_url: Optional[str] = Field(None, description="URL to live demo")
    download_size: int = Field(0, description="Download size in bytes")
    file_count: int = Field(0, description="Total number of files")
    frontend_files: List[str] = Field(
        default_factory=list, description="Frontend file names"
    )
    backend_files: List[str] = Field(
        default_factory=list, description="Backend file names"
    )


class TemplateGenerationResult(BaseModel):
    """Result of template generation"""

    success: bool = Field(..., description="Generation success status")
    project_id: Optional[int] = Field(None, description="Created project ID")
    project_name: str = Field(..., description="Project name")
    template_used: str = Field(..., description="Template that was used")
    generated_files: Dict[str, str] = Field(
        default_factory=dict, description="Generated file contents"
    )
    files_count: int = Field(0, description="Number of files generated")
    customizations_applied: TemplateCustomizations = Field(
        default_factory=TemplateCustomizations, description="Applied customizations"
    )
    generation_log: Optional[str] = Field(None, description="Generation process log")
    download_ready: bool = Field(False, description="Ready for download")
    estimated_deploy_time: Optional[str] = Field(
        "5-10 minutes", description="Estimated deployment time"
    )


class TemplateStatusInfo(BaseModel):
    """Template generation status information"""

    available_templates: List[str] = Field(
        default_factory=list, description="Available template names"
    )
    generated_count: int = Field(
        0, description="Number of successfully generated templates"
    )
    total_templates: int = Field(0, description="Total number of templates")
    generation_status: Dict[str, Any] = Field(
        default_factory=dict, description="Individual template status"
    )
    last_updated: str = Field(..., description="Last update timestamp")


class TemplateLogEntry(BaseModel):
    """Template generation log entry"""

    timestamp: str = Field(..., description="Log entry timestamp")
    template: str = Field(..., description="Template name")
    status: str = Field(..., description="Generation status")
    message: str = Field(..., description="Log message")
    details: Dict[str, Any] = Field(
        default_factory=dict, description="Additional details"
    )
    error: Optional[str] = Field(None, description="Error message if failed")


class TemplateLogsResponse(BaseModel):
    """Template generation logs response"""

    logs: List[TemplateLogEntry] = Field(
        default_factory=list, description="Log entries"
    )
    total: int = Field(0, description="Total number of log entries")
    generated_at: str = Field(..., description="Response generation time")
    error: Optional[str] = Field(None, description="Error message if any")


class EnhancedTemplateOutSchema(BaseModel):
    """Enhanced template output schema with generation data"""

    id: str = Field(..., description="Template ID")
    name: str = Field(..., description="Template name")
    description: str = Field(..., description="Template description")
    version: str = Field("1.0.0", description="Template version")
    category: str = Field("general", description="Template category")
    author: str = Field("SEVDO Team", description="Template author")
    tags: List[str] = Field(default_factory=list, description="Template tags")
    is_featured: bool = Field(False, description="Is featured template")
    is_public: bool = Field(True, description="Is publicly available")
    usage_count: int = Field(0, description="Number of times used")
    rating: float = Field(5.0, description="Template rating")

    # Template structure and configuration
    structure: Optional[Dict[str, Any]] = Field(None, description="Template structure")
    required_prefabs: List[str] = Field(
        default_factory=list, description="Required SEVDO prefabs"
    )
    customization: Dict[str, Any] = Field(
        default_factory=dict, description="Customization options"
    )
    features: List[str] = Field(default_factory=list, description="Template features")
    installation: Optional[Dict[str, str]] = Field(
        None, description="Installation instructions"
    )

    # Generation-specific data
    preview_data: Optional[TemplatePreviewData] = Field(
        None, description="Preview and generation data"
    )
    generated_at: Optional[str] = Field(None, description="Generation timestamp")
    is_generated: bool = Field(False, description="Has been generated by integrator")

    # Timestamps
    created_at: str = Field(..., description="Creation timestamp")
    updated_at: str = Field(..., description="Last update timestamp")


class TemplateDownloadResponse(BaseModel):
    """Template download response"""

    success: bool = Field(True, description="Download success status")
    message: str = Field("Download started", description="Download status message")
    filename: str = Field(..., description="Download filename")
    size: int = Field(0, description="File size in bytes")


class TemplateActionResponse(BaseModel):
    """Generic template action response"""

    success: bool = Field(..., description="Action success status")
    message: str = Field(..., description="Action result message")
    template: Optional[str] = Field(None, description="Template name if applicable")


class BackgroundTaskResponse(BaseModel):
    """Background task response"""

    message: str = Field(..., description="Task status message")
    status: str = Field("processing", description="Task status")
    task_id: Optional[str] = Field(None, description="Task identifier")


class TemplateUseSchema(BaseModel):
    """Schema for using a template to create a project"""

    project_name: str = Field(
        ..., min_length=1, max_length=100, description="Project name"
    )
    project_description: Optional[str] = Field(
        None, max_length=500, description="Project description"
    )
    customize_config: Optional[Dict[str, Any]] = Field(
        None, description="Customization configuration"
    )
