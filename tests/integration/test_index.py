import pytest

from odmantic.engine import AIOEngine, SyncEngine
from odmantic.field import Field
from odmantic.index import Index
from odmantic.model import Model
from odmantic.query import asc, desc

pytestmark = pytest.mark.asyncio


async def test_single_field_index_creation(aio_engine: AIOEngine):
    class M(Model):
        f: int = Field(index=True)

    await aio_engine.configure_database([M])

    info = await aio_engine.get_collection(M).index_information()
    assert (
        next(
            filter(lambda v: v["key"] == [("f", 1)], info.values()),
            None,
        )
        is not None
    )


async def test_sync_single_field_index_creation(sync_engine: SyncEngine):
    class M(Model):
        f: int = Field(index=True)

    sync_engine.configure_database([M])

    info = sync_engine.get_collection(M).index_information()
    assert (
        next(
            filter(lambda v: v["key"] == [("f", 1)], info.values()),
            None,
        )
        is not None
    )


async def test_single_field_index_creation_unique(aio_engine: AIOEngine):
    class M(Model):
        f: int = Field(unique=True)

    await aio_engine.configure_database([M])

    info = await aio_engine.get_collection(M).index_information()
    assert (
        next(
            filter(lambda v: v["key"] == [("f", 1)] and v["unique"], info.values()),
            None,
        )
        is not None
    )


async def test_sync_single_field_index_creation_unique(sync_engine: SyncEngine):
    class M(Model):
        f: int = Field(unique=True)

    sync_engine.configure_database([M])

    info = sync_engine.get_collection(M).index_information()
    assert (
        next(
            filter(lambda v: v["key"] == [("f", 1)] and v["unique"], info.values()),
            None,
        )
        is not None
    )


async def test_compound_index_with_name(aio_engine: AIOEngine):
    class M(Model):
        f: int
        g: int

        class Config:
            @staticmethod
            def indexes():
                yield Index(asc(M.f), desc(M.g), name="test")

    await aio_engine.configure_database([M])

    info = await aio_engine.get_collection(M).index_information()
    assert "test" in info
    assert info["test"]["key"] == [("f", 1), ("g", -1)]


async def test_sync_compound_index_with_name(sync_engine: SyncEngine):
    class M(Model):
        f: int
        g: int

        class Config:
            @staticmethod
            def indexes():
                yield Index(asc(M.f), desc(M.g), name="test")

    sync_engine.configure_database([M])

    info = sync_engine.get_collection(M).index_information()
    assert "test" in info
    assert info["test"]["key"] == [("f", 1), ("g", -1)]


async def test_multiple_indexes(aio_engine: AIOEngine):
    class M(Model):
        f: int = Field(index=True)
        g: int = Field(unique=True)

        class Config:
            @staticmethod
            def indexes():
                yield Index(asc(M.f), desc(M.g))

    await aio_engine.configure_database([M])

    info = await aio_engine.get_collection(M).index_information()
    assert (
        next(
            filter(lambda v: v["key"] == [("f", 1)], info.values()),
            None,
        )
        is not None
    )
    assert (
        next(
            filter(lambda v: v["key"] == [("g", 1)] and v["unique"], info.values()),
            None,
        )
        is not None
    )
    assert (
        next(
            filter(lambda v: v["key"] == [("f", 1), ("g", -1)], info.values()),
            None,
        )
        is not None
    )


async def test_sync_multiple_indexes(sync_engine: SyncEngine):
    class M(Model):
        f: int = Field(index=True)
        g: int = Field(unique=True)

        class Config:
            @staticmethod
            def indexes():
                yield Index(asc(M.f), desc(M.g))

    sync_engine.configure_database([M])

    info = sync_engine.get_collection(M).index_information()
    assert (
        next(
            filter(lambda v: v["key"] == [("f", 1)], info.values()),
            None,
        )
        is not None
    )
    assert (
        next(
            filter(lambda v: v["key"] == [("g", 1)] and v["unique"], info.values()),
            None,
        )
        is not None
    )
    assert (
        next(
            filter(lambda v: v["key"] == [("f", 1), ("g", -1)], info.values()),
            None,
        )
        is not None
    )
