from fhir_referencer.plantuml import ReferenceRenderer
from fhir_referencer.parser import ReferenceParser
from fhir_referencer import argparser

args = argparser.parse_args()

refparser = ReferenceParser(args.profiles, args.resources)
profiles = refparser.parse()

renderer = ReferenceRenderer(
    profiles, "reference.jinja", args.diagram_name
)
puml = renderer.render()

with open(args.output, "w") as fh:
    fh.write(puml)