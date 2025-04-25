from jinja2 import PackageLoader, Environment, select_autoescape
from fhir_referencer.parser import Profile
from collections import defaultdict
import distinctipy # type: ignore


class ReferenceRenderer:
    def __init__(
        self,
        profiles: list[Profile],
        template_name: str,
        diagram_name: str
    ):
        self.packages: dict[str, list[dict[str, str]]] = {}
        self.references: list[dict[str, str]] = []
        self.template_name: str = template_name
        self.diagram_name: str = diagram_name
        self.unique_types: set[str] = set()
        self.colormap: dict[str, str] = {}
        self.profiles = profiles

        self._set_unique_types()
        self._set_references()
        self._set_packages()
        self._set_colormap()

    def _set_unique_types(self):
        types = set(map(lambda p: p.type, self.profiles)) 
        self.unique_types = types

    def _set_colormap(self):
        colormap = self._create_colormap()
        self.colormap = colormap

    def _set_packages(self):
        packages = self._create_packages()
        self.packages = packages

    def _set_references(self):
        references = self._create_references()
        self.references = references

    def _get_profile_by_url(self, url: str) -> Profile | None:
        output: Profile | None = None

        for profile in self.profiles:
            if url == profile.url:
                output = profile
                break

        return output

    def _create_colormap(self) -> dict[str, str]:
        n_types = len(self.unique_types)
        colors = distinctipy.get_colors(
            n_types, pastel_factor=0.7, colorblind_type="Deuteranomaly"
        )
        colormap: dict[str, str] = {}

        for t, c in zip(sorted(self.unique_types), colors):
            colormap[t] = distinctipy.get_hex(c)

        return colormap

    def _create_packages(self) -> dict[str, list[dict[str, str]]]:
        packages: dict[str, list[dict[str, str]]] = defaultdict(list)

        for profile in self.profiles:
            obj = {"name": profile.name, "type": profile.type}            
            packages[profile.package].append(obj)

        return dict(packages)

    def _create_references(self) -> list[dict[str, str]]:
        references: list[dict[str, str]] = []

        for profile in self.profiles:
            for field, urls in profile.references.items():

                for url in urls:
                    if linked_profile := self._get_profile_by_url(url):
                        references.append(
                            {
                                "source": profile.name,
                                "destination": linked_profile.name,
                                "field": field,
                            }
                        )

        return references

    def render(self) -> str:
        env = Environment(
            loader=PackageLoader("fhir_referencer"),
            autoescape=select_autoescape()
        )
        tmp = env.get_template(self.template_name)
        puml = tmp.render(
            diagram_name=self.diagram_name, 
            colors=self.colormap, 
            packages=self.packages,
            references=self.references
        )

        return puml