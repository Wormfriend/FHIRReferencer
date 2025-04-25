from jinja2 import PackageLoader, Environment, select_autoescape
from fhir_referencer.parser import Profile
import distinctipy # type: ignore


class ReferenceRenderer:
    def __init__(
        self,
        profiles: list[Profile],
        logical_map: dict[str, tuple[str, ...]],
        template_name: str,
        diagram_name: str
    ):
        self.template_name: str = template_name
        self.legend: list[dict[str, str]] = []
        self.diagram_name: str = diagram_name
        self.colormap: dict[str, str] = {}
        self.uq_types: set[str] = set()
        self.logical_map = logical_map
        self.profiles = profiles

        self._set_unique_types()
        self._set_colormap()

    def _set_unique_types(self):
        types = set(map(lambda p: p.type, self.profiles)) 
        self.uq_types = types

    def _set_colormap(self):
        colormap = self._create_colormap()
        self.colormap = colormap

    def _create_colormap(self) -> dict[str, str]:
        n_types = len(self.uq_types)
        colors = distinctipy.get_colors(
            n_types, pastel_factor=0.7, colorblind_type="Deuteranomaly"
        )
        colormap: dict[str, str] = {}

        for t, c in zip(sorted(self.uq_types), colors):
            colormap[t] = distinctipy.get_hex(c)

        return colormap

    def render(self) -> str:
        env = Environment(
            loader=PackageLoader("fhir_referencer"),
            autoescape=select_autoescape()
        )
        tmp = env.get_template(self.template_name)
        puml = tmp.render(diagram_name=self.diagram_name, colors=self.colormap)

        return puml
