from setuptools import setup, find_packages

# Leer la descripción larga desde README.md
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

# Leer los autores desde el archivo AUTHORS
with open('AUTHORS', 'r', encoding='utf-8') as f:
    authors = f.read().strip().split('\n')
    author_names = ', '.join([a.split(' <')[0] for a in authors])
    author_emails = ', '.join([a.split(' <')[1][:-1] for a in authors])

setup(
    name='scidx',
    version='0.1.0',
    description='Description of scidx',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=author_names,
    author_email=author_emails,
    url='https://github.com/sci-ndp/scidx-py',
    packages=find_packages(),
    install_requires=[
        # List of dependencies, if any
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
