###Install

Install dependencies with pip:

`pip install -r requirements.txt `

###Usage

####Get a Github Authentication Token

Run the following command - username needs write access on
the Github repo specified above.

```
curl -u 'username' -d '{"scopes":["repo"],"note":"Migration"}' \
	https://api.github.com/authorizations
```

Just replace `username` by your username, `repo` shouldn't be replaced.

###Todo

* Implement a CLI
* Implement to Bitbucket migration
* Do not transform Bitbucket priority and kind to labels
* Create specific colors for Github labels depending on priority

###Credits

Created from Gist: https://gist.github.com/nidico/3778347 by [@nidico](https://github.com/nidico)


###License

No license was specified by the original Gist, so it depends. My changes are released under the MIT License.
