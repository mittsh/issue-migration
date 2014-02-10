#!/usr/bin/env python

# Log Level
LOG_LEVEL_SILENT = 0
LOG_LEVEL_ERRORS = 1
LOG_LEVEL_WARN = 2
LOG_LEVEL_INFO = 2
LOG_LEVEL_DEBUG = 3

# Platform
PLATFORM_GH = 'Github'
PLATFORM_BB = 'Bitbucket'

if __name__ == '__main__':

	import getpass
	import config

	from bitbucket_migration import fetch_issues_from_bitbucket
	from github_migration import GithubMigration

	from_user = (not config.INPUT and config.BB_USER) or raw_input(u'[From] Bitbucket Username ({0}): '.format(config.BB_USER)) or config.BB_USER
	from_password = getpass.getpass(u'[From] Bitbucket Password (protected, leave empty for none): ')
	from_repo = (not config.INPUT and config.BB_REPO) or raw_input(u'[From] Bitbucket Repo ({0}): '.format(config.BB_REPO)) or config.BB_REPO

	to_user = (not config.INPUT and config.GH_USER) or raw_input(u'[To] Github Username ({0}): '.format(config.GH_USER)) or config.GH_USER
	to_repo = (not config.INPUT and config.GH_REPO) or raw_input(u'[To] Github Repo ({0}): '.format(config.GH_REPO)) or config.GH_REPO

	issues = fetch_issues_from_bitbucket(from_user=from_user, from_repo=from_repo, from_password=from_password, log_level=LOG_LEVEL_INFO, fetch_limit=1, stop_at_index = 1)
	
	print(u'\n==========\n\n\n'.join([issue.format(to_platform=PLATFORM_GH) + 'Comments:\n' + '\n----------\n'.join([comment.format(to_platform=PLATFORM_GH) for comment in issue.comments]) for issue in issues]))
	
	gh_migration = GithubMigration(username=to_user, repo=to_repo, access_token=config.GH_TOKEN)
	gh_migration.push_issues_to_github(issues)
