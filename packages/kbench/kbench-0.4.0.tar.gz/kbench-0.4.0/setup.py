# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kbench']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0,<9.0', 'kubernetes>=18.20,<19.0', 'loguru>=0.5,<0.6']

entry_points = \
{'console_scripts': ['kbench = kbench.__main__:cli']}

setup_kwargs = {
    'name': 'kbench',
    'version': '0.4.0',
    'description': 'Benchmarking tool for Kubernetes clusters',
    'long_description': '# kbench\n[![CircleCI](https://circleci.com/gh/keichi/kbench.svg?style=svg)](https://circleci.com/gh/keichi/kbench)\n[![PyPI](https://img.shields.io/pypi/v/kbench?style=flat-square)](https://pypi.org/project/kbench)\n\n## Installation\n\n```\n$ pip install kbench\n```\n\n## Usage\n\n### pod-throughput\n\nLaunch multiple pods in parallel and measure their startup and cleanup time.\n\n```\n$ kbench pod-throughput\n```\n\n- `-n`, `--num-pods`: Number of pods to launch.\n- `-i`, `--image`: Container image to use.\n- `--timings` / `--no-timings`:  Print timing information for all pods.\n\n### pod-latency\n\nLaunch multiple pods sequentially and measure their startup and cleanup time.\n\n```\n$ kbench pod-latency\n```\n\n- `-n`, `--num-pods`: Number of pods to launch.\n- `-i`, `--image`: Container image to use.\n- `--timings` / `--no-timings`:  Print timing information for all pods.\n\n### deployment-scaling\n\nCreate a deployment and measure scale-in/out latency. First, a deployment with\n`m` replicas is created. Then, the deployment is scaled-out to `n` replicas.\nOnce the scale-out is completed, the deployment is scaled-in to `m` replicas\nagain.\n\n```\n$ kbench deployment-scaling\n```\n\n- `-i`, `--image`: Container image to use.\n- `-m`, `--num-init-replicas`: Initial number of replicas.\n- `-n`, `--num-target-replicas`: Target number of replicas.\n',
    'author': 'Keichi Takahashi',
    'author_email': 'keichi.t@me.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/keichi/kbench/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
