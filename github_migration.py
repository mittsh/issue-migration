# import PyGithub
from github import Github

# import log levels
from migrate import LOG_LEVEL_SILENT, LOG_LEVEL_ERRORS, LOG_LEVEL_WARN, LOG_LEVEL_INFO, LOG_LEVEL_DEBUG

# platforms
from migrate import PLATFORM_GH

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

		# Log
		if log_level >= LOG_LEVEL_DEBUG:
			print(u'Pushing issue ({title}) to Github...'.format(title=issue.title))

		# Making args
		kwargs = {
			'title':issue.title,
		}

		if issue.body is not None:
			kwargs['body'] = issue.format(to_platform=PLATFORM_GH)

		if issue.assignee is not None:
			kwargs['assignee'] = self.get_user(issue.assignee.gh_username)

		kwargs['labels'] = map(lambda label: self.get_label(label), issue.labels)

		# Push issue
		gh_issue = self.gh_repo.create_issue(**kwargs)

		# Log
		if log_level >= LOG_LEVEL_INFO:
			print(u'..Pushed issue to Github: #{number} {title}'.format(number=gh_issue.number, title=gh_issue.title))

		# Push comments
		for comment in issue.comments:
			self.push_comment_to_github(gh_issue, comment, log_level=log_level)

		# Close issue
		if issue.closed:

			# Close
			gh_issue.edit(state=u'closed')

			# Log
			if log_level >= LOG_LEVEL_DEBUG:
				print(u'..Closed issue')

		# Log
		if log_level >= LOG_LEVEL_DEBUG:
			print(u'..Finished to push issue and its comments to Github: #{number} {title}'.format(number=gh_issue.number, title=gh_issue.title))
		elif log_level >= LOG_LEVEL_INFO:
			print(u'Pushed issue and its comments to Github: #{number} {title}'.format(number=gh_issue.number, title=gh_issue.title))

	def push_comment_to_github(self, gh_issue, comment, log_level=LOG_LEVEL_ERRORS):
		'''
		Creates a new comment on Github from an IssueComment object
		'''
		
		# Push
		gh_comment = gh_issue.create_comment(body=comment.format(to_platform=PLATFORM_GH))

		# Log
		if log_level >= LOG_LEVEL_DEBUG:
			print(u'..Pushed comment ({id}) to Github...'.format(id=gh_comment.id))

	def push_issues_to_github(self, issues, log_level=LOG_LEVEL_ERRORS):
		'''
		Creates new issues on Github from a list Issue objects.
		'''

		for issue in issues:
			self.push_issue_to_github(issue, log_level=log_level)
