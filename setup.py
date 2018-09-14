import os
from setuptools import setup, find_packages

base_dir = os.path.dirname(__file__)

def readme():
    with open('README.md') as f:
        return f.read()

about = {}
with open(os.path.join(base_dir, 'wpexport', '__about__.py')) as f:
    exec(f.read(), about)

setup(
    name=about['__title__'],
    version=about['__version__'],
    description=about['__summary__'],
    url=about['__url__'],
    author=about['__author__'],
    author_email=about['__email__'],
    license=about['__license__'],
    long_description=readme(),
    keywords='github wordpress backup sync',
    packages=find_packages(),
    install_requires=[
        'gitpython', 'python-wordpress-xmlrpc', 'pypandoc',
    ],
    entry_points = {
        'console_scripts': [
            'wpexport=wpexport.__main__:main',
        ],
    },
    include_package_data=True,
    zip_safe=False
)
