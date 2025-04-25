import distinctipy # type: ignore

class Mapper:
    def __init__(self, profiles: list[dict], logical_map: dict[str, tuple[str, ...]]):
        self.colormap: dict[str, str] = {}
        self.logical_map = logical_map
        self.types: set[str] = set()
        self.profiles = profiles

        self._set_unique_types()
        self._set_colormap()

    def _set_unique_types(self):
        types = {p["type"] for p in self.profiles if "type" in p}
        self.types = types

    def _set_colormap(self):
        colormap = self._create_colormap()
        self.colormap = colormap

    def _create_colormap(self) -> dict[str, str]:
        n_types = len(self.types)
        colors = distinctipy.get_colors(
            n_types, pastel_factor=0.7, colorblind_type="Deuteranomaly"
        )
        colormap: dict[str, str] = {}

        for t, c in zip(self.types, colors):
            colormap[t] = distinctipy.get_hex(c)

        return colormap
