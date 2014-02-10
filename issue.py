from user import User
from comment import IssueComment
from migrate import PLATFORM_GH, PLATFORM_BB

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
		self.comments = [] # a list of IssueComment objects
		self.source = None # source of the Issue (Github or Bitbucket)
		self.source_issue_id = None # issue id at the source
		self.created_on = None
		self.updated_on = None

		# Bitbucket Payload
		self.bb_issue = None

		# If Bitbucket payload is passed
		if bb_issue_and_comments:
			(bb_issue, bb_comments,) = bb_issue_and_comments
			self.bb_load_issue(bb_issue)
			self.bb_load_comments(bb_comments)

	def bb_load_issue(self, bb_issue):
		'''
		Loads issue from a Bitbucket response.
		'''

		# save bitbucket payload
		self.bb_issue = bb_issue

		# source
		self.source = PLATFORM_BB

		# source issue id
		self.source_issue_id = bb_issue['local_id']

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
			self.assignee = User(bb_username=bb_issue[u'responsible'][u'username'])

		# reported_by
		if u'reported_by' in bb_issue:
			self.reported_by = User(bb_username=bb_issue[u'reported_by'][u'username'])

		# created_on
		self.created_on = bb_issue['utc_created_on']

		# updated_on
		self.updated_on = bb_issue['utc_last_updated']

		# body
		self.body = bb_issue['content']

	def bb_load_comments(self, bb_comments):
		'''
		Loads comments from a Bitbucket response.
		'''

		for bb_comment in bb_comments:
			if bb_comment[u'content'] is not None:
				comment = IssueComment(bb_comment=bb_comment)
				self.comments.append(comment)

	def format(self, to_platform=None):
		'''
		Formats the Issue body to adapt it to a platform.
		'''

		CONTENT_TEMPLATE = u'''{body}**Note**: This issue has been migrated from {source} (ID: {source_issue_id}){assignee}
Created by **{author}** on {created_on}{updated_on}{status}
'''

		kwargs={
			'body': '{body}\n\n\n'.format(content=self.body) if self.body else '',
			'source': self.source,
			'author':self.reported_by.format(to_platform=to_platform),
			'created_on': self.created_on,
			'updated_on': '',
			'source_issue_id': self.source_issue_id,
			'status': '',
			'assignee': '',
		}
		
		if self.updated_on != self.created_on:
			kwargs['updated_on'] = u'\nLast updated on {updated_on}'.format(updated_on=self.updated_on)

		if self.assignee:
			kwargs['assignee'] = u'\nAssigned to **{assignee}**'.format(assignee=self.assignee.format(to_platform=to_platform))

		if self.source == PLATFORM_BB:
			kwargs['status'] = u'\nStatus **{status}**'.format(status=self.bb_issue['status'])

		return CONTENT_TEMPLATE.format(**kwargs)


	def __unicode__(self):

		ISSUE_FORMAT = u'''Issue ID: {source_issue_id} ({source})
Title: {title}
Reported By: {reported_by}
Assignee: {assignee}
Status: {status}
Labels: {labels}

{body}
{comments}
'''
		return ISSUE_FORMAT.format(
			source_issue_id=self.source_issue_id,
			source=self.source,
			title=self.title,
			reported_by=self.reported_by.__unicode__() if self.reported_by else u'None',
			assignee=self.assignee.__unicode__() if self.assignee else u'None',
			status=u'Closed' if self.closed else u'Open',
			labels=u', '.join(self.labels),
			body=self.body,
			comments=u'\n\n'.join([comment.__unicode__() for comment in self.comments]),
		)
