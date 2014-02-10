# import bitbucket-api
from bitbucket.bitbucket import Bitbucket

# import our Issue class
from issue import Issue

# import log levels
from migrate import LOG_LEVEL_SILENT, LOG_LEVEL_ERRORS, LOG_LEVEL_WARN, LOG_LEVEL_INFO, LOG_LEVEL_DEBUG

def fetch_issues_from_bitbucket(from_user, from_repo, from_password=None, log_level=LOG_LEVEL_ERRORS, fetch_limit=50, stop_at_index=None, start=0):
	'''
	Loads all issues form a Bitbucket repository, and returns a list of Issue objects.
	'''

	# Issues
	issues = []

	# Connect to the Bitbucket repo
	bb = Bitbucket(username=from_user, password=from_password or '', repo_name_or_slug=from_repo)
	success, bb_repo = bb.repository.get()

	# If error, raise
	if not success:
		if log_level >= LOG_LEVEL_ERRORS:
			print(u'Can\' connect to Bitbucket: {0}'.format(bb_repo))
		raise Exception(u'Can\' connect to Bitbucket: {0}'.format(bb_repo))

	# Log
	if log_level >= LOG_LEVEL_INFO:
		print(u'Connected to Bitbucket Repository: {owner}/{slug} ({name})'.format(owner=bb_repo.get('owner'), slug=bb_repo.get('slug'), name=bb_repo.get('name')))

	# Iterate until we fetch all the issues
	while True:

		# Load issues
		success, bb_all_issues = bb.issue.all(params={'sort':'local_id', 'start':str(start), 'limit':str(fetch_limit)})

		# If error, raise
		if not success:
			if log_level >= LOG_LEVEL_ERRORS:
				print(u'Can\'t fetch issues from Bitbucket: {0}'.format(bb_all_issues))
			raise Exception(u'Can\'t fetch issues from Bitbucket: {0}'.format(bb_all_issues))

		# Log
		if log_level >= LOG_LEVEL_DEBUG:
			print(u'Fetched {count} (total: {total}) issues from Bitbucket: {issues}'.format(
				count=len(bb_all_issues['issues']),
				total=bb_all_issues['count'],
				issues=' '.join('#{id}'.format(id=bb_issue['local_id']) for bb_issue in bb_all_issues['issues']),
			))

		# Iterate on issues
		for bb_issue in bb_all_issues['issues']:

			# try/catch to show the issue ID if fails
			try:
				# Load comments
				success, bb_comments = bb.issue.comment.all(issue_id=bb_issue['local_id'])

				# Create Issue
				issue = Issue(bb_issue_and_comments = (bb_issue, bb_comments,))

				# Append issue
				issues.append(issue)

				# Log
				if log_level >= LOG_LEVEL_DEBUG:
					print(issue.__unicode__())
				elif log_level >= LOG_LEVEL_INFO:
					print('Issue ID {id}: {title} ({count} comment(s))'.format(id=bb_issue['local_id'], title=issue.title, count=len(issue.comments)))

			except Exception, e:
				print(u'Cannot create issue ID: {0}'.format(bb_issue.get('local_id')))
				raise

		# Increment start
		start += len(bb_all_issues['issues'])

		# Break when all is loaded
		if start >= bb_all_issues['count'] or (stop_at_index and start >= stop_at_index):
			break
	
	return issues
