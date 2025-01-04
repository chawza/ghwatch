from . import github
from .gui import TaskTrackerApp

def app():
    _app = TaskTrackerApp()
    _app.run()

    # for issue in user.get_issues(sort='-created'):

    #     if len(assigned_issues) <= 10:
    #         if issue.assignee == user:
    #             assigned_issues.append(issue)

    #     if count >= 100:
    #         break

    # pulls = []
    # for pr in user.get_pulls(sort='-created'):
    #     if len(pulls) <= 10:
    #         if pr.assignee == user:
    #             pulls.append(pr)
    #     if count >= 50:
    #         break



    # # print('assigned assues', len(assigned_issues))
    # # for issue in assigned_issues:
    # #     print(issue)

    # for pull in pulls:
    #     print(pull)