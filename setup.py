from setuptools import setup, find_packages

# Read the long description from README.md
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

# Read the authors from the AUTHORS file
with open('AUTHORS', 'r', encoding='utf-8') as f:
    authors = f.read().strip().split('\n')
    author_names = ', '.join([a.split(' <')[0] for a in authors])
    author_emails = ', '.join([a.split(' <')[1][:-1] for a in authors])

# Read dependencies from requirements.txt
with open('requirements.txt', 'r', encoding='utf-8') as f:
    requirements = f.read().splitlines()

# Read staging requirements
with open('staging-requirements.txt', 'r',  encoding='utf-8') as f:
    staging_requirements = f.read().splitlines()

setup(
    name='scidx',
    version='0.3.0',
    description='Python client library for interacting with the sciDX API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=author_names,
    author_email=author_emails,
    url='https://github.com/sci-ndp/scidx-py',
    packages=find_packages(),
    install_requires=requirements,
    extras_require={
        'staging': staging_requirements
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
