# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['partifact']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.15,<2.0', 'tomlkit>=0.7.0,<1.0.0', 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['partifact = partifact.main:app']}

setup_kwargs = {
    'name': 'partifact',
    'version': '0.1.0',
    'description': '',
    'long_description': '# pArtifact\n\npArtifact is a tool to help with configuring and authenticating CodeArtifact as a repository for [Poetry](https://github.com/python-poetry/poetry) and [pip](https://pip.pypa.io/en/stable/).\n\n[AWS CLI](https://docs.aws.amazon.com/cli/latest/reference/codeartifact/login.html) offers functionality to configure CodeArtifact for pip.\nThis tool offers the following improvements over the CLI:\n1. Poetry support.\n1. Assuming an AWS role to get the token. This is handy in automated pipelines, which may have the access key and secret key as environment variables,\n  but want to install packages from CodeArtifact on a different account.\n1. Configuration persisted in a config file, making the tool more convenient to use than the CLI with the options it requires to be passed in from the command line.\n\n\n# How to use?\n\nInstall pArtifact from pypi using pip the usual way:\n\n```shell\npip install partifact\n```\n\nIt\'s best to do this globally, rather than inside the virtualenv.\n\nBefore you can use pArtifact, you need to configure it for your project\nin the `pyproject.toml` file.\n\nIn the future, this will be done via a configuration tool.\nFor now, however, add the following to the file manually:\n\n```toml\n[tool.partifact.repository.POETRY_REPOSITORY_NAME]\ncode_artifact_account = "your-aws-account-hosting-codeartifact"\ncode_artifact_domain = "your-domain-name"\ncode_artifact_repository = "your-codeartifact-repository"  # not the same as the Poetry repository\naws_profile = "your-aws-profile"  # optional\naws_role_arn = "an-aws-role-to-assume"  # optional\n```\n\nReplace `POETRY_REPOSITORY_NAME` with your Poetry repository name. E.g. for the following\nPoetry configuration:\n\n```toml\n[[tool.poetry.source]]\nname = "myrepo"\nurl = "https://myrepo-codeartifact-url"\n```\n\n`POETRY_REPOSITORY_NAME` should be set to "myrepo".\n\nThe configuration entries are:\n1. `code_artifact_account`: The account hosting the CodeArtifact repository.\n2. `code_artifact_domain`: The [CodeArtifact domain](https://docs.aws.amazon.com/codeartifact/latest/ug/domains.html).\n3. `code_artifact_repository`: The [CodeArtifact repository](https://docs.aws.amazon.com/codeartifact/latest/ug/repos.html).\n4. `aws_profile` (optional): Use a non-default AWS profile to get the CodeArtifact token.\n5. `aws_role_arn` (optional): Assume and use this AWS role to get the CodeArtifact token.\nThis is useful in deployment pipelines, where ENV variables are used for the AWS\naccess key and secret key and the keys are for the account it\'s deploying the application\nin, rather than the CodeArtifact account.\n\nOnce everything is configured, you can log into CodeArtifact using the\npArtifact login command:\n\n```shell\npartifact login [POETRY_REPOSITORY_NAME]\n```\n',
    'author': 'David Steiner',
    'author_email': 'david_j_steiner@yahoo.co.nz',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
