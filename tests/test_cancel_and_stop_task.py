from asyncio import Task

import pytest

from asyncio_task_helpers import cancel_and_stop_task


@pytest.mark.asyncio
async def test_cancel_simple(success_completion_task: Task) -> None:
    await cancel_and_stop_task(success_completion_task)


@pytest.mark.asyncio
async def test_cancel_already_cancelled_task(already_cancelled_task: Task) -> None:
    await cancel_and_stop_task(already_cancelled_task)


@pytest.mark.asyncio
async def test_cancel_task_with_exception(exception_completion_task: Task) -> None:
    with pytest.raises(Exception):
        await cancel_and_stop_task(exception_completion_task)


@pytest.mark.asyncio
async def test_cancel_task_with_reraise_flag(exception_completion_task: Task) -> None:
    await cancel_and_stop_task(exception_completion_task, reraise_exception=False)


@pytest.mark.asyncio
async def test_cancel_done_task(already_done_task: Task) -> None:
    await cancel_and_stop_task(already_done_task, reraise_exception=True)
