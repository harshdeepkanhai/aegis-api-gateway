import pytest
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials

from aegis.adapters.auth import get_current_user, issue_dev_token, require_scope


def _cred(tok: str) -> HTTPAuthorizationCredentials:
    return HTTPAuthorizationCredentials(scheme="Bearer", credentials=tok)


def test_valid_token_yields_scopes() -> None:
    user = get_current_user(_cred(issue_dev_token("u1", ["read:authors"])))
    assert user.subject == "u1"
    assert "read:authors" in user.scopes


def test_garbage_token_rejected() -> None:
    with pytest.raises(HTTPException) as exc:
        get_current_user(_cred("not-a-jwt"))
    assert exc.value.status_code == 401


def test_require_scope_allows_matching_scope() -> None:
    user = get_current_user(_cred(issue_dev_token("u1", ["read:authors"])))
    dep = require_scope("read:authors")
    assert dep(user) is user


def test_require_scope_rejects_missing_scope() -> None:
    user = get_current_user(_cred(issue_dev_token("u1", ["read:authors"])))
    dep = require_scope("write:authors")
    with pytest.raises(HTTPException) as exc:
        dep(user)
    assert exc.value.status_code == 403
