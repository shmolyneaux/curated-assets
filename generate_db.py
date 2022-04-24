#!/usr/bin/env python3

import json
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, List, Union

root_path = Path(__file__).parent
asset_info_path = root_path / "asset_info"
creator_info_path = root_path / "creator_info"
license_info_path = root_path / "license_info"

output_path = root_path / "src/lib/db.js"

assets = {}
creators = {}
licenses = {}

def first_true(itr, key, default=None):
    for item in itr:
        if key(item):
            return item
    return default

def check_schema(*, data, schema) -> List[str]:
    """Check data against a schema returning any errors found."""
    errors = []
    data_only_keys = set(data) - set(schema)
    common_keys = set(data) & set(schema)
    schema_only_keys = set(schema) - set(data)

    for key in data_only_keys:
        errors.append(f"data contains unknown key {key}")

    for key in schema_only_keys:
        errors.append(f"schema expected an entry for key {key}")

    for key in common_keys:
        data_value = data[key]
        schema_type = schema[key]
        if schema_type not in (str, List[str], Optional[str]):
            errors.append(f"Unknown schema type {schema_type}")

        if schema_type == str:
            if isinstance(data_value, str):
                continue
            errors.append(f"key '{key}' in data is not a string, found {data_value}")

        elif schema_type == List[str]:
            if not isinstance(data_value, list):
                errors.append(f"key '{key}' in data is not a list, found {data_value}")
                continue
            for idx, item in enumerate(data_value):
                if isinstance(item, str):
                    continue
                errors.append(f"index {idx} of key '{key}' is not a string, found {item}")

        else:
            if isinstance(data_value, str):
                continue
            if data_value is None:
                continue

            errors.append(f"Expected optional string, but found {data_value}")

    return errors


def validate_license(license_info):
    schema = {
        "short_name": str,
        "long_name": str,
        "link": str,
    }

    return check_schema(data=license_info, schema=schema)

def validate_creator(creator_info):
    schema = {
        "name": str,
        "bio": str,
        "links": List[str],
    }

    return check_schema(data=creator_info, schema=schema)

def validate_asset(*, asset_info, licenses, creators):
    schema = {
        "name": str,
        "category": str,
        "description": str,
        "tags": List[str],
        "assets": List[str],
        "thumbnail": str,
        "images": List[str],
        "creator_id": str,
        "sources": List[str],
        "license_id": str,
        "credit_text": Optional[str],
    }

    errors = check_schema(data=asset_info, schema=schema)

    if not errors:
        license_id = asset_info["license_id"]
        if not license_id in licenses:
            errors.append(f"could not find license {license_id}")

        creator_id = asset_info["creator_id"]
        if not creator_id in creators:
            errors.append(f"could not find creator {creator_id}")

    return errors


def print_errors(heading: str, errors: List[str]):
    print(heading, ":", sep="", file=sys.stderr)
    for error in errors:
        print("    ", error, sep="", file=sys.stderr)

found_errors = False

for license_file in license_info_path.glob("*.json"):
    license_info = json.loads(license_file.read_text())
    if validation_errors := validate_license(license_info):
        found_errors = True
        print_errors(f"{license_file} is not a valid license", validation_errors)
    else:
        licenses[license_file.stem] = license_info

for creator_file in creator_info_path.glob("*.json"):
    creator_info = json.loads(creator_file.read_text())
    if validation_errors := validate_creator(creator_info):
        found_errors = True
        print_errors(f"{creator_file} is not a valid creator", validation_errors)
    else:
        creators[creator_file.stem] = creator_info

for asset_file in asset_info_path.glob("*.json"):
    asset_info = json.loads(asset_file.read_text())
    if validation_errors := validate_asset(
        asset_info=asset_info,
        licenses=licenses,
        creators=creators,
    ):
        found_errors = True
        print_errors(f"{asset_file} is not a valid asset", validation_errors)
    else:
        assets[asset_file.stem] = asset_info

if found_errors:
    sys.exit("Found errors while generating DB")

# TODO: assign priorities to the categories
asset_categories = list({asset_info["category"] for asset_info in assets.values()})

db = {
    "asset_categories": asset_categories,
    "assets": assets,
    "creators": creators,
    "licenses": licenses,
}

js_text = f"""\
export let db = {json.dumps(db, indent=4)};
"""

output_path.write_text(js_text)
