
# Import BaseModel to create Pydantic models
# Import field_validator to define custom validation logic
from pydantic import BaseModel, field_validator


# -------------------- SINGLE PINCODE REQUEST MODEL --------------------

# Defines the expected structure of a single pincode request.
class pincoderequest(BaseModel):

    # Pincode is accepted as a string to preserve its exact format.
    pincode: str

    # Custom validator that executes whenever the pincode field is received.
    @field_validator("pincode")
    @classmethod
    def validate_pincode(cls, value):

        # Check whether the pincode contains exactly 6 digits.
        # isdigit() ensures that the value contains only numeric characters.
        if len(value) != 6 or not value.isdigit():

            # Raise a validation error if the pincode format is incorrect.
            raise ValueError("pincode must be exactly 6 digits")

        # Return the validated value back to Pydantic.
        return value


# -------------------- LOCATION RESPONSE MODEL --------------------

# Defines the structure of the location details returned by the API.
class LocationRespnse(BaseModel):

    # Indian postal pincode.
    pincode: str

    # City associated with the pincode.
    city: str

    # District associated with the pincode.
    district: str

    # State associated with the pincode.
    state: str


# -------------------- BULK PINCODE REQUEST MODEL --------------------

# Defines the structure of a request containing multiple pincodes.
class bulkrequest(BaseModel):

    # Accepts a list of pincode strings from the client.
    pincodes: list[str]

    # Custom validator for validating the complete list of pincodes.
    @field_validator("pincodes")
    @classmethod
    def bulk_validate_pincode(cls, value):

        # Ensure that the request contains at least one pincode.
        if len(value) == 0:
            raise ValueError("at least 1 pincode is needed")

        # Restrict the number of pincodes to a maximum of 5 per request.
        if len(value) > 5:
            raise ValueError("max of 5 pincodes can be checked at once")

        # Iterate through every pincode in the received list.
        for item in value:

            # Validate each individual pincode.
            if len(item) != 6 or not item.isdigit():

                # Raise an error if any pincode has an invalid format.
                raise ValueError("pincode must be exactly 6 digits")

        # Return the complete list after successful validation.
        return value


# -------------------- BULK PINCODE RESPONSE MODEL --------------------

# Defines the structure of the response returned by the bulk lookup API.
class BulkRespnse(BaseModel):

    # Indicates the overall status of the API response.
    # Default value is "Success".
    status: str = "Success"

    # Total number of pincodes successfully found.
    found: int

    # Total number of pincodes not found in the dataset.
    not_found: int

    # List of location objects for the pincodes that were found.
    # Each item must follow the LocationRespnse model.
    results: list[LocationRespnse]

    # List containing pincodes that were not available.
    missing: list[str]
