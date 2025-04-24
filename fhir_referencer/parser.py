from pathlib import Path
# from re import Pattern
import logging
import json
# import re

logger = logging.getLogger()

class ReferenceParser:
    def __init__(self, profiles_dir: str, resources_dir: str):
        self.resources_dir = self.__validate_directory(resources_dir)
        self.profiles_dir = self.__validate_directory(profiles_dir)
        self.logical_map: dict[str, str] = {}
        self.profiles: list[dict] = []

    def __validate_directory(self, directory: str) -> Path:
        path = Path(directory)

        if not path.exists():
            raise FileExistsError(f"Directory '{directory}' does not exists")

        if not path.is_dir():
            raise ValueError(f"'{directory}' is not a directory")

        return path

    # def __extract(self, filename: Path):
    #     pattern_profile = re.compile(r"^Profile: +(?P<name>\S*)")
    #     pattern_reference = re.compile(
    #         r"^[ \t]*\* (?P<field>\S+) only Reference\((?P<references>.*?)\)",
    #         flags=re.M | re.S,
    #     )
    #     file = ""

    #     with open(filename, "r") as fh:
    #         file = fh.read()

    #     profiles = list(pattern_profile.finditer(file))
    #     references = list(pattern_reference.finditer(file))
    #     pass
        # with open(filename, "r") as fh:
        #     profile = ""

        #     for line in fh.readlines():
        #         # line = re.escape(line)

        #         if m:= pattern_profile.match(line):
        #             profile = m.group("name")
        #             self.profiles.add(profile)

        #         elif (m := pattern_reference.match(line)) and profile:
        #             references = list(
        #                 map(lambda r: r.strip(), m.group("references").split(" or "))
        #             )
        #             field = m.group("field")

        #             for reference in references:
        #                 self.references.add((profile, reference, field))

    # def __cleanup(self):
    #     marked: list[tuple[str, str, str]] = []

    #     for triplet in self.references:
    #         if not triplet[1] in self.profiles:
    #             marked.append(triplet)

    #     for t in marked:
    #         self.references.remove(t)

    def __extract_logical_structure(self):
        for file in self.profiles_dir.glob("**/*.fsh"):
            pass

    def __load_profiles_and_resources(self):
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

                self.profiles.append(profile)

    def parse(self) -> tuple[list[dict], dict[str, str]]:
        self.__load_profiles_and_resources()
        # for file in self.profiles_dir.glob("**/*.fsh"):
        #     self.__extract(file)
            # self.__extract(file)

        # self.__cleanup()

        return self.profiles, self.logical_map
