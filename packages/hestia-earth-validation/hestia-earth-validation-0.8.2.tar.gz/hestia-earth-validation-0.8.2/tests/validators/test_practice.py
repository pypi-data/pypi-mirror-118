import json

from tests.utils import fixtures_path
from hestia_earth.validation.validators.practice import (
    validate_cropResidueManagement,
    validate_longFallowPeriod,
    validate_excretaManagement
)


def test_validate_cropResidueManagement_valid():
    # no practices should be valid
    assert validate_cropResidueManagement([])

    with open(f"{fixtures_path}/practice/cropResidueManagement/valid.json") as f:
        data = json.load(f)
    assert validate_cropResidueManagement(data.get('nodes')) is True


def test_validate_cropResidueManagement_invalid():
    with open(f"{fixtures_path}/practice/cropResidueManagement/invalid.json") as f:
        data = json.load(f)
    assert validate_cropResidueManagement(data.get('nodes')) == {
        'level': 'error',
        'dataPath': '.practices',
        'message': 'value should sum to 100 or less across crop residue management practices',
        'params': {
            'sum': 110
        }
    }


def test_validate_longFallowPeriod_valid():
    # no practices should be valid
    assert validate_longFallowPeriod([])

    with open(f"{fixtures_path}/practice/longFallowPeriod/valid.json") as f:
        data = json.load(f)
    assert validate_longFallowPeriod(data.get('nodes')) is True


def test_validate_longFallowPeriod_invalid():
    with open(f"{fixtures_path}/practice/longFallowPeriod/invalid.json") as f:
        data = json.load(f)
    assert validate_longFallowPeriod(data.get('nodes')) == {
        'level': 'error',
        'dataPath': '.practices[1].value',
        'message': 'longFallowPeriod must be lower than 5 years'
    }


def test_validate_excretaManagement_valid():
    # no practices should be valid
    assert validate_excretaManagement({}, [])

    with open(f"{fixtures_path}/practice/excretaManagement/valid.json") as f:
        cycle = json.load(f)
    assert validate_excretaManagement(cycle, cycle.get('practices')) is True


def test_validate_excretaManagement_invalid():
    with open(f"{fixtures_path}/practice/excretaManagement/invalid.json") as f:
        cycle = json.load(f)
    assert validate_excretaManagement(cycle, cycle.get('practices')) == {
        'level': 'error',
        'dataPath': '.practices',
        'message': 'an excreta input is required when using an excretaManagement practice'
    }
