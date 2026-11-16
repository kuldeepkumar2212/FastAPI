
# Import FastAPI to create the API application
from fastapi import FastAPI

# Import custom exception classes and their respective handlers
import exception

# Import Pydantic request and response models
import model

# Import the Python dictionary containing pincode details
import pincodedata


# -------------------- FASTAPI APPLICATION INITIALIZATION --------------------

# Create the FastAPI application instance
app = FastAPI(
    title="pincodeLookUp",
    description="pincodeLookUp is used to check whether the entered pincode is available in the pincodes supported by the application"
)


# -------------------- CUSTOM EXCEPTION HANDLER REGISTRATION --------------------

# Register custom exception handlers with the FastAPI application.

# Whenever PincodeNotFoundError is raised,
# FastAPI invokes the pincode_not_found handler.
app.add_exception_handler(
    exception.PincodeNotFoundError,
    exception.pincode_not_found
)

# Whenever InvalidPincodeError is raised,
# FastAPI invokes the invalid_Pincode handler.
app.add_exception_handler(
    exception.InvalidPincodeError,
    exception.invalid_Pincode
)


# -------------------- ROOT / HEALTH CHECK ENDPOINT --------------------

# GET endpoint to check whether the application is running.
# This endpoint does not require any request parameters.
@app.get("/")
def root():
    return {
        "message": "healthy",
        "status": "success"
    }


# -------------------- SINGLE PINCODE LOOKUP ENDPOINT --------------------

# GET endpoint to retrieve location details using a pincode.
# {code} is a dynamic path parameter supplied by the client.
#
# response_model defines the structure of the successful API response.
@app.get("/pincode/{code}", response_model=model.LocationRespnse)
def lookuppincode(code: str):

    # Validate whether the pincode contains exactly 6 numeric digits.
    # If the validation fails, raise a custom InvalidPincodeError.
    if len(code) != 6 or not code.isdigit():
        raise exception.InvalidPincodeError(
            code,
            "must be exactly 6 digits"
        )

    # Check whether the requested pincode exists in the dataset.
    # If it does not exist, raise a custom PincodeNotFoundError.
    if code not in pincodedata.pincode:
        raise exception.PincodeNotFoundError(code)

    # Return the complete location details for the requested pincode.
    # FastAPI validates the returned dictionary against LocationRespnse.
    return pincodedata.pincode[code]


# -------------------- BULK PINCODE LOOKUP ENDPOINT --------------------

# POST endpoint to check multiple pincodes in a single API request.
#
# request: Accepts the list of pincodes from the client.
# model.bulkrequest validates the incoming request body.
#
# response_model defines the structure of the bulk API response.
@app.post("/pincode/bulk", response_model=model.BulkRespnse)
def bulklookup(request: model.bulkrequest):

    # List to store location details of pincodes that exist.
    results = []

    # List to store pincodes that are not available in the dataset.
    missing = []

    # Iterate through each pincode received in the request body.
    for code in request.pincodes:

        # Check whether the current pincode exists in the dictionary.
        if code in pincodedata.pincode:

            # Append the complete location dictionary to results.
            results.append(pincodedata.pincode[code])

        else:
            # If the pincode does not exist, add it to the missing list.
            missing.append(code)

    # Create and return the bulk response using the Pydantic model.
    return model.BulkRespnse(

        # Total number of pincodes successfully found.
        found=len(results),

        # Total number of pincodes that were not found.
        not_found=len(missing),

        # List containing complete location details of found pincodes.
        results=results,

        # List containing pincodes that were unavailable.
        missing=missing
    )
