import asyncio
import importlib
import logging
from typing import Callable, List, Tuple

import schedule


def add_new_schedule(
    interval: str, time_str: str, task_func: Callable, asyncio_function=asyncio.run, *_
) -> None:
    """Uses the module Schedule to programatically create repeatable tasks

    Args:
        interval : str
            The interval of time when fuction will be called, it must adhere to Schedule's intervals
            https://schedule.readthedocs.io/en/stable/reference.html#schedule.Job
        time_str : str
            Time pattern *when* the func will be called, formats should be:
            "%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d", "%H:%M:%S", "%H:%M"
        task_func : str
            The function that is going to be called in passed interval
    """
    if "second" in interval or "minute" in interval:
        logging.debug(
            f"Added new schedule task: {interval} every {time_str} - {task_func.__name__}"
        )
        scheduler = getattr(schedule.every(int(time_str)), interval)
        scheduler.do(lambda: asyncio_function(task_func()))
    else:
        logging.debug(
            f"Added new schedule task: {interval} at {time_str} - {task_func.__name__}"
        )
        scheduler = getattr(schedule.every(), interval)
        scheduler.at(time_str).do(lambda: asyncio_function(task_func()))


def get_module_scheduler_data(module_name: str) -> List[Tuple[str, str, Callable]]:
    """Programatically get data from `schedules.py` for the provided protocol name

    Args:
        module_name : str
            The module name that contains the schedules

    Returns:
        list
            A list following the format [<interval>, <time>, <func>]

    """
    try:
        scheduler_module = importlib.import_module(f"{module_name}.schedules")
        schedule = getattr(scheduler_module, f"SCHEDULE")
        logging.debug(f"Loaded schedules for {module_name}")
        return schedule
    except AttributeError:
        raise NotImplementedError(f"Schedules not created for {module_name}.")


def schedule_module(module_name: str):
    try:
        schedules_data = get_module_scheduler_data(module_name)
    except AttributeError:
        raise NotImplementedError(f"Schedules not created for {module_name}.")

    for schedule_info in schedules_data:
        add_new_schedule(*schedule_info)
