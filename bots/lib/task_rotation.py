from datetime import datetime


def get_current_task(
    task_list, rotation_days=7, reference_datetime=datetime(2024, 1, 1)
):
    now = datetime.now()
    delta = now - reference_datetime
    weeks_since_start = delta.days // rotation_days

    task_index = weeks_since_start % len(task_list)
    return task_list[task_index]
