import asyncio
from contextlib import nullcontext as does_not_raise

import aiohttp
import pytest

from tests.functional.core.settings import test_settings
from fastapi import status


@pytest.mark.asyncio
async def test_read_role():
    pass


@pytest.mark.parametrize(
    "query_data_login, query_data_main, expected_answer, expectation",
    [
        (
                {
                    "email": "admin@admin.ru",
                    "hashed_password": "admin",
                },
                {
                    "role_name": "TestRoleName",
                    "comment": "TestComment",
                    "permissions": {
                        "logout": True,
                        "refresh_token": True,
                        "history": True,
                        "change_password": True,
                        "create_role": False,
                        "delete_role": False,
                        "change_role": False,
                        "get_roles": False,
                        "set_role": False,
                        "grab_role": False,
                        "check_role": False,
                    },
                },
                {
                    "status": status.HTTP_201_CREATED,
                },
                does_not_raise(),
        ),
        (
                {
                    "email": "admin@admin.ru",
                    "hashed_password": "admin",
                    "permissions": {
                        "logout": True,
                        "refresh_token": True,
                        "history": True,
                        "change_password": True,
                        "create_role": False,
                        "delete_role": False,
                        "change_role": False,
                        "get_roles": False,
                        "set_role": False,
                        "grab_role": False,
                        "check_role": False,
                    },
                },
                {
                    "role_name": "Admin",
                    "comment": "TestComment",
                },
                {
                    "status": status.HTTP_409_CONFLICT,
                    "detail": "Role is already exist",
                },
                does_not_raise(),
        ),
        (
                {
                    "email": "vasya@admin.ru",
                    "hashed_password": "password",
                    "permissions": {
                        "logout": True,
                        "refresh_token": True,
                        "history": True,
                        "change_password": True,
                        "create_role": False,
                        "delete_role": False,
                        "change_role": False,
                        "get_roles": False,
                        "set_role": False,
                        "grab_role": False,
                        "check_role": False,
                    },
                },
                {
                    "role_name": "TestRoleName",
                    "comment": "TestComment",
                },
                {
                    "atatus": status.HTTP_403_FORBIDDEN,
                    "details": "Insufficient rights to use this function.",
                },
                does_not_raise()
        ),
    ]
)
@pytest.mark.asyncio
async def test_create_role(
        make_post_request,
        redis_read_data,
        execute_raw_sql,
        query_data_login,
        query_data_main,
        expected_answer,
        expectation,
):
    """Test create role."""
    url_login = test_settings.server_url + "/auth/login/"
    url_create_role = test_settings.server_url + "/auth/roles/create"
    with expectation:
        _response_login, _status_login, _cookies_login = await make_post_request(
            url_login, query_data_login
        )
        _response_create, _status_create, _cookies_create = await make_post_request(
            url_create_role, query_data_main, _cookies_login
        )
        assert expected_answer["status"] == _status_create
        assert expected_answer["details"] == _response_create


@pytest.mark.asyncio
async def test_update_role():
    assert 1==1


@pytest.mark.asyncio
async def test_delete_role():
    assert 1==1


@pytest.mark.asyncio
async def test_set_role():
    assert 1==1
