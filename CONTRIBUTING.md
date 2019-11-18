# Contributing

When contributing to this repository, please first discuss the change you wish to make via issue,
email, or any other method with the owners of this repository before making a change. Or at

Please note we have a code of conduct, please follow it in all your interactions with the project.

 - [Feature Requests](#feature)
 - [Issues and Bugs](#issue)
 - [Submission Guidelines](#submit)
 - [Coding Rules](#rules)
 - [Git Commit Guidelines](#commit)

## <a name="feature"></a> Feature Requests
You can request a new feature by submitting a ticket to our [Github issues](https://github.com/Roche/gitlab-configuration-as-code/issues/new).
If you would like to implement a new feature then open up a ticket, explain your change in the description 
and you can propose a Pull Request straight away.

Before raising a new feature requests, you can [browse existing requests](https://github.com/Roche/gitlab-configuration-as-code/issues) 
to save us time removing duplicates.

## <a name="issue"></a> Issues and Bugs
If you find a bug in the source code or a mistake in the documentation, you can help us by [
submitting a ticket](https://github.com/Roche/gitlab-configuration-as-code/issues/new).
**Even better**, if you could submit a Pull Request to our repo fixing the issue. 

**Please see the Submission Guidelines below**.

## <a name="submit"></a> Submission Guidelines

### [Submitting an Issue](https://opensource.guide/how-to-contribute/#opening-an-issue)
Before you submit your issue search the [backlog](https://github.com/Roche/gitlab-configuration-as-code/issues), 
maybe your question was already answered or is already there in backlog.

Providing the following information will increase the chances of your issue being dealt with quickly:

* **Overview of the issue** - if an error is being thrown a stack trace helps
* **Motivation for or Use Case** - explain why this is a feature or bug for you
* **Reproduce the error** - if reporting a bug, provide an unambiguous set of steps to reproduce the error. 
* **Related issues** - has a similar issue been reported before?
* **Suggest a Fix** - if you can't fix the bug yourself, perhaps you can point to what might be causing 
the problem (line of code or commit or general idea)

### [Submitting a Pull Request](https://opensource.guide/how-to-contribute/#opening-a-pull-request)
Before you submit your pull request consider the following guidelines:

* Search [Github](https://github.com/Roche/gitlab-configuration-as-code/pulls) for an open or closed Pull Request
  that relates to your submission.
* Fork the repository
* Make your changes in a new git branch

     ```shell
     git checkout -b my-branch master
     ```

* Create your patch, **including appropriate test cases**. 
* Follow our [Coding Rules](#rules).
* Ensure that our coding style check passes:

     ```shell
     make lint
     ```

* Ensure that all tests pass

     ```shell
     make test
     ```

* Commit your changes using a descriptive commit message that follows our
  [commit message conventions](#commit-message-format).

     ```shell
     git commit -a
     ```

  _Note:_ the optional commit `-a` command line option will automatically "add" and "rm" edited files.

* Push your branch:

    ```shell
    git push origin my-branch
    ```

* In Github, [send a pull request](https://github.com/Roche/gitlab-configuration-as-code/compare) 
from your fork to our `master` branch
* There will be default reviewers added.
* If any changes are suggested then
  * Make the required updates.
  * Re-run tests ensure tests are still passing

That's it! Thank you for your contribution!

## <a name="rules"></a> Coding Rules
We use black as code formatter, so you'll need to format your changes using 
the [black code formatter](https://github.com/python/black).

Just run:
```bash
cd python-gitlab/
pip3 install --user tox
tox -e black
```
to format your code according to our guidelines ([tox](https://tox.readthedocs.io/en/latest/) is required).

Additionally, `flake8` linter is used to verify code style. It must succeeded
in order to make pull request approved.

Just run:
```bash
cd python-gitlab/
pip3 install --user tox
tox -e flake
```
to verify code style according to our guidelines (`tox` is required).

Before submitting a pull request make sure that the tests still pass with your change. 
Unit tests run using Github Actions and passing tests are mandatory 
to get merge requests accepted.

## <a name="commit"></a> Git Commit Guidelines

We have rules over how our git commit messages must be formatted. 
Please ensure to [squash](https://help.github.com/articles/about-git-rebase/#commands-available-while-rebasing)
unnecessary commits so that commit history is clean.

### <a name="commit-message-format"></a> Commit Message Format
Each commit message consists of a **header** and a **body**.

```
<header>
<BLANK LINE>
<body>
```

Any line of the commit message cannot be longer 100 characters! This allows the message to be easier
to read.

### Header
The Header contains a succinct description of the change:

* use the imperative, present tense: "change" not "changed" nor "changes"
* don't capitalize first letter
* no dot (.) at the end

### Body
If your change is simple, the Body is optional.

Just as in the Header, use the imperative, present tense: "change" not "changed" nor "changes".
The Body should include the motivation for the change

### Example
For example, here is a good commit message:

```
upgrade to Spring Boot 1.1.7

upgrade the Maven and Gradle builds to use the new Spring Boot 1.1.7,
see http://spring.io/blog/2014/09/26/spring-boot-1-1-7-released
```