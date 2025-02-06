from argparse import ArgumentParser

argparser = ArgumentParser(
    description=(
        "Tool for visualizing dependencies in FHIR Ressources using PlantUML"
    )
)
argparser.add_argument("-p", "--path", type=str, help="Path to the profiles directory")