"""
IUCN Red List API v4 client.
Docs: https://api.iucnredlist.org/api/v4/

Set your token in the IUCN_TOKEN environment variable, or pass it directly.
Get a free token at: https://www.iucnredlist.org (account page)
"""

import os
import time
import requests

BASE_URL = "https://api.iucnredlist.org/api/v4"

# Taxonomic groups we care about for this project
TAXONOMIC_GROUPS = [
    ("class", "mammalia"),
    ("class", "aves"),
    ("class", "amphibia"),
    ("class", "reptilia"),
    ("class", "actinopterygii"),   # ray-finned fish
    ("class", "insecta"),
]


def _get_headers(token=None):
    t = token or os.environ.get("IUCN_TOKEN")
    if not t:
        raise ValueError(
            "No IUCN token found. Set the IUCN_TOKEN environment variable "
            "or pass token= directly."
        )
    return {"Authorization": f"Bearer {t}", "Accept": "application/json"}


def get_assessment(assessment_id, token=None):
    """Return full data for a single assessment by its ID."""
    resp = requests.get(
        f"{BASE_URL}/assessment/{assessment_id}",
        headers=_get_headers(token),
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


def get_assessments_by_sis_id(sis_id, token=None):
    """Return all assessments for a species by its SIS taxon ID."""
    resp = requests.get(
        f"{BASE_URL}/taxa/sis/{sis_id}",
        headers=_get_headers(token),
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


def get_assessments_by_name(genus, species, token=None):
    """Return all assessments for a species by genus + species name."""
    resp = requests.get(
        f"{BASE_URL}/taxa/scientific_name",
        headers=_get_headers(token),
        params={"genus_name": genus, "species_name": species},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


def get_assessments_by_taxonomy(level, name, page=1, token=None, wait_time=0.3):
    """
    Return assessments for a taxonomic group, one page at a time.
    level: 'class', 'order', 'family', 'phylum', 'kingdom'
    name:  e.g. 'mammalia', 'aves', 'amphibia'  (case-insensitive)
    page:  page number (starts at 1)
    """
    resp = requests.get(
        f"{BASE_URL}/taxa/{level}/{name.lower()}",
        headers=_get_headers(token),
        params={"page": page},
        timeout=60,
    )
    resp.raise_for_status()
    time.sleep(wait_time)
    return resp.json()
