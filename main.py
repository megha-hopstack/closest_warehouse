#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 16:57:56 2024

@author: megha
"""

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional, Union
import googlemaps
import os

app = FastAPI()

# Initialize Google Maps client
API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")  # Replace with your API key or use an environment variable
gmaps = googlemaps.Client(key=API_KEY)

class Warehouse(BaseModel):
    warehouse_name: str
    address: str

class DistanceRequest(BaseModel):
    to_address: Optional[str] = None
    from_address: Optional[List[Warehouse]] = None

class ValidResponse(BaseModel):
    closest_warehouse: Warehouse

class InvalidResponse(BaseModel):
    closest_warehouse: Optional[None] = None
    invalid_addresses: Optional[List[str]] = None
    error_message: Optional[str] = None

ResponseModel = Union[ValidResponse, InvalidResponse]

@app.post("/closest-warehouse/", response_model=ResponseModel)
async def get_closest_warehouse(data: DistanceRequest):
    invalid_addresses = []

    # 1. Check if `to_address` and `from_address` are empty
    if not data.to_address and not data.from_address:
        return InvalidResponse(
            closest_warehouse=None,
            error_message="Both `to_address` and `from_address` are required and cannot be empty."
        )
    elif not data.to_address:
        return InvalidResponse(
            closest_warehouse=None,
            error_message="`to_address` is required and cannot be empty."
        )
    elif not data.from_address or len(data.from_address) == 0:
        return InvalidResponse(
            closest_warehouse=None,
            error_message="`from_address` is required and cannot be empty."
        )

    # 2. Validate `to_address`
    to_address_check = gmaps.distance_matrix(
        origins=["1 Infinite Loop, Cupertino, CA"],  # Arbitrary valid point
        destinations=[data.to_address],
        mode="driving"
    )
    if to_address_check['rows'][0]['elements'][0].get('status') != 'OK':
        return InvalidResponse(
            closest_warehouse=None,
            error_message="The `to_address` is invalid.",
            invalid_addresses=[data.to_address]
        )

    # 3. Validate each `from_address`
    closest_warehouse = None
    shortest_distance_meters = float("inf")

    for warehouse in data.from_address:
        response = gmaps.distance_matrix(
            origins=[warehouse.address],
            destinations=[data.to_address],
            mode="driving"
        )

        # If `from_address` is invalid, add to `invalid_addresses`
        if response['rows'][0]['elements'][0].get('status') != 'OK':
            invalid_addresses.append(warehouse.address)
        else:
            # Calculate distance if address is valid
            distance_meters = response['rows'][0]['elements'][0]['distance']['value']
            if distance_meters < shortest_distance_meters:
                shortest_distance_meters = distance_meters
                closest_warehouse = warehouse

    # 4. Return if any `from_address` entries are invalid
    if invalid_addresses:
        return InvalidResponse(
            closest_warehouse=None,
            invalid_addresses=invalid_addresses,
            error_message="Some `from_address` entries are invalid."
        )

    # 5. If all addresses are valid, return the closest warehouse
    return ValidResponse(closest_warehouse=closest_warehouse)