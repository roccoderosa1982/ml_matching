from setuptools import setup, find_packages

setup(
    name='ml_matching',
    version='0.1.0',
    packages=find_packages(include=['src', 'src.*']),
    install_requires=[
        'numpy',
        'scikit-learn'
    ],
    entry_points={
        'console_scripts': [
            'ml_matching=main:main',
        ],
    },
)