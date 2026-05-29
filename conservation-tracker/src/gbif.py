"""
GBIF (Global Biodiversity Information Facility) API client.
Docs: https://www.gbif.org/developer/summary
No authentication needed for read-only access.
"""

import requests

BASE_URL = "https://api.gbif.org/v1"


def search_species(q, rank=None, kingdom=None, limit=20, offset=0):
    """
    Search the GBIF species backbone by name.
    rank: SPECIES, GENUS, FAMILY, ORDER, CLASS, PHYLUM, KINGDOM
    """
    params = {"q": q, "limit": limit, "offset": offset}
    if rank:
        params["rank"] = rank
    if kingdom:
        params["kingdom"] = kingdom

    resp = requests.get(f"{BASE_URL}/species/search", params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()


def get_occurrences(taxon_key, country=None, year=None, limit=300, offset=0):
    """
    Get occurrence records for a species by its GBIF taxon key.
    taxon_key: integer key from search_species results.
    country:   ISO 2-letter country code, e.g. "US", "BR"
    year:      single year or range string e.g. "2000,2024"
    """
    params = {"taxonKey": taxon_key, "limit": limit, "offset": offset, "hasCoordinate": True}
    if country:
        params["country"] = country
    if year:
        params["year"] = year

    resp = requests.get(f"{BASE_URL}/occurrence/search", params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()


def occurrence_count_by_country(taxon_key):
    """Return occurrence counts grouped by country for a given taxon key."""
    params = {"taxonKey": taxon_key, "dimension": "country"}
    resp = requests.get(f"{BASE_URL}/occurrence/counts/schema", params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()


def get_species_info(taxon_key):
    """Return full metadata for a single species by GBIF taxon key."""
    resp = requests.get(f"{BASE_URL}/species/{taxon_key}", timeout=30)
    resp.raise_for_status()
    return resp.json()
