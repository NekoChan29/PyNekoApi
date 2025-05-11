import pytest

from pynekoapi import AsyncNekoApi, SyncNekoApi


@pytest.fixture
def api_sync():
    return SyncNekoApi()


@pytest.fixture
async def api_async():
    return AsyncNekoApi()


def test_get_bin_sync(api_sync):
    key = "example_key"
    result = api_sync.get_bin(key)
    assert isinstance(result, dict)


def test_save_bin_sync(api_sync):
    content = "Hello, World!"
    result = api_sync.save_bin(content)
    assert isinstance(result, dict)


def test_register_date_sync(api_sync):
    user_id = 5050907047
    result = api_sync.register_date(user_id)
    assert isinstance(result, dict)


def test_register_date_with_timezone_sync(api_sync):
    user_id = 5050907047
    timezone = "Asia/Jakarta"
    result = api_sync.register_date(user_id, timezone)
    assert isinstance(result, dict)


@pytest.mark.asyncio
async def test_get_bin_async(api_async):
    key = "example_key"
    result = await api_async.get_bin(key)
    assert isinstance(result, dict)


@pytest.mark.asyncio
async def test_save_bin_async(api_async):
    content = "Hello, World!"
    result = await api_async.save_bin(content)
    assert isinstance(result, dict)


@pytest.mark.asyncio
async def test_register_date_async(api_async):
    user_id = 5050907047
    result = await api_async.register_date(user_id)
    assert isinstance(result, dict)


@pytest.mark.asyncio
async def test_register_date_with_timezone_async(api_async):
    user_id = 5050907047
    timezone = "Asia/Jakarta"
    result = await api_async.register_date(user_id, timezone)
    assert isinstance(result, dict)
