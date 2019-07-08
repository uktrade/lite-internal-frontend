def get_assigned_users_from_cases(case_ids: list, case_assignments: list) -> list:
    """
    Return a list of users if the case they're in belongs to the list of cases given in case_ids
    """
    assigned_users = []

    for assignment in (x for x in case_assignments if x['case'] in case_ids):
        assigned_users.extend(assignment['users'])

    return assigned_users
