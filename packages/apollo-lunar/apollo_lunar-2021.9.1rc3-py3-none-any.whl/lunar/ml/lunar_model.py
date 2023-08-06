from typing import Any, Callable, Dict, List, Optional


class LunarModel:
    def __init__(self, name: str, version: str, predict_fn: Callable, models: Optional[List[Any]] = []):
        self.name = name
        self.version = version
        self.predict_fn = predict_fn
        self.models = models
        self.params = {}

    def add_param(self, key: str, value: Any) -> None:
        self.params[key] = value

    def remove_param(self, key: str) -> None:
        self.params.pop(key, None)

    def clear_params(self) -> None:
        self.params = {}

    async def predict(self, id: str, channel_id: str, **params) -> List[Dict[str, Any]]:
        return await self.predict_fn(models=self.models, id=id, channel_id=channel_id, **params)
