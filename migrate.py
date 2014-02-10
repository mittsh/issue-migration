#!/usr/bin/env python

LOG_LEVEL_SILENT = 0
LOG_LEVEL_ERRORS = 1
LOG_LEVEL_WARN = 2
LOG_LEVEL_INFO = 2
LOG_LEVEL_DEBUG = 3

def get_gh_user(username):
	if username not in _gh_users:
		_gh_users[username] = gh.get_user(username)
	return _gh_users[username]



# gh_repo = get_gh_user(GH_USER).get_repo(GH_REPO)

# _gh_repo_labels = dict([(l.name, l) for l in list(gh_repo.get_labels())])


def get_gh_label(label):
	if label not in _gh_repo_labels:
		_gh_repo_labels[label] = gh_repo.create_label(label, '444444')
	return _gh_repo_labels[label]


if __name__ == '__main__':

	import getpass
	import config
	
	from bitbucket_migration import get_issues_from_bitbucket

	from_user = (not config.INPUT and config.BB_USER) or raw_input(u'[From] Bitbucket Username ({0}): '.format(config.BB_USER)) or config.BB_USER
	from_password = getpass.getpass(u'[From] Bitbucket Password (protected, leave empty for none): ')
	from_repo = (not config.INPUT and config.BB_REPO) or raw_input(u'[From] Bitbucket Repo ({0}): '.format(config.BB_REPO)) or config.BB_REPO

	to_user = (not config.INPUT and config.GH_USER) or raw_input(u'[To] Github Username ({0}): '.format(config.GH_USER)) or config.GH_USER
	to_repo = (not config.INPUT and config.GH_REPO) or raw_input(u'[To] Github Repo ({0}): '.format(config.GH_REPO)) or config.GH_REPO

	issues = get_issues_from_bitbucket(from_user=from_user, from_repo=from_repo, from_password=from_password, log_level = LOG_LEVEL_INFO)
	