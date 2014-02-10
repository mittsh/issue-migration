from user import User
from migrate import PLATFORM_GH, PLATFORM_BB

#
# Comment
#

class IssueComment(object):
	'''
	An Comment inside an Issue
	'''

	def __init__(self, bb_comment = None, gh_comment = None):

		self.author = None
		self.body = None
		self.source = None
		self.source_comment_id = None

		if bb_comment:
			self.bb_load_comment(bb_comment)

	def bb_load_comment(self, bb_comment):
		'''
		Loads a comment from a Bitbucket response.
		'''

		# author
		self.author = User(bb_username=bb_comment['author_info']['username'])

		# body
		self.body = bb_comment['content']

		# source
		self.source = PLATFORM_BB

		# id
		self.source_comment_id = bb_comment['comment_id']

	def __unicode__(self):

		ISSUE_COMMENT_FORMAT = u'''Comment ID: {source_comment_id} ({source})
Author: {author}

{body}
'''
		return ISSUE_COMMENT_FORMAT.format(
			source_comment_id=self.source_comment_id,
			source=self.source,
			author=self.author.__unicode__(),
			body=self.body,
		)

	def format(self, to_platform=None):
		'''
		Formats the IssueComment body to adapt it to a platform.
		'''

		CONTENT_TEMPLATE = u'''{body}**Note**: This comment has been migrated from {source} (author: **{author}**)
'''

		return CONTENT_TEMPLATE.format(
			body='{body}\n\n\n'.format(body=self.body) if self.body else '',
			author=self.author.format(to_platform=to_platform),
			source=self.source,
		)
