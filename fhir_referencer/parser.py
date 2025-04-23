from pathlib import Path
from re import Pattern
import logging
import re

logger = logging.getLogger()

class ReferenceParser:
    def __init__(self, profiles_dir: str):
        self.profiles_dir = self.__validate_directory(profiles_dir)
        self.references: set[tuple[str, str, str]] = set()
        self.profiles: set[str] = set()

    def __validate_directory(self, directory: str) -> Path:
        path = Path(directory)

        if not path.exists():
            raise FileExistsError(f"Directory '{directory}' does not exists")

        if not path.is_dir():
            raise ValueError(f"'{directory}' is not a directory")

        return path

    def __extract(self, filename: Path):
        pattern_profile = re.compile(r"^Profile: *(?P<name>\S*)")
        pattern_reference = re.compile(r"^\* (?P<field>\S+) .*Reference\((?P<references>.+)\)$")

        with open(filename, "r") as fh:
            profile = ""

            for line in fh.readlines():
                if m:= pattern_profile.match(line):
                    profile = m.group("name")
                    self.profiles.add(profile)

                elif (m := pattern_reference.match(line)) and profile:
                    references = list(
                        map(lambda r: r.strip(), m.group("references").split("or"))
                    )
                    field = m.group("field")

                    for reference in references:
                        self.references.add((profile, reference, field))

    def parse(self) -> tuple[set[str], set[tuple[str, str, str]]]:
        parsed: list[tuple[str, ...]] = []

        for file in self.profiles_dir.glob("**/*.fsh"):
            self.__extract(file)

        return self.profiles, self.references
