import uuid
from typing import Optional


def generate_unique_id(prefix: Optional[str]) -> str:
    """Generate a unique identifier using UUID4."""
    base_uuid = str(uuid.uuid4())
    return f"{prefix}:{base_uuid}" if prefix else base_uuid
