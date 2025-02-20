from pathlib import Path
from re import Pattern
import logging
import re

logger = logging.getLogger()

class ReferenceParser:
    def __init__(self, profiles_dir: str):
        self.profiles_dir = self.__validate_directory(profiles_dir)

    def __validate_directory(self, directory: str) -> Path:
        path = Path(directory)

        if not path.exists():
            raise FileExistsError(f"Directory '{directory}' does not exists")

        if not path.is_dir():
            raise ValueError(f"'{directory}' is not a directory")

        return path

    def __extract(
        self, filename: Path
    ) -> list[tuple[str, ...]]:
        pattern: Pattern = re.compile(
            r"(?P<profile>^Profile: .*$)\n"
            r"(?P<parent>^Parent: .*$)", 
            re.M
        )
        results: list[tuple[str, ...]] = []

        with open(filename, "r") as fh:
            file = fh.read()

            m = pattern.search(file)

            for m in pattern.finditer(file):
                if m:
                    results.append(
                        (str(filename), m.group("profile"), m.group("parent"))
                    )

        return results
    
    def __transform(self, result: tuple[str, ...]) -> tuple[str, ...]:
        pattern = re.compile(r"^.*:")
        result = tuple(
            map(
                lambda s:  pattern.sub("", s), 
                result[1:]
            )
        )

        return result

    def parse(self) -> list[tuple[str, ...]]:
        parsed: list[tuple[str, ...]] = []

        for file in self.profiles_dir.glob("**/*.fsh"):
            extracted = self.__extract(file)

            for result in extracted:
                transformed = self.__transform(result)
                parsed.append(transformed)

        return parsed