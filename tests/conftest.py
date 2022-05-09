from asyncio import CancelledError, Task, create_task, sleep

import pytest_asyncio


async def wrapper(task: Task) -> None:
    await task


@pytest_asyncio.fixture
async def success_completion_task() -> Task:
    async def inner() -> None:
        await sleep(1)

    task = create_task(inner())

    yield task

    if not task.cancelled():
        try:
            task.cancel()
            await task
        except CancelledError:
            pass


@pytest_asyncio.fixture
async def already_done_task() -> Task:
    async def inner() -> None:
        pass

    task = create_task(inner())

    await sleep(0.1)

    return task


@pytest_asyncio.fixture
async def already_cancelled_task() -> Task:
    async def inner() -> None:
        pass

    task = create_task(inner())

    try:
        task.cancel()
        await task
    except CancelledError:
        pass

    return task


@pytest_asyncio.fixture
async def exception_completion_task() -> Task:
    async def inner() -> None:
        raise Exception("я умир")

    task = create_task(inner())

    return task
