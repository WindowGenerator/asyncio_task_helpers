import logging
import sys

from asyncio import CancelledError, Future, Task, create_task, ensure_future, sleep
from functools import partial, wraps
from typing import Awaitable, Callable, Coroutine, Union


_logger = logging.getLogger(__name__)


async def cancel_and_stop_task(
    task: Union[Task, Future], reraise_exception: bool = True
) -> None:
    """
    Cancels the task and waits for it to complete.

    Args:
        task: asyncio.Task or asyncio.Future.

    Returns:
        None
    """
    task.cancel()

    try:
        await task

    except CancelledError:
        _logger.debug("The task was canceled")
        # WARN: DO NOT `raise' here because then the function will never end.

    except Exception as err:
        _logger.exception(f"The task was completed with an error ({err}):")

        if reraise_exception:
            raise

    else:
        _logger.debug("Task completed successfully")


def run_forever(
    repeat_delay: int = 0, failure_delay: int = None, reraise_exception: bool = True
) -> Callable[[Callable], Callable]:
    """
    A decorator that allows you to make the function for asyncio.Task repeatable, with a given time interval.

    Args:
        repeat_delay: Delay between calls, seconds.
        failure_delay: Delay between calls in case of a runtime error, seconds.
    """
    if failure_delay is None:
        failure_delay = repeat_delay

    def decorator(func: Callable[..., Coroutine]):
        @wraps(func)
        async def task_wrapper(*args, **kwargs):
            _logger.debug("Running an endless task")

            while True:
                try:
                    await func(*args, **kwargs)

                except CancelledError:
                    _logger.debug("Endless task canceled")
                    raise

                except Exception as err:
                    _logger.exception(
                        f"Unexpected error while running an infinite task ({err}):"
                    )
                    if reraise_exception:
                        raise

                    await sleep(failure_delay)

                else:
                    await sleep(repeat_delay)

        return task_wrapper

    return decorator


def _default_on_complete(name: str, future: Future, exit_on_error: bool = True) -> None:
    """
    Default handler on task completion

    Args:
        name: Task name that was completed
        future: Future after task completion
    """
    if future.cancelled():
        _logger.debug(f"Task {name} canceled")
        return

    error = future.exception()
    if error is not None:
        _logger.error(f"Unexpected error in task {name}:", exc_info=error)

        if exit_on_error:
            sys.exit(1)

    _logger.debug(f"Task {name} completed successfully")


def run_background_task(
    awaitable: Awaitable,
    name: str,
    on_complete: Callable[[str, Future], None] = _default_on_complete,
    exit_on_error: bool = True,
) -> Task:
    """
    A wrapper for running tasks in the background.

    Args:
        awaitable: task or coro
        name: name for logging
        on_complete: callback after task will comlpete

    Returns:
        Task
    """
    task = create_task(awaitable)
    task.add_done_callback(partial(on_complete, name, exit_on_error=exit_on_error))
    return task
