"""
Schemas package: Pydantic models and related types.
"""

import enum
from typing import Annotated

from pydantic import BaseModel, EmailStr, StringConstraints, field_validator
