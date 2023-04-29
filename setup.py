from setuptools import setup

setup(
    name='git-repo-manager',
    version='0.1',
    packages=['GitRepoManager'],
    entry_points={
        'console_scripts': [
            'git-repo-manager=GitRepoManager.cli:main'
        ]
    },
    install_requires=[
        'typer',
        'GitPython'
    ]
)
