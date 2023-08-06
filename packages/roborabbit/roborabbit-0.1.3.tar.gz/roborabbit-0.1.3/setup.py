# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['roborabbit']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0', 'aio-pika>=6.8.0,<7.0.0', 'click>=8.0.1,<9.0.0']

entry_points = \
{'console_scripts': ['roborabbit = run:config_rmq']}

setup_kwargs = {
    'name': 'roborabbit',
    'version': '0.1.3',
    'description': 'Set up your rabbit instance using a declarative yaml file.',
    'long_description': '# RoboRabbit\n\nSet up your rabbit instance using a declarative yaml file.\n\n## Command\n\n`roborabbit --config path/to/roborabbit.yaml`\n\n## Example yaml files\n\n### Simple declare queue, exchange, and bind\n\n```\n# Connection info\nhost: localhost\nusername: guest\npassword: guest\nvirtualhost: /\nport: 5672\nexchanges:\n  - name: exchange_1\n    type: topic\nqueues:\n  - name: queue_1\nbindings:\n  - from:\n      type: exchange\n      name: exchange_1\n    to:\n      type: queue\n      name: queue_1\n    routing_key: records.created\n```\n\n### Header exchange declaration and binding\n\n```\n# Connection info\nhost: localhost\nusername: guest\npassword: guest\nvirtualhost: /\nport: 5672\nexchanges:\n  - name: exchange_2\n    type: headers\nqueues:\n  - name: queue_2\nbindings:\n  - from:\n      type: exchange\n      name: exchange_2\n    to:\n      type: queue\n      name: queue_1\n    bind_options:\n      x-match: all\n      hw-action: header-value\n```\n\n## All Values Available\n\n```\n# Connection info\nhost: localhost\nusername: guest\npassword: guest\nvirtualhost: /\nport: 5672\n\n# Exchange declarations\nexchanges:\n  - name: string\n    type: topic|headers|direct|fanout # topic is default\n    durable: false # default\n    auto_delete: true # default\n\n# queue declarations\nqueues:\n  - name: string\n    type: quorum # Not required. This is the default and currently only option available (For us, all our queues are quorum. We manually create the queue that needs other requirements). MR welcome\n    # create_dlq: true # TODO: This will be the default. Set to false if you do not want a dead letter queue/exchange for this queue\n    durable: true # default\n    robust: true # default\n    auto_delete: false # default\n    exclusive: false # default\n    auto_delete_delay: 0 # default\n    arguments: # rabbit specific key/value pairs\n      key_1: value_1\n      key_2: value_2\n\n# bindings\nbindings:\n  - from:\n      type: exchange\n      name: string\n    to:\n      type: exchange|queue\n      name: string\n    routing_key: string # required, unless bind_options is defined\n    bind_options: # required if binding to a header exchange\n      x-match: all|any # header type of matcher\n      header-key: string # header topic to be matched\n```\n',
    'author': 'Skyler Lewis',
    'author_email': 'skyler@hivewire.co',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/alairock/roborabbit',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
