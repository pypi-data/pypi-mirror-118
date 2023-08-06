# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pypj']

package_data = \
{'': ['*']}

install_requires = \
['single-source>=0.2.0,<0.3.0']

entry_points = \
{'console_scripts': ['pypj = pypj.main:main']}

setup_kwargs = {
    'name': 'pypj',
    'version': '0.2.2',
    'description': 'Python project initializer',
    'long_description': '```txt\n┌─┐┬ ┬┌─┐┬\n├─┘└┬┘├─┘│\n┴   ┴ ┴ └┘\n```\n\npypj is a command that initializes a modern python project.\n\n## Installation\n\n```sh\npip install pypj\n```\n\n## Usage\n\n```\n$ pypj\n\n┌─┐┬ ┬┌─┐┬\n├─┘└┬┘├─┘│    python : 3.8.5\n┴   ┴ ┴ └┘    poetry : 1.1.7\n\nPackage name: my-package\nDo you want to use customized setting? (y/N): N\n  Command: poetry new my-package ✨\n  Command: poetry config virtualenvs.in-project true ✨\nInitialize done 🚀\n  Create : .vscode directory ✨\n  Create : .vscode/settings.json ✨\n  Command: poetry add -D black ✨\n  Command: poetry add -D pyproject-flake8 ✨\n  Command: poetry add -D mypy ✨\n  Command: poetry add -D isort ✨\n  Command: poetry add -D pytest ✨\n  Command: poetry add -D pytest-cov ✨\n\nComplete! 🚀\nLet\'s make the world better! ✨😋🐍🌎\n```\n\n### Requirement\n\n- python\n- poetry\n\n## What will be done\n\n- Install elementary dev packages in once\n- Configure dev tools on `pyproject.toml`\n  - Aggregate all configurations in one\n\n### Details\n\n- Installation\n  - Formatter: [`black`](https://github.com/psf/black)\n  - Linter: [`pflake8`](https://github.com/csachs/pyproject-flake8)\n  - Type linter: [`mypy`](https://github.com/python/mypy)\n  - Import formatter: [`isort`](https://github.com/PyCQA/isort)\n  - Test framework: [`pytest`](https://github.com/pytest-dev/pytest)\n    - Plugin: [`pytest-cov`](https://github.com/pytest-dev/pytest-cov)\n- Configuration on `pyproject.toml`\n  - Max line length: default is `119`\n  - Ignore [`PEP8`](https://pep8.org/): `None`\n    - No PEP8 rules are ignored\n  - Comfortable `mypy` setting\n\n## Why black and pflake8?\n\n### Formatter: [`black`](https://github.com/psf/black)\n\n`Black` finalize the formats in one. That\'s the biggest reason it got chosen.\n\n> Black is the uncompromising Python code formatter. By using it, you agree to cede control over minutiae of hand-formatting. In return, Black gives you speed, determinism, and freedom from pycodestyle nagging about formatting. You will save time and mental energy for more important matters.\n\n### Linter: [`pflake8`](https://github.com/csachs/pyproject-flake8)\n\nThe configurations must be aggregated in one place, `pyproject.toml`. `pflake8` enables to configure `flake8` on `pyproject.toml`.\n\n## Example of pyproject.toml\n\nWith default setting, this kind of `pyproject.toml` file will be generated.\n\n```toml\n[tool.poetry]\nname = "my-package"\nversion = "0.1.0"\ndescription = ""\nauthors = ["you <you@example.com>"]\n\n[tool.poetry.dependencies]\npython = "^3.8"\n\n[tool.poetry.dev-dependencies]\npytest = "^5.2"\nblack = "^21.8b0"\npyproject-flake8 = "^0.0.1-alpha.2"\nmypy = "^0.910"\nisort = "^5.9.3"\npytest-cov = "^2.12.1"\n\n[build-system]\nrequires = ["poetry-core>=1.0.0"]\nbuild-backend = "poetry.core.masonry.api"\n\n[tool.black]\nline-length = 119\nexclude = \'\'\'\n(\n    migrations\n    | .mypy_cache\n    | .pytest_cache\n    | .tox\n    | venv\n)\n\'\'\'\n\n[tool.flake8]\nmax-line-length = 119\nmax-complexity = 10\n\n[tool.mypy]\n# common\npython_version = 3.8\nshow_column_numbers = true\nshow_error_context = true\nignore_missing_imports = true\ncheck_untyped_defs = true\ndisallow_untyped_defs = true\n# warning\nwarn_return_any = true\nwarn_unused_configs = true\nwarn_redundant_casts = true\n\n[tool.isort]\nprofile = "black"\nline_length = 119\n```\n\n## Supported python versions\n\n- Supported: `3.7`, `3.8`, `3.9`\n- Is going to be supported: `3.10`\n- Not supported: `3.6` or less\n\n**NOTE**: According to [Status of Python branches](https://devguide.python.org/#status-of-python-branches), the EoL of Python 3.6 is `2021-12-23`.\n',
    'author': 'edge-minato',
    'author_email': 'edge.minato@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/edge-minato/pypj',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
