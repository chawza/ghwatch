import os
from textual.app import App
from textual.widgets import Static, Input, Header, ListView, ListItem
from textual.screen import Screen
from textual import events

from github.Issue import Issue
from github import Github
from github.GithubException import BadCredentialsException

from .import github

class BaseScreen(Screen):
    app: 'GHWatchApp'

class WelcomeScreen(BaseScreen):

    def compose(self):
        yield Static("Enter Github Userrname")
        yield Input(id="token_input", type='text')
        yield Static(id='error_message')

    def on_key(self, event: events.Key) -> None:
        if event.key == "enter":
            token = self.query_one("#token_input").value

            if token:
                self.check_login(token)

    def on_mount(self):
        if token := os.environ.get('GITHUB_TOKEN'):
            self.check_login(token)


    # hnadlers
    def check_login(self, token: str):

        client = github.get_github_client(token)
        user = client.get_user()

        error_widget: Static = self.query_one('#error_message')
        error_widget.update('')

        try:
            user.login
        except BadCredentialsException:
            error_widget.update('Invalid username or token')
            return
        
        self.app.client = client
        self.app.pop_screen()        
        self.app.push_screen(HomeScreen())


class SelectRepoScreen(BaseScreen):
    def compose(self):
        yield Header("Select a repository")
        # TODO: list repositories and allow selection


class SelectIssueScreen(BaseScreen):
    def __init__(self, repo: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.repo = repo

    def compose(self):
        yield Header("Select Issue for repo {}".format(self.repo))


class HomeScreen(BaseScreen):

    class IssueItem(ListItem):
        def __init__(self, issue: Issue, *args, **kwargs):
            self.issue = issue
            super().__init__(*args, **kwargs)

        def compose(self):
            yield Static(f'#{self.issue.number} - {self.issue.title}')

    def compose(self):
        yield Static(f'[{self.app.user.name}]')
        yield ListView(id='issue_list')
        yield Static(id='bottom_message')

    def on_mount(self):
        message = self.query_one('#bottom_message')
        message.update('Fetching...')

        list_view: ListView = self.query_one('#issue_list')
        list_view.clear()
        items = [self.IssueItem(issue) for issue in self.get_latest_issues()]

        if len(items) == 0:
            message.update('No issues found')
            return

        list_view.clear()
        list_view.extend(items)

        message.update('')

    def get_latest_issues(self, num_issues=10):
        return list(self.app.user.get_issues(sort='-created')[:num_issues])


class GHWatchApp(App):
    client: Github

    def on_mount(self):
        self.push_screen(WelcomeScreen())


    @property
    def user(self):
        return self.client.get_user()


