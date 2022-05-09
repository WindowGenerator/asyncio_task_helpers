from asyncio import Task, sleep

import pytest

from asyncio_task_helpers import run_background_task
from tests.conftest import wrapper


@pytest.mark.asyncio
async def test_run_forever_simple(success_completion_task: Task) -> None:
    run_background_task(wrapper(success_completion_task), "Simple test")
    await sleep(0.5)


@pytest.mark.asyncio
async def test_run_background_task_with_exception(
    exception_completion_task: Task,
) -> None:
    run_background_task(
        wrapper(exception_completion_task), "Exception test", exit_on_error=False
    )
    await sleep(0.5)


@pytest.mark.asyncio
async def test_run_cancelled_background_task(already_cancelled_task: Task) -> None:
    run_background_task(wrapper(already_cancelled_task), "Cancelled test")
    await sleep(0.5)
