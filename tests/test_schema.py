import os
from pydantic import ValidationError

import json
import yaml

from schema.MagneticMultipoleParameters import MagneticMultipoleParameters

from schema.BaseElement import BaseElement
from schema.ThickElement import ThickElement
from schema.DriftElement import DriftElement
from schema.QuadrupoleElement import QuadrupoleElement

from schema.Line import Line


def test_BaseElement():
    # nothing to test here
    pass


def test_ThickElement():
    # Create one thick element with custom name and length
    element_length = 1.0
    element = ThickElement(
        length=element_length,
    )
    assert element.length == element_length
    # Try to assign negative length and
    # detect validation error without breaking pytest
    element_length = -1.0
    passed = True
    try:
        element.length = element_length
    except ValidationError as e:
        print(e)
        passed = False
    assert not passed


def test_DriftElement():
    # Create one drift element with custom name and length
    element_length = 1.0
    element = DriftElement(
        length=element_length,
    )
    assert element.length == element_length
    # Try to assign negative length and
    # detect validation error without breaking pytest
    element_length = -1.0
    passed = True
    try:
        element.length = element_length
    except ValidationError as e:
        print(e)
        passed = False
    assert not passed


def test_QuadrupoleElement():
    # Create one drift element with custom name and length
    element_length = 1.0
    element_magnetic_multipole_Bn1 = 1.1
    element_magnetic_multipole_Bn2 = 1.2
    element_magnetic_multipole_Bs1 = 2.1
    element_magnetic_multipole_Bs2 = 2.2
    element_magnetic_multipole_tilt1 = 3.1
    element_magnetic_multipole_tilt2 = 3.2
    element_magnetic_multipole = MagneticMultipoleParameters(
        Bn1=element_magnetic_multipole_Bn1,
        Bs1=element_magnetic_multipole_Bs1,
        tilt1=element_magnetic_multipole_tilt1,
        Bn2=element_magnetic_multipole_Bn2,
        Bs2=element_magnetic_multipole_Bs2,
        tilt2=element_magnetic_multipole_tilt2,
    )
    element = QuadrupoleElement(
        length=element_length,
        MagneticMultipoleP=element_magnetic_multipole,
    )
    assert element.length == element_length
    assert element.MagneticMultipoleP.Bn1 == element_magnetic_multipole_Bn1
    assert element.MagneticMultipoleP.Bs1 == element_magnetic_multipole_Bs1
    assert element.MagneticMultipoleP.tilt1 == element_magnetic_multipole_tilt1
    assert element.MagneticMultipoleP.Bn2 == element_magnetic_multipole_Bn2
    assert element.MagneticMultipoleP.Bs2 == element_magnetic_multipole_Bs2
    assert element.MagneticMultipoleP.tilt2 == element_magnetic_multipole_tilt2
    # Serialize the Line object to YAML
    yaml_data = yaml.dump(element.model_dump(), default_flow_style=False)
    print(f"\n{yaml_data}")


def test_Line():
    # Create first line with one base element
    element1 = BaseElement()
    line1 = Line(line={"element1": element1})
    assert line1.line == {"element1": element1}
    # Extend first line with one thick element
    element2 = ThickElement(length=2.0)
    line1.line.update({"element2": element2})
    assert line1.line == {"element1": element1, "element2": element2}
    # Create second line with one drift element
    element3 = DriftElement(length=3.0)
    line2 = Line(line={"element3": element3})
    # Extend first line with second line
    line1.line.update(line2.line)
    assert line1.line == {
        "element1": element1,
        "element2": element2,
        "element3": element3,
    }


def test_yaml():
    # Create one base element
    element1 = BaseElement()
    # Create one thick element
    element2 = ThickElement(length=2.0)
    # Create line with both elements
    line = Line(line={"element1": element1, "element2": element2})
    # Serialize the Line object to YAML
    yaml_data = yaml.dump(line.model_dump(), default_flow_style=False)
    print(f"\n{yaml_data}")
    # Write the YAML data to a test file
    test_file = "line.yaml"
    with open(test_file, "w") as file:
        file.write(yaml_data)
    # Read the YAML data from the test file
    with open(test_file, "r") as file:
        yaml_data = yaml.safe_load(file)
    # Parse the YAML data back into a Line object
    loaded_line = Line(**yaml_data)
    # Remove the test file
    os.remove(test_file)
    # Validate loaded Line object
    assert line == loaded_line


def test_json():
    # Create one base element
    element1 = BaseElement()
    # Create one thick element
    element2 = ThickElement(length=2.0)
    # Create line with both elements
    line = Line(line={"element1": element1, "element2": element2})
    # Serialize the Line object to JSON
    json_data = json.dumps(line.model_dump(), sort_keys=True, indent=2)
    print(f"\n{json_data}")
    # Write the JSON data to a test file
    test_file = "line.json"
    with open(test_file, "w") as file:
        file.write(json_data)
    # Read the JSON data from the test file
    with open(test_file, "r") as file:
        json_data = json.loads(file.read())
    # Parse the JSON data back into a Line object
    loaded_line = Line(**json_data)
    # Remove the test file
    os.remove(test_file)
    # Validate loaded Line object
    assert line == loaded_line
