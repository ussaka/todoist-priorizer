from todoist_api_python.api import TodoistAPI
import keyring
import configparser
import logging
import datetime
import sys
from time import sleep
from CommandLineParser import CommandLineParser


def get_tasks(filters: str) -> list:
    """!
    Get filtered tasks from the Todoist API

    @param filters The filters to apply to the tasks

    @return The list of tasks from the Todoist API
    """
    tasks = []
    try:
        tasks = api.get_tasks(filter=filters)
    except Exception as error:
        logging.error(error)
        sys.exit(1)
    logging.debug(f"({filters}) filtered tasks:\n{tasks}\n")
    return tasks


def sort_tasks_date(tasks: list) -> list:
    """!
    Sort the tasks by date, oldest to newest

    @param tasks The list of tasks to sort

    @return The sorted list of tasks, oldest to newest
    """
    tasks.sort(key=lambda x: x.created_at)
    logging.debug(f"Sorted tasks:\n{tasks}\n")
    return tasks


def prioritize_tasks(tasks: list, p: int, max_size: int) -> list:
    """!
    Prioritize the tasks

    @param tasks The list of tasks to prioritize
    @param p The priority to set, 1-4, 4 being the highest priority
    @param max_size The maximum number of tasks to prioritize

    @return The list of tasks with the new priority
    """
    for i in range(0, max_size):
        try:
            is_success = api.update_task(task_id=tasks[i].id, priority=p)
            logging.info(f"Priority changed:\n{is_success}\n")
        except Exception as error:
            logging.error(error)
            sys.exit(1)
    logging.debug(f"Prioritized tasks:\n{tasks}\n")
    return tasks


if __name__ == "__main__":
    # Create the command line parser
    cmd = CommandLineParser()

    # Create the config parser
    config = configparser.ConfigParser()
    config.read("config.ini")

    # API token must be set
    try:
        if keyring.get_password("system", "todoist-api-token") is None:
            raise Exception("No API token provided")
    except Exception as error:
        logging.error(error)

    # Create the TodoistAPI object
    api = TodoistAPI(keyring.get_password("system", "todoist-api-token"))

    run_hour = int(config.get("USER", "run_hour"))
    run_minute = int(config.get("USER", "run_minute"))
    while True:
        current_time = datetime.datetime.now().time()
        run_time = datetime.time(run_hour, run_minute)
        if (
            current_time.hour == run_time.hour
            and current_time.minute == run_time.minute
        ):
            # Prioritize the tasks
            p1_tasks = get_tasks("P1")
            p2_tasks = get_tasks("P2")
            p2_tasks = sort_tasks_date(p2_tasks)
            tasks_size = len(p1_tasks)
            tasks_target_size = int(config.get("USER", "p1_tasks"))
            if tasks_size < tasks_target_size:
                logging.info(f"You have {tasks_size}/{tasks_target_size} P1 tasks")
                prioritize_tasks(p2_tasks, 4, tasks_target_size - tasks_size)

            p2_tasks = get_tasks("P2")
            p3_tasks = get_tasks("P3")
            p3_tasks = sort_tasks_date(p3_tasks)
            tasks_size = len(p2_tasks)
            tasks_target_size = int(config.get("USER", "p2_tasks"))
            if tasks_size < tasks_target_size:
                logging.info(f"You have {tasks_size}/{tasks_target_size} P2 tasks")
                prioritize_tasks(p3_tasks, 3, tasks_target_size - tasks_size)

            p3_tasks = get_tasks("P3")
            p4_tasks = get_tasks("P4")
            p4_tasks = sort_tasks_date(p4_tasks)
            tasks_size = len(p3_tasks)
            tasks_target_size = int(config.get("USER", "p3_tasks"))
            if tasks_size < tasks_target_size:
                logging.info(f"You have {tasks_size}/{tasks_target_size} P3 tasks")
                prioritize_tasks(p4_tasks, 2, tasks_target_size - tasks_size)

            sleep(60)  # Run only once
        else:
            sleep(60)
