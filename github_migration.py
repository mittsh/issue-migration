# import PyGithub
from github import Github

# import log levels
from migrate import LOG_LEVEL_SILENT, LOG_LEVEL_ERRORS, LOG_LEVEL_WARN, LOG_LEVEL_INFO, LOG_LEVEL_DEBUG

# platforms
from migrate import PLATFORM_GH, PLATFORM_BB

class GithubMigration(object):

	def __init__(self, username, repo, access_token):

		# Create caches
		self.gh_users={}
		self.gh_labels={}

		# Creates the Github Connection
		self.gh=Github(login_or_token=access_token)

		# Get the Repo
		self.gh_repo=self.get_user(username).get_repo(repo)

		# Get the Repo Labels
		self.gh_repo_labels = dict([(l.name, l) for l in list(self.gh_repo.get_labels())])

	def get_user(self, username):
		if username not in self.gh_users:
			self.gh_users[username] = self.gh.get_user(username)
		return self.gh_users[username]

	def get_label(self, label, color='444444'):
		if label not in self.gh_repo_labels:
			self.gh_repo_labels[label] = self.gh_repo.create_label(label, color)
		return self.gh_repo_labels[label]

	def push_issue_to_github(self, issue, log_level=LOG_LEVEL_ERRORS):
		'''
		Creates a new issue on Github from a Issue object.
		'''

		kwargs = {
			'title':issue.title,
		}

		if issue.body is not None:
			kwargs[u'body'] = issue.format(to_platform=PLATFORM_GH)

		if issue.assignee is not None:
			kwargs[u'assignee'] = self.get_user(issue.assignee.gh_username)

		kwargs[u'labels'] = map(lambda label: self.get_label(label), issue.labels)

		issue = self.gh_repo.create_issue(**kwargs)

		for comment in issue.comments:
			issue.create_comment(comment)

		if issue.closed:
			issue.edit(state=u'closed')

		print u'Created issue "%s" - %s' % (issue.title, issue.html_url)

		return issue

	def push_issues_to_github(self, issues, log_level=LOG_LEVEL_ERRORS):
		'''
		Creates new issues on Github from a list Issue objects.
		'''

		for issue in issues:
			self.push_issue_to_github(issue, log_level=log_level)
