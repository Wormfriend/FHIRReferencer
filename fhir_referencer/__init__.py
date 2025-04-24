from argparse import ArgumentParser

argparser = ArgumentParser(
    description=(
        "Tool for visualizing dependencies in FHIR Ressources using PlantUML"
    )
)
argparser.add_argument("-p", "--profiles", type=str, help="Path to the profiles directory")
argparser.add_argument("-r", "--resources", type=str, help="Path to the resources directory")