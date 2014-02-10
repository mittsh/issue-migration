# import PyGithub
from github import Github

def push_issue_to_github(issue):
	kwargs = {
		'title':issue.title,
	}

	if issue.body is not None:
		kwargs[u'body'] = issue.body

	if issue.assignee is not None:
		kwargs[u'assignee'] = get_gh_user(issue.assignee)

	kwargs[u'labels'] = map(get_gh_label, issue.labels)

	issue = gh_repo.create_issue(**kwargs)

	for comment in issue.comments:
		issue.create_comment(comment)

	if issue.closed:
		issue.edit(state=u'closed')

	print u'Created issue "%s" - %s' % (issue.title, issue.html_url)

	return issue
