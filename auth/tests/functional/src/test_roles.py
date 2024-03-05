import asyncio

import pytest


@pytest.mark.asyncio
async def test_role(pg_migrate):
    await asyncio.sleep(0.5)
    assert 1 == 1
