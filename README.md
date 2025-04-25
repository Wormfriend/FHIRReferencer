# FHIR Referencer

## Description

This is a small CLI helper for creating plantUML references diagrams for FHIR resources.
Before you get started run ```sushi``` to create the necessary resource json-files.

## Instruction

1. Clone this repository
2. Install dependencies ```pip install -r requirements.txt``
3. Run referencer

```bash
python -m fhir_referencer -p {directory containing the .fsh-profiles} \
-r {directory containing the json resources aka sushi output} \
-o {filename of the plantuml (pu) output file}
-n {name of the diagram after rendering also the filename}
```
