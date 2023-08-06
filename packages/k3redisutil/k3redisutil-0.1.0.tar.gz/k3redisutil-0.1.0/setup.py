# DO NOT EDIT!!! built with `python _building/build_setup.py`
import setuptools
setuptools.setup(
    name="k3redisutil",
    packages=["k3redisutil"],
    version="0.1.0",
    license='MIT',
    description='For using redis more easily.',
    long_description='# k3redisutil\n\n[![Action-CI](https://github.com/pykit3/k3redisutil/actions/workflows/python-package.yml/badge.svg)](https://github.com/pykit3/k3redisutil/actions/workflows/python-package.yml)\n[![Build Status](https://travis-ci.com/pykit3/k3redisutil.svg?branch=master)](https://travis-ci.com/pykit3/k3redisutil)\n[![Documentation Status](https://readthedocs.org/projects/k3redisutil/badge/?version=stable)](https://k3redisutil.readthedocs.io/en/stable/?badge=stable)\n[![Package](https://img.shields.io/pypi/pyversions/k3redisutil)](https://pypi.org/project/k3redisutil)\n\nFor using redis more easily.\n\nk3redisutil is a component of [pykit3] project: a python3 toolkit set.\n\n\nFor using redis more easily.\n\n\n\n# Install\n\n```\npip install k3redisutil\n```\n\n# Synopsis\n\n```python\n\nimport k3redisutil\nimport time\n\n# Using redis as a duplex cross process communication channel pool.\n\n# client and server with the same channel name "/foo" is a pair\nc = k3redisutil.RedisChannel(6379, \'/foo\', \'client\')\ns = k3redisutil.RedisChannel(6379, \'/foo\', \'server\')\n\nc.send_msg(\'c2s\')\ns.send_msg(\'s2c\')\n\n# list channels\nprint(c.list_channel(\'/\'))  # ["/foo"]\nprint(s.recv_msg())  # c2s\nprint(c.recv_msg())  # s2c\n\ncli = k3redisutil.RedisProxyClient([(\'127.0.0.1\', 2222), (\'192.168.0.100\', 222)])\n\ncli.set(\'k1\', \'v1\', retry=1)\ncli.set(\'k2\', \'v2\', expire=1000)  # msec\n\nprint(cli.get(\'k1\', retry=2))\n# out: \'v1\'\n\nprint(cli.get(\'k2\'))\n# out: \'v2\'\n\ntime.sleep(1)\ncli.get(\'k2\')\n# raise a \'redisutil.KeyNotFoundError\' because it is timeout\n\ncli.hset(\'hashname1\', \'k3\', \'v3\')\ncli.hset(\'hashname2\', \'k4\', \'v4\', expire=1000)\n\nprint(cli.hget(\'hashname1\', \'k3\'))\n# out: \'v3\'\n\nprint(cli.hget(\'hashname2\', \'k4\'))\n# out: \'v4\'\n\ntime.sleep(1)\ncli.hget(\'hashname2\', \'k4\')\n# raise a \'redisutil.KeyNotFoundError\' because it is timeout\n\n```\n\n#   Author\n\nZhang Yanpo (张炎泼) <drdr.xp@gmail.com>\n\n#   Copyright and License\n\nThe MIT License (MIT)\n\nCopyright (c) 2015 Zhang Yanpo (张炎泼) <drdr.xp@gmail.com>\n\n\n[pykit3]: https://github.com/pykit3',
    long_description_content_type="text/markdown",
    author='Zhang Yanpo',
    author_email='drdr.xp@gmail.com',
    url='https://github.com/pykit3/k3redisutil',
    keywords=['python', 'redis'],
    python_requires='>=3.0',

    install_requires=['k3ut<0.2,>=0.1.15', 'k3awssign<0.2,>=0.1.0', 'k3thread<0.2,>=0.1.0', 'k3utfjson<0.2,>=0.1.1', 'k3confloader<0.2,>=0.1.1', 'k3utdocker<0.2,>=0.1.0', 'k3http<0.2,>=0.1.0', 'redis>=3.5.0', 'mock>=4.0.0'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
    ] + ['Programming Language :: Python :: 3'],
)
