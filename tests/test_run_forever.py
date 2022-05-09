from asyncio import CancelledError, Task, create_task, sleep

import pytest

from asyncio_task_helpers import run_forever
from tests.conftest import wrapper


@pytest.mark.asyncio
async def test_run_forever_simple(success_completion_task: Task) -> None:
    t = run_forever()(wrapper)(success_completion_task)
    create_task(t)
    await sleep(0.5)


@pytest.mark.asyncio
async def test_run_forever_with_exception(exception_completion_task: Task) -> None:
    t = run_forever()(wrapper)(exception_completion_task)
    with pytest.raises(Exception):
        await create_task(t)


@pytest.mark.asyncio
async def test_run_forever_with_exception_without_reraise(
    exception_completion_task: Task,
) -> None:
    t = run_forever(reraise_exception=False)(wrapper)(exception_completion_task)
    create_task(t)
    await sleep(0.5)


@pytest.mark.asyncio
async def test_run_forever_cancelled_task(already_cancelled_task: Task) -> None:
    t = run_forever()(wrapper)(already_cancelled_task)
    with pytest.raises(CancelledError):
        await create_task(t)
