from pydantic import BaseModel, Field
from typing import List
from models.section import Section
class StructuredDocument(BaseModel):
    """Obtains meaningful sections, each centered around a single concept/topic."""
    sections: List[Section] = Field(description="A list of sections of the document")
