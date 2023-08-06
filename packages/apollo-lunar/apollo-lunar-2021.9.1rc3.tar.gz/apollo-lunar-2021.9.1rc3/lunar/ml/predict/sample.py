from typing import Any, Dict, List


async def predict(models: Any, id: str, channel_id: str, **params) -> List[Dict[str, Any]]:
    y = models[0].predict([1, 2, 3])
    return [{"id": y}]
