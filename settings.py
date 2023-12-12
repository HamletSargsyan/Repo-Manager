from typing import List, Union, Tuple, Any
import json

from alert import alert

class Settings:
    def __init__(self) -> None:
        pass
    
    def open(self, path: str = 'settings.json') -> Union[dict, None]:
        try:
            with open(path, "r", encoding="utf-8") as f:
                return dict(json.load(f))
        except json.JSONDecodeError:
            alert('Произошла ошибка при загрузке настроек')

    def save(self, data: dict, path: str = 'settings.json') -> None:
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f)
        except json.JSONDecodeError:
            alert('Произошла ошибка при сохранении настроек')

    def get(self, key: str, default = {}) -> Union[Any, None]:
        return self.open().get(key, default)

    def get_categories(self) -> List[Tuple]:
        categories = []
        file = self.open()
        for index, category in enumerate(file, start=1):
            if category not in categories:
                categories.append((category, index))
        return categories