from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader


X_API_KEY = APIKeyHeader(name="x-api-key")
VALUE_API_KEY = "BigProfiles-API"


def check_authentication_header(x_api_key: str = Depends(X_API_KEY)):

    if x_api_key == VALUE_API_KEY:
        return True

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid API Key",
    )
