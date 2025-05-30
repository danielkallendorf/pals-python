import json
import os
import sys
import yaml

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from schema.MagneticMultipoleParameters import MagneticMultipoleParameters

from schema.DriftElement import DriftElement
from schema.QuadrupoleElement import QuadrupoleElement

from schema.Line import Line


def main():
    drift1 = DriftElement(
        length=0.25,
    )
    quad1 = QuadrupoleElement(
        length=1.0,
        MagneticMultipoleP=MagneticMultipoleParameters(
            Bn1=1.0,
        ),
    )
    drift2 = DriftElement(
        length=0.5,
    )
    quad2 = QuadrupoleElement(
        length=1.0,
        MagneticMultipoleP=MagneticMultipoleParameters(
            Bn1=-1.0,
        ),
    )
    drift3 = DriftElement(
        length=0.5,
    )
    # Create line with all elements
    line = Line(
        line={
            "drift1": drift1,
            "quad1": quad1,
            "drift2": drift2,
            "quad2": quad2,
            "drift3": drift3,
        }
    )

    # Serialize to YAML
    yaml_data = yaml.dump(line.model_dump(), default_flow_style=False, sort_keys=False)
    print("Dumping YAML data...")
    print(f"{yaml_data}")
    # Write YAML data to file
    yaml_file = "examples_fodo.yaml"
    with open(yaml_file, "w") as file:
        file.write(yaml_data)
    # Read YAML data from file
    with open(yaml_file, "r") as file:
        yaml_data = yaml.safe_load(file)
    # Parse YAML data
    loaded_line = Line(**yaml_data)
    # Validate loaded data
    assert line == loaded_line

    # Serialize to JSON
    json_data = json.dumps(line.model_dump(), indent=2)
    print("Dumping JSON data...")
    print(f"{json_data}")
    # Write JSON data to file
    json_file = "examples_fodo.json"
    with open(json_file, "w") as file:
        file.write(json_data)
    # Read JSON data from file
    with open(json_file, "r") as file:
        json_data = json.loads(file.read())
    # Parse JSON data
    loaded_line = Line(**json_data)
    # Validate loaded data
    assert line == loaded_line


if __name__ == "__main__":
    main()
