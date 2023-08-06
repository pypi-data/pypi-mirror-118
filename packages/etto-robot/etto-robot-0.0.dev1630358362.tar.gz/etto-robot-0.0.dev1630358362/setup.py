import os

from setuptools import setup, find_packages

__version__ = '0.0.dev1630358362'


def read(file_name):
    with open(os.path.join(os.path.dirname(__file__), file_name)) as f:
        return f.read()


setup(
    name='etto-robot',
    version=__version__,
    description='Python Library to Build Web Robots',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    url='https://github.com/ettoreleandrotognoli/py-robot',
    download_url='https://github.com/ettoreleandrotognoli/py-robot/tree/%s/' % __version__,
    license='Apache License 2.0',
    author='Éttore Leandro Tognoli',
    author_email='ettoreleandrotognoli@gmail.com',
    data_files=[
        'LICENSE',
    ],
    packages=find_packages(
        './src/main/python/',
    ),
    package_dir={'': 'src/main/python'},
    include_package_data=True,
    keywords=['Robot', 'Web Crawler'],
    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Framework :: AsyncIO',
        'Topic :: Internet :: WWW/HTTP :: Indexing/Search',
    ],
    install_requires=[
        'aiohttp==3.7',
        'pyquery==1.4',
        'jsonpath-ng==1.5',
    ],
    tests_require=[
        'coverage==5.3',
        'pylint==2.6',
        'aiounittest==1.4',
        'pytest-httpserver==0.3',
    ],
)
