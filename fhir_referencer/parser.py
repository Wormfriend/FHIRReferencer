from pydantic import BaseModel
from pathlib import Path
import logging
import json
import re


class Profile(BaseModel):
    name: str
    id: str
    url: str
    type: str
    package: str
    references: dict[str, list[str]]


class ReferenceParser:
    def __init__(self, profiles_dir: str, resources_dir: str):
        self.resources_dir = self._validate_directory(resources_dir)
        self.profiles_dir = self._validate_directory(profiles_dir)

    def _validate_directory(self, directory: str) -> Path:
        path = Path(directory)

        if not path.exists():
            raise FileNotFoundError(f"Directory '{directory}' does not exists")

        if not path.is_dir():
            raise ValueError(f"'{directory}' is not a directory")

        return path

    def _extract_logical_structure(self) -> dict[str, str]:
        pattern = re.compile(r"^Id: +(?P<id>\S+)", flags=re.M)
        logical_map: dict[str, str] = {}

        for file in self.profiles_dir.glob("**/*.fsh"):
            text = file.read_text()
            path = file.parent.parts

            for m in pattern.finditer(text):
                if m:
                    logical_map[m.group("id")] = ".".join(path)

        return logical_map

    def _load_profiles_and_resources(self) -> list[dict]:
        profiles: list[dict] = []

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
                                profile["references"][element["id"]] = t["targetProfile"]

                profiles.append(profile)

        return profiles

    def _merge_profiles_and_logical_map(
        self, profiles: list[dict], logical_map: dict[str, str]
    ) -> list[Profile]: 
        merged: list[Profile] = []

        for profile in profiles:
            profile["package"] = logical_map[profile["id"]]
            merged.append(Profile(**profile))

        return merged           

    def parse(self) -> list[Profile]:
        profiles = self._load_profiles_and_resources()
        logical_map = self._extract_logical_structure()
        merged = self._merge_profiles_and_logical_map(profiles, logical_map)

        return merged