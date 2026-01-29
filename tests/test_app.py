import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))

from app import app
from dash import dcc, html


def find_components(component, component_type):
    """
    Recursively search Dash layout for components of a given type
    """
    found = []

    if isinstance(component, component_type):
        found.append(component)

    if hasattr(component, "children"):
        children = component.children

        if isinstance(children, list):
            for child in children:
                found.extend(find_components(child, component_type))
        else:
            found.extend(find_components(children, component_type))

    return found


def test_header_present():
    headers = find_components(app.layout, html.H1)

    assert len(headers) == 1
    assert headers[0].children == "Pink Morsels Sales Visualiser"


def test_graph_present():
    graphs = find_components(app.layout, dcc.Graph)

    assert len(graphs) == 1
    assert graphs[0].id == "sales-graph"


def test_region_picker_present():
    radios = find_components(app.layout, dcc.RadioItems)

    assert len(radios) == 1
    assert radios[0].id == "region-selector"
