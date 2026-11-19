from typing import Literal
from pydantic import BaseModel, Field

class Source(BaseModel):
    id: str
    title: str
    url: str
    verified: bool = False  # URL was returned by a search citation, not independently fact-checked

class Claim(BaseModel):
    text: str
    source_ids: list[str] = Field(default_factory=list)

class Scene(BaseModel):
    scene_id: int
    start_sec: int
    duration_sec: int
    narration: str
    visual_type: Literal['ai_video', 'motion_graphics']
    visual_prompt: str
    on_screen_text: str
    source_ids: list[str] = Field(default_factory=list)

class Plan(BaseModel):
    topic: str
    title: str
    target_duration_sec: int = 150
    aspect_ratio: Literal['16:9'] = '16:9'
    language: str = 'ko'
    claims: list[Claim]
    scenes: list[Scene]
    notes: list[str] = Field(default_factory=list)
    publication_status: Literal['review_required'] = 'review_required'
