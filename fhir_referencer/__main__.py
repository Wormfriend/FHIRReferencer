from fhir_referencer.parser import ReferenceParser
from fhir_referencer import argparser

args = argparser.parse_args()

refparser = ReferenceParser(args.profiles, args.resources)
profiles, logical_map = refparser.parse()

# for reference in references:
#     print(reference)