import datetime

def compute_urgency_score(due_date):
    """Higher score = more urgent."""
    if not due_date:
        return 0

    today = datetime.date.today()
    delta = (due_date - today).days

    if delta < 0:
        return 20  # overdue = max urgency

    if delta == 0:
        return 15  # due today

    return max(0, 10 - delta)  # gradual decay


def compute_effort_score(hours):
    """Low effort = higher score."""
    if hours is None:
        return 0

    if hours <= 1:
        return 10
    if hours <= 3:
        return 6
    if hours <= 6:
        return 3
    return 1


def compute_dependency_score(task, all_tasks):
    """Tasks that block others get priority."""
    count = sum([task["title"] in t.get("dependencies", []) for t in all_tasks])
    return count * 5  # each task blocked adds weight


def balanced_score(task, all_tasks):
    urgency = compute_urgency_score(task.get("due_date"))
    importance = task.get("importance", 5) * 2
    effort = compute_effort_score(task.get("estimated_hours"))
    deps = compute_dependency_score(task, all_tasks)

    score = urgency + importance + effort + deps

    explanation = (
        f"Urgency: {urgency}, Importance: {importance}, "
        f"Effort bonus: {effort}, Dependency weight: {deps}"
    )

    return score, explanation