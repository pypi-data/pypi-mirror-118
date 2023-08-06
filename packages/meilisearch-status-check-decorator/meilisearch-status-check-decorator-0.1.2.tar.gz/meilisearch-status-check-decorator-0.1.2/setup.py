# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['meilisearch_status_check_decorator']

package_data = \
{'': ['*']}

install_requires = \
['meilisearch>=0.16.0,<0.17.0']

setup_kwargs = {
    'name': 'meilisearch-status-check-decorator',
    'version': '0.1.2',
    'description': 'A decorator to check for indexing status errors',
    'long_description': '# MeiliSearch Status Check Decorator\n\n[![Tests Status](https://github.com/sanders41/meilisearch-status-check-decorator/workflows/Testing/badge.svg?branch=main&event=push)](https://github.com/sanders41/meilisearch-status-check-decorator/actions?query=workflow%3ATesting+branch%3Amain+event%3Apush)\n[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/sanders41/meilisearch-status-check-decorator/main.svg)](https://results.pre-commit.ci/latest/github/sanders41/meilisearch-status-check-decorator/main)\n[![Coverage](https://codecov.io/github/sanders41/meilisearch-status-check-decorator/coverage.svg?branch=main)](https://codecov.io/gh/sanders41/meilisearch-status-check-decorator)\n[![PyPI version](https://badge.fury.io/py/meilisearch-status-check-decorator.svg)](https://badge.fury.io/py/meilisearch-status-check-decorator)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/meilisearch-status-check-decorator?color=5cc141)](https://github.com/sanders41/meilisearch-status-check-decorator)\n\nThis package provides a decorator for the [MeiliSearch Python](https://github.com/meilisearch/meilisearch-python)\nclient that will check for a failed status when adding documents.\n\n## Instillation\n\n```sh\npip install meilisearch-status-check-decorator\n```\n\n## Useage\n\n### Add documents with no errors\n\nIn this example there will be no errors so the documents will be added and the decorator will not\nprint anything.\n\n```py\nfrom meilisearch import Client\nfrom meilisearch_status_check_decorator import status_check\n\nindex = Client("http://localhost:7700", "masterKey").index("test")\n\n\n@status_check(index=index)\ndef good_insert():\n    documents = [\n      {\n        "id": 1,\n        "name": "test 1",\n      },\n      {\n        "id": 2,\n        "name": "test 2",\n      }\n    ]\n    index.add_documents(documents)\n```\n\n### Add documents with errors\n\nIn this example an error will be returned because a primary key cannot be inferred\n\n```py\nfrom meilisearch import Client\nfrom meilisearch_status_check_decorator import status_check\n\nindex = Client("http://localhost:7700", "masterKey").index("test")\n\n\n@status_check(index=index)\ndef bad_insert():\n    documents = [\n      {\n        "name": "test 1",\n      },\n      {\n        "name": "test 2",\n      }\n    ]\n    index.add_documents(documents)\n```\n\nThis will result in an error similar to the following being printed:\n\n```sh\nFAILED: {\'status\': \'failed\', \'updateId\': 0, \'type\': {\'name\': \'DocumentsAddition\'}, \'message\': \'missing primary key\', \'errorCode\': \'missing_primary_key\', \'errorType\': \'invalid_request_error\', \'errorLink\': \'https://docs.meilisearch.com/errors#missing_primary_key\', \'duration\': 0.025, \'enqueuedAt\': \'2021-08-29T17:06:59.877177189Z\', \'processedAt\': \'2021-08-29T17:06:59.906190045Z\'}\n```\n\n## Contributing\n\nContributions to this project are welcome. If you are interesting in contributing please see our [contributing guide](CONTRIBUTING.md)\n',
    'author': 'Paul Sanders',
    'author_email': 'psanders1@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sanders41/meilisearch-status-check-decorator',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
