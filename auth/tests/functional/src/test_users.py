from contextlib import nullcontext as does_not_raise

import aiohttp
import pytest

from tests.functional.core.settings import test_settings
from fastapi import status


@pytest.mark.parametrize(
    "query_data, expected_answer, expectation",
    [
        (
            {
                "email": "christian_bale@practix.ru",
                "user_name": "first_practix_user",
                "first_name": "practix_default_name",
                "last_name": "practix_last_name",
                "phone_number": "78005553535",
                "hashed_password": "practix_password",
            },
            {"status": status.HTTP_201_CREATED},
            does_not_raise(),
        ),
        (
            {
                "email": "leonardo_dicaprio@practix.ru",
                "hashed_password": "practix_password",
            },
            {"status": status.HTTP_201_CREATED},
            does_not_raise(),
        ),
        (
            {
                "email": "ryan_gosling",
                "hashed_password": "practix_password",
            },
            {"status": status.HTTP_409_CONFLICT},
            pytest.raises(aiohttp.ClientResponseError),
        ),
        (
            {
                "email": "joseph_gordon_levitt@practix.ru",
                "hashed_password": "",
            },
            {"status": status.HTTP_201_CREATED},
            does_not_raise(),
        ),
        (
            {
                "email": "christian_bale@practix.ru",
                "user_name": "christian_bale",
                "first_name": "practix_default_name",
                "last_name": "practix_last_name",
                "phone_number": "78005553535",
                "hashed_password": "practix_password",
            },
            {"status": status.HTTP_409_CONFLICT},
            pytest.raises(aiohttp.ClientResponseError),
        ),
        (
            {
                "email": "christian_bale_fake@practix.ru",
                "user_name": "first_practix_user",
                "first_name": "practix_default_name",
                "last_name": "practix_last_name",
                "phone_number": "78005553535",
                "hashed_password": "practix_password",
            },
            {"status": status.HTTP_409_CONFLICT},
            pytest.raises(aiohttp.ClientResponseError),
        ),
    ],
)
@pytest.mark.asyncio
async def test_signup(
    make_post_request,
    execute_raw_sql,
    query_data,
    expected_answer,
    expectation,
):
    # TODO(MosyaginGrigorii): Подумать как чистить БД
    url = test_settings.service_url + "/auth/signup"
    with expectation:
        response, status, _ = await make_post_request(url, query_data)
        assert expected_answer["status"] == status
        assert query_data["email"] == response["email"]


@pytest.mark.parametrize(
    "query_data, expected_answer, expectation",
    [
        (
            {
                "email": "christian_bale@practix.ru",
                "hashed_password": "practix_password",
            },
            {"status": status.HTTP_200_OK},
            does_not_raise(),
        ),
        (
            {
                "email": "christian_bale@practix.ru",
                "hashed_password": "practix_password",
            },
            {"status": status.HTTP_200_OK},
            does_not_raise(),
        ),
        (
            {
                "email": "christian_bale@practix.ru",
                "hashed_password": "wrong_password",
            },
            {"status": status.HTTP_409_CONFLICT},
            pytest.raises(aiohttp.ClientResponseError),
        ),
        (
            {
                "email": "christian_bale",
                "hashed_password": "practix_password",
            },
            {"status": status.HTTP_409_CONFLICT},
            pytest.raises(aiohttp.ClientResponseError),
        ),
    ],
)
@pytest.mark.asyncio
async def test_login(
    make_post_request,
    redis_read_data,
    execute_raw_sql,
    query_data,
    expected_answer,
    expectation,
):
    url = test_settings.service_url + "/auth/login"
    key = "refresh_tokens"
    with expectation:
        response, status, cookies = await make_post_request(url, query_data)
        response_redis = await redis_read_data(key)
        response_redis = [
            refresh_token.decode("UTF-8") for refresh_token in response_redis
        ]
        is_exist = cookies["refresh_token"].value in response_redis
        assert expected_answer["status"] == status
        assert is_exist
