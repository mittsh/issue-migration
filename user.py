from config import USER_MAP
from migrate import PLATFORM_GH, PLATFORM_BB

#
# User
#

class User(object):
	'''
	A User, can be a Github or Bitbucket user, or none
	'''

	def __init__(self, bb_username = None, gh_username = None):

		self.bb_username = None
		self.gh_username = None
		self.common_name = 'Anonymous'
		self.source = None

		# Github username is passed
		if gh_username:
			self.source = PLATFORM_GH
			self.common_name = gh_username
			self.gh_username = gh_username
			for bb_u, gh_u in USER_MAP.iteritems():
				if gh_u == gh_username:
					self.bb_username = bb_username
					break

		# Bitbucket username is passed
		elif bb_username:
			self.source = PLATFORM_BB
			self.common_name = bb_username
			self.bb_username = bb_username
			self.gh_username = USER_MAP.get(bb_username)

	def __unicode__(self):
		return self.format()

	def format(self, to_platform = None):
		
		# To Github
		if to_platform == PLATFORM_GH:
			if self.gh_username:
				return u'@{username}'.format(username=self.gh_username)
			elif self.bb_username:
				return u'[{username} (Bitbucket)](https://bitbucket.org/{username})'.format(username=self.bb_username)
			else:
				return self.common_name
		
		# To Bitbucket
		elif to_platform == PLATFORM_BB:
			if self.bb_username:
				return u'[@{username}](https://bitbucket.org/{username})'.format(username=self.bb_username)
			elif self.gh_username:
				return u'[{username} (Github)](https://github.com/{username})'.format(username=self.gh_username)
			else:
				return self.common_name
		
		# Generic
		else:
			if self.source == PLATFORM_GH and self.gh_username:
				return u'{0} (Github)'.format(self.gh_username)
			elif self.source == PLATFORM_BB and self.bb_username:
				return u'{0} (Bitbucket)'.format(self.bb_username)
			else:
				return self.common_name
