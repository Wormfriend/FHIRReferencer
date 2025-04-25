from pydantic import BaseModel
from pathlib import Path
import logging
import json
import re


logger = logging.getLogger()


class Profile(BaseModel):
    name: str
    id: str
    url: str
    type: str
    references: dict[str, list[str]]


class ReferenceParser:
    def __init__(self, profiles_dir: str, resources_dir: str):
        self.resources_dir = self._validate_directory(resources_dir)
        self.profiles_dir = self._validate_directory(profiles_dir)
        self.logical_map: dict[str, tuple[str, ...]] = {}
        self.profiles: list[Profile] = []

    def _validate_directory(self, directory: str) -> Path:
        path = Path(directory)

        if not path.exists():
            raise FileExistsError(f"Directory '{directory}' does not exists")

        if not path.is_dir():
            raise ValueError(f"'{directory}' is not a directory")

        return path

    def _extract_logical_structure(self):
        pattern = re.compile(r"^Id: +(?P<id>\S+)", flags=re.M)
        logical_map = {}

        for file in self.profiles_dir.glob("**/*.fsh"):
            text = file.read_text()
            path = file.parent.parts
                    
            for m in pattern.finditer(text):
                if m:
                    logical_map[m.group("id")] = path

        self.logical_map = logical_map

    def _load_profiles_and_resources(self):
        for file in self.resources_dir.glob("*.json"):
            data = json.loads(file.read_text())
            
            if "kind" in data and data["kind"] == "resource":
                profile = {
                    "name": data["name"],
                    "id": data["id"],
                    "url": data["url"],
                    "type": data["type"],
                    "references": {}
                }
                element: dict

                for element in data["differential"]["element"]:

                    if _type := element.get("type", None):
                        for t in _type:

                            if "code" in t and t["code"] == "Reference":
                                profile["references"][element["path"]] = t["targetProfile"]

                self.profiles.append(Profile(**profile))

    def parse(self) -> tuple[list[Profile], dict[str, tuple[str, ...]]]:
        self._load_profiles_and_resources()
        self._extract_logical_structure()

        return self.profiles, self.logical_map
