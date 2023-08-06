# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jarpyvscode', 'jarpyvscode.projects', 'tests']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'jarpyvscode',
    'version': '0.2.55555',
    'description': "Python backend for Jamil Raichouni's personal Visual Studio Code Extension jamilraichouni.jarpyvscode",
    'long_description': '# jarpyvscode\n\n![pipeline status](https://gitlab.com/jar1/jarpyvscode/badges/master/pipeline.svg)\n![coverage report](https://gitlab.com/jar1/jarpyvscode/badges/master/coverage.svg)\n![flake8](https://gitlab.com/jar1/jarpyvscode/-/jobs/artifacts/master/raw/badges/flake8.svg?job=flake8)\n![mypy](https://gitlab.com/jar1/jarpyvscode/-/jobs/artifacts/master/raw/badges/mypy.svg?job=mypy)\n![black](https://gitlab.com/jar1/jarpyvscode/-/jobs/artifacts/master/raw/badges/black.svg?job=black)\n![isort](https://gitlab.com/jar1/jarpyvscode/-/jobs/artifacts/master/raw/badges/isort.svg?job=isort)\n\n## Documentation\n\nFind the docs at https://jar1.gitlab.io/jarpyvscode\n\n## Steps to create project\n\n### Create blank Visual Studio Code extension\n\n```bash\ncd ~/repos\nyo code\n\n# ? What type of extension do you want to create? (Use arrow keys)\n# ❯ New Extension (TypeScript)\n\n# ? What\'s the name of your extension? ()\n# ❯ jarpyvscode\n\n# ? What\'s the identifier of your extension? (jarpyvscode)\n# ❯ jarpyvscode\n\n# ? What\'s the description of your extension? ()\n# ❯ Jamil Raichouni\'s personal Visual Studio Code Extension\n\n# ? Initialize a git repository? (Y/n) n\n\n# ? Bundle the source code with webpack? (y/N) y\n\n# ? Which package manager to use? (Use arrow keys)\n# ❯ npm\n#   yarn\n\ncd jarpyvscode\ngit init\ntouch .gitignore\n\n```\n\nPut the following into the `.gitignore`:\n\n```bash\n.vscode-test/\ndist/\nnode_modules/\nout/\n\n*.vsix\n\n```\n\n### Version control\n\nBefore we continue, we store the fresh extension in an VCS.\n\n```bash\ngit remote add origin git@gitlab.com:jar1/jarpyvscode.git\ngit add .\ngit commit -m "Initial commit"\n\n```\n\n### Initialise Python poetry project\n\n```bash\npoetry init\n\n# Package name [jarpyvscode]:\n# ❯ jarpyvscode\n\n# Would you like to define your main dependencies interactively? (yes/no) [yes]\n# ❯ no\n\n# Would you like to define your development dependencies interactively? (yes/no) [yes]\n# ❯ no\n```\n\nAdd dependencies:\n\n```bash\npoetry add click json5 pandas psutil loguru\npoetry add --dev black doc8 flake8 flake8-builtins flake8-docstrings flake8-isort flake8-quotes flake8-rst-docstrings isort jupyter notebook pydocstyle pytest pytest-cov pytest-xdist Sphinx sphinx-autobuild sphinx-rtd-theme\n```\n\n---\n\nWE RECOMMEND INCLUDING THE FOLLOWING SECTIONS:\n\n## Features\n\nDescribe specific features of your extension including screenshots of your extension in\naction. Image paths are relative to this README file.\n\nFor example if there is an image subfolder under your extension project workspace:\n\n\\!\\[feature X\\]\\(images/feature-x.png\\)\n\n> Tip: Many popular extensions utilize animations. This is an excellent way to show off\n> your extension! We recommend short, focused animations that are easy to follow.\n\n## Requirements\n\nIf you have any requirements or dependencies, add a section describing those and how to\ninstall and configure them.\n\n## Extension Settings\n\nInclude if your extension adds any VS Code settings through the\n`contributes.configuration` extension point.\n\nFor example:\n\nThis extension contributes the following settings:\n\n- `myExtension.enable`: enable/disable this extension\n- `myExtension.thing`: set to `blah` to do something\n\n## Known Issues\n\nCalling out known issues can help limit users opening duplicate issues against your\nextension.\n\n## Release Notes\n\nsee `CHANGELOG.md`\n\n---\n\n## Following extension guidelines\n\nEnsure that you\'ve read through the extensions guidelines and follow the best practices\nfor creating your extension.\n\n- [Extension Guidelines](https://code.visualstudio.com/api/references/extension-guidelines)\n\n```\n\n```\n',
    'author': 'Jamil Raichouni',
    'author_email': 'raichouni@gmail.com',
    'maintainer': 'Jamil Raichouni',
    'maintainer_email': 'raichouni@gmail.com',
    'url': 'https://jar1.gitlab.io/jarpyvscode',
    'packages': packages,
    'package_data': package_data,
}


setup(**setup_kwargs)
