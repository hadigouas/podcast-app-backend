import jwt
from fastapi import Header, HTTPException


def getdata(x_auth=Header()):
    try:
        if not x_auth:
            raise HTTPException(400,{"error":"no token found"})
        valid_token=jwt.decode(x_auth,"password_key",algorithms="['HS256']")
        if not valid_token:
            raise HTTPException(400,{"error":"the token is incorrect"})
        uuid=valid_token.get("id")
        print('m here')
        return {'uid': uuid, 'token': x_auth}
    
    except jwt.PyJWKError:
        raise HTTPException(401, 'Token is not valid, authorization failed.')