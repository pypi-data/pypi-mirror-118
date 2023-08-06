from setuptools import find_packages, setup

setup(
    name='sweelimiter',
    packages=['sweelimiter','sweelimiter.api','sweelimiter.backends','sweelimiter.extractors'],
    version='0.1.3',
    description='Limiter for fastapi',
    author='Maxim Besogonov',
    author_email='swifstail@gmail.com',
    license='mpl-2.0',
    keywords=['fastapi', 'starlette', 'ratelimit', 'limiter', 'redis'],
    install_requires=['fastapi~=0.68.1', 'starlette~=0.14.2'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest~=6.2.5', 'requests'],
    test_suite='tests',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
