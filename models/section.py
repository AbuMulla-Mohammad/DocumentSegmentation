from pydantic import BaseModel, Field


class Section(BaseModel):
    title: str = Field(description="Main topic of this section of the document")
    start_index: int = Field(description="Line number where the section begins")
    end_index: int = Field(description="Line number where the section ends")
