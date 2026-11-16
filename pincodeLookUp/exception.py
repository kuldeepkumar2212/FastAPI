
# Import JSONResponse to return custom JSON error responses
from fastapi.responses import JSONResponse

# Import Request to access the incoming HTTP request
from fastapi import Request


# -------------------- CUSTOM EXCEPTION CLASSES --------------------

# Custom exception raised when a requested pincode
# does not exist in the available records.
class PincodeNotFoundError(Exception):

    # Constructor to initialize the exception with the pincode
    # that could not be found.
    def __init__(self, pincode: str):
        self.pincode = pincode


# Custom exception raised when the provided pincode
# does not follow the expected format or validation rules.
class InvalidPincodeError(Exception):

    # Constructor accepts the invalid pincode and an optional reason.
    # If no reason is provided, it defaults to "Invalid Format".
    def __init__(self, pincode: str, reason: str = "Invalid Format"):
        self.pincode = pincode
        self.reason = reason


# -------------------- CUSTOM EXCEPTION HANDLERS --------------------

# Exception handler for PincodeNotFoundError.
# This function is called when this specific exception is raised
# and registered with the FastAPI application.
async def pincode_not_found(request: Request, exc: PincodeNotFoundError):

    # Return a custom JSON response with HTTP status code 404.
    # 404 means the requested resource (pincode) was not found.
    return JSONResponse(
        status_code=404,
        content={
            "error": "Pincode not found",
            "message": f"The entered pincode is not available: {exc.pincode}",
            "pincode": exc.pincode
        }
    )


# Exception handler for InvalidPincodeError.
# This function handles cases where the provided pincode is invalid.
async def invalid_Pincode(request: Request, exc: InvalidPincodeError):

    # Return a custom JSON response with HTTP status code 400.
    # 400 means the client has sent an invalid request.
    return JSONResponse(
        status_code=400,
        content={
            "error": "Invalid pincode",
            "message": f"The entered pincode is invalid: {exc.pincode}, reason: {exc.reason}",
            "pincode": exc.pincode
        }
    )
