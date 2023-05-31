from setuptools import setup

setup(
    name='git-mgr',
    version='0.1',
    packages=['GitMgr'],
    entry_points={
        'console_scripts': [
            'git-mgr=GitMgr.cli:main'
        ]
    },
    install_requires=[
        'typer',
        'GitPython'
    ]
)
