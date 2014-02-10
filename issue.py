# 
# Issue
# 

class Issue(object):
	'''
	Issue that can be imported from Github or Bitbucket and pushed to Github or
	Bitbucket.
	'''

	def __init__(self, bb_issue_and_comments = None, gh_issue = None):

		self.title = ''
		self.body = None
		self.reported_by = None
		self.assignee = None
		self.closed = False
		self.labels = set()
		self.comments = []

		if bb_issue_and_comments:
			(bb_issue, bb_comments,) = bb_issue_and_comments
			self.bb_load_issue(bb_issue)
			self.bb_load_comments(bb_comments)

	def bb_load_issue(self, bb_issue):
		'''
		Loads issue from a Bitbucket response.
		'''

		# status: new, open, resolved, on hold
		if bb_issue['status'] == u'resolved':
			self.closed = True
		
		# title
		self.title = bb_issue[u'title']

		# priority: trivial, minor, major, critical, blocker
		self.labels.add(u'priority-%s' % bb_issue[u'priority'])

		# metadata.kind: bug, enhancement, proposal, task
		self.labels.add(u'type-%s' % bb_issue[u'metadata'][u'kind'])
		
		# metadata.component
		if bb_issue[u'metadata'][u'component'] is not None:
			self.labels.add(u'component-%s' % bb_issue[u'metadata'][u'component'])
		
		# assignee
		if u'responsible' in bb_issue:
			self.assignee = USER_MAP[bb_issue[u'responsible'][u'username']]

		# reported_by
		if u'reported_by' in bb_issue:
			self.reported_by = bb_issue[u'reported_by'][u'username']

		self.body = bb_migration_issue_body(bb_issue)

	def bb_load_comments(self, bb_comments):
		'''
		Loads comments from a Bitbucket response.
		'''
		
		for bb_comment in bb_comments:
			if bb_comment[u'content'] is not None:
				body = bb_migration_comment_body(bb_comment)
				self.comments.append(body)

	def __unicode__(self):
		'''
		Returns formatted issue and comments.
		'''
		
		ISSUE_FORMAT = u'''Title: {title}
Reported By: {reported_by}
Assignee: {assignee}
Status: {status}
Labels: {labels}

{body}
{comments}
'''
		return ISSUE_FORMAT.format(
			title=self.title,
			reported_by=self.reported_by,
			assignee=self.assignee,
			status=u'Closed' if self.closed else u'Open',
			labels=u', '.join(self.labels),
			body=self.body,
			comments=u'\n\n'.join(self.comments)
		)

	def gh_create(self):

		kwargs = {}

		if self.body is not None:
			kwargs[u'body'] = self.body

		if self.assignee is not None:
			kwargs[u'assignee'] = get_gh_user(self.assignee)

		kwargs[u'labels'] = map(get_gh_label, self.labels)

		issue = gh_repo.create_issue(self.title, **kwargs)

		for comment in self.comments:
			issue.create_comment(comment)

		if self.closed:
			issue.edit(state=u'closed')

		print u'Created issue "%s" - %s' % (self.title, issue.html_url)

		return issue

# 
# Migration from Bitbucket
# 

def bb_format_author(bb_username):
	if bb_username is None:
		author = u'Anonymous'
	elif bb_username in USER_MAP:
		author = u'@%s' % USER_MAP[bb_username]
	else:
		author = u'[%s](https://bitbucket.org/%s)' % (2 * (bb_username,))
		
	return author

def bb_migration_issue_body(issue):

	CONTENT_TEMPLATE = u'''{content}


**Note**: This issue has been migrated from Bitbucket
Bitbucket issue ID: {bb_issue_id}
Created by **{author}** on {utc_created_on} last updated {utc_last_updated} status **{status}**
'''

	return CONTENT_TEMPLATE.format(
		content=issue['content'],
		author=bb_format_author(issue['reported_by']['username']),
		utc_created_on=issue['utc_created_on'],
		utc_last_updated=issue['utc_last_updated'],
		bb_issue_id=issue['local_id'],
		status=issue['status']
	)

def bb_migration_comment_body(comment):

	CONTENT_TEMPLATE = u'''{content}

**Note**: This comment has been migrated from Bitbucket (author: **{author}**)
'''

	return CONTENT_TEMPLATE.format(
		content=comment['content'],
		author=bb_format_author(comment['author_info']['username']),
	)
