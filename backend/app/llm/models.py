from pydantic import BaseModel, Field
from typing import List
from enum import Enum

class Category(str, Enum):
    HOMEPAGE = "HOMEPAGE"
    COLLECTION = "COLLECTION"
    PRODUCT = "PRODUCT"
    CART = "CART"
    NAVIGATION = "NAVIGATION"
    TRUST = "TRUST"
    GLOBAL = "GLOBAL"

class Impact(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

class Confidence(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

class Effort(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

class Opportunity(BaseModel):
    title: str = Field(..., description="Short, descriptive title of the opportunity")
    category: Category = Field(..., description="Category of the opportunity")
    problem: str = Field(..., description="Description of the friction or missing best practice")
    evidence: str = Field(..., description="Explicit reference to the provided FeatureSet evidence")
    recommendation: str = Field(..., description="Actionable recommendation to solve the problem")
    impact: Impact = Field(..., description="Expected impact on conversion rate")
    confidence: Confidence = Field(..., description="Confidence in the recommendation based on evidence")
    effort: Effort = Field(..., description="Estimated engineering/design effort to implement")
    experiment: str = Field(..., description="Proposed A/B test to validate the recommendation")
    quick_win: bool = Field(..., description="Whether this is a quick win (high impact, low effort)")

class ValidatedAudit(BaseModel):
    opportunities: List[Opportunity] = Field(..., description="List of prioritized CRO opportunities")
    insufficient_evidence: bool = Field(False, description="Set to true if there is not enough evidence to make recommendations")
