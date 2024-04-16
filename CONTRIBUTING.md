
# Contribute to PST Nodes

This page will give you a quick overview of how things are organized and most importantly, how to get involved.

## We develop with Github

We use github to host code, to track issues and feature requests, as well as accept pull requests.


## Git Branching Workflow:
Our project uses the Gitflow branching model to manage code contributions and releases. This model consists of three main branches: dev, main, and the release branch. Development work is done on feature branches, which are merged into the dev branch once they are complete. The dev branch serves as the integration branch, where all the features are brought together and tested as a whole. Once the dev branch is stable and ready for release, a new release branch is created off of the dev branch. The release branch is used to perform any final testing and bug fixing before the release.

When you contribute code to our project, we ask that you follow the Gitflow workflow by creating a new feature or bugfix branch off of the dev branch, making your changes, and `submitting a pull request to merge your changes back into the dev branch`. We encourage you to keep your branches small and focused on a single task, and to test your changes thoroughly before submitting a pull request. This will help to ensure that your changes integrate smoothly with the rest of the codebase and minimize the risk of introducing bugs or conflicts.

If you're not familiar with Gitflow or need more guidance on how to contribute code to our project, please refer to the Gitflow documentation or reach out to our team for assistance. 


## Branch naming conventions:

In the Gitflow branching workflow, it's important to follow naming conventions when creating new branches for features, bugfixes, and releases. Typically, feature branches have a prefix of `feature/`, bugfix branches have a prefix of `bugfix/`, and release branches have a prefix of `release/`.


## Example

Let's say we decided to implement a new feature to our project to save a pst file. In that case we recommend creating a new feature branch called `feature/pst_writer` off of the dev branch. This can be done by running the following command in your Git repository:

```
$ git checkout dev
$ git pull
$ git checkout -b feature/pst_writer
```
Once you have created the new branch, you can start working on your feature by adding new code and making changes to existing files as needed. When you are ready to submit your changes, you can create a new pull request on GitHub that targets the dev branch. Our team will review your changes and provide feedback or request revisions as needed.

Once your pull request has been approved and merged into the dev branch, it will be included in the next release of our project. From there, it will be merged into the main branch, which represents the stable and production-ready version of our project.


## Unit testing

**Prerequistes**: `pytest` should be installed with either `conda` or `pip`

All tests are located in the `tests` folder and start with `test_`. Run the entire test suite by running the following command from the project root directory:

```
$ pytest
```
To run a specific test module or test function, you can use the following command:

```
$ pytest tests/test_module.py
```
Replace test_module with the name of the test module you want to run.

## Code conventions

We follows the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html), which provides guidelines for writing Python code that is clear, readable, and maintainable. We strive to follow these guidelines to improve the quality and consistency of our code.

Here are some key points:

* Use four spaces for indentation.
* Use docstrings to document all functions, classes, and methods.
* Use `snake_case` 🐍 (lowercase_with_underscores) for variable names and function names.
* Use CAPITALIZED_WITH_UNDERSCORES for constants.
* Use `CamelCase` 🐫 for class names.
* Use whitespace to improve readability.
* Avoid extraneous whitespace.
* Use meaningful variable names.
* Use exception chaining appropriately.
* Follow Python's import style.