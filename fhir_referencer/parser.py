from pathlib import Path

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
    
    def parse(self):
        ...
