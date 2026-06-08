import time
from dataclasses import dataclass

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from aegis.config import get_settings

bearer = HTTPBearer(auto_error=True)


@dataclass(frozen=True)
class CurrentUser:
    subject: str
    scopes: frozenset[str]


def issue_dev_token(sub: str, scopes: list[str]) -> str:
    s = get_settings()
    now = int(time.time())
    payload = {
        "sub": sub,
        "scope": " ".join(scopes),
        "aud": s.jwt_audience,
        "iat": now,
        "exp": now + 3600,
    }
    return jwt.encode(payload, s.jwt_secret, algorithm=s.jwt_alg)


def get_current_user(cred: HTTPAuthorizationCredentials = Depends(bearer)) -> CurrentUser:
    s = get_settings()
    try:
        claims = jwt.decode(
            cred.credentials, s.jwt_secret, algorithms=[s.jwt_alg], audience=s.jwt_audience
        )
    except jwt.PyJWTError as exc:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "invalid token") from exc
    return CurrentUser(subject=claims["sub"], scopes=frozenset(claims.get("scope", "").split()))


def require_scope(scope: str):
    def _dep(user: CurrentUser = Depends(get_current_user)) -> CurrentUser:
        if scope not in user.scopes:
            raise HTTPException(status.HTTP_403_FORBIDDEN, f"missing scope {scope}")
        return user

    return _dep
