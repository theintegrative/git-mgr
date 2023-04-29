from setuptools import setup

setup(
    name='grm',
    version='0.1',
    packages=['grm'],
    entry_points={
        'console_scripts': [
            'grm=grm.cli:main'
        ]
    },
    install_requires=[
        'typer',
        'GitPython'
    ]
)
