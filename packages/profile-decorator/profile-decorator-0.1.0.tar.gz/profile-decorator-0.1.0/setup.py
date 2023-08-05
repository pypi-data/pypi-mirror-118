# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['profile_decorator']

package_data = \
{'': ['*']}

install_requires = \
['psutil>=4.0.0']

setup_kwargs = {
    'name': 'profile-decorator',
    'version': '0.1.0',
    'description': 'A simple decorator to profile memory usage in production apps',
    'long_description': '# profile-decorator\n\n## Problem/Motivation\n\nFind memory leaks in Python code quickly without significant code changes in a quickly digestible manner such that the root cause can be easily diagnosed.\n\nUntil open-telemetry [Adds metrics API](https://github.com/open-telemetry/opentelemetry-python/pull/1887), I want a quick and dirty decorator that will give me the  memory usage of the process in scope before and after a function is run.\n\n## Usage\n\n```python\n# example.py\nfrom profile_decorator import profile_decorator\n\nprofile_decorator.init()\n\n\n@profile_decorator.profile_memory\ndef my_func():\n    print("hello, world")\n\n\nif __name__ == "__main__":\n    my_func()\n```\n\n```zsh\n$ poetry run python example.py\nhello, world\n{\n  "start_time": "2021-08-29T13:20:31.435036",\n  "uss_memory_before": 6852608,\n  "end_time": "2021-08-29T13:20:31.435892",\n  "uss_memory_after": 6995968,\n  "lines": [\n    {\n      "filename": "/home/harry/projects/GitHub/hkiang01/profile-decorator/example.py",\n      "lineno": 7,\n      "size": 752,\n      "size_diff": 0\n    },\n    {\n      "filename": "/home/harry/projects/GitHub/hkiang01/profile-decorator/example.py",\n      "lineno": 12,\n      "size": 560,\n      "size_diff": 0\n    }\n  ]\n}\n```\n\n## Design\n\nThe decorator will collect the following information:\n- name of function\n- filepath\n- line number\n- memory usage before function is run\n- timestamp when function is called\n- timestamp when function is finished\n- memory usage after function is run\n\nIt will expose this in json or other easily digestble format for reporting purposes.\n',
    'author': 'Harrison Kiang',
    'author_email': 'hkiang01@gmail.com',
    'maintainer': 'Harrison Kiang',
    'maintainer_email': 'hkiang01@gmail.com',
    'url': 'https://github.com/hkiang01/profile-decorator',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4',
}


setup(**setup_kwargs)
