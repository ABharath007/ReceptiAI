from pydantic import BaseModel


class KnowledgeBaseCreate(BaseModel):
    business_id: int
    category: str
    title: str
    content: str


class KnowledgeBaseUpdate(BaseModel):
    business_id: int
    category: str
    title: str
    content: str


class KnowledgeBaseResponse(BaseModel):
    id: int
    business_id: int
    category: str
    title: str
    content: str

    class Config:
        from_attributes = True