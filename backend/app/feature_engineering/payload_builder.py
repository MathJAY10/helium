import json
from typing import Any, Dict
from app.feature_engineering.models import FeatureSet

def build_llm_payload(feature_set: FeatureSet) -> str:
    """
    Creates an optimized, dense payload for the LLM by removing metadata,
    sources, and URLs to save tokens.
    """
    def _optimize_dict(data: Dict[str, Any]) -> Dict[str, Any]:
        optimized = {}
        for k, v in data.items():
            if isinstance(v, dict):
                # If it's a BusinessFeature, extract just the boolean/value
                if "value" in v and "status" in v:
                    # Keep it only if it was FOUND and True (to compress size)
                    if v["status"] == "FOUND" and v["value"]:
                        optimized[k] = True
                else:
                    opt = _optimize_dict(v)
                    if opt:
                        optimized[k] = opt
            elif isinstance(v, list):
                opt_list = []
                for item in v:
                    if isinstance(item, dict):
                        opt = _optimize_dict(item)
                        if opt:
                            opt_list.append(opt)
                    elif item:
                        opt_list.append(item)
                if opt_list:
                    optimized[k] = opt_list
            elif v:
                optimized[k] = v
        return optimized

    # Dump the feature set without metadata and quality metrics for LLM
    data = {
        "homepage": feature_set.homepage.model_dump(),
        "collections": [c.model_dump() for c in feature_set.collections],
        "products": [p.model_dump() for p in feature_set.products],
        "cart": feature_set.cart.model_dump()
    }

    optimized = _optimize_dict(data)
    return json.dumps(optimized, separators=(',', ':'))
