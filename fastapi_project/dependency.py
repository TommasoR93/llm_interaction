from fastapi import Header, HTTPException

# fake authentication dependency

def verify_api_key(apy_key: str = Header()):
    if apy_key != "secret123":
        raise HTTPException(status_code=401, detail="Invalid API KEY")
    return apy_key