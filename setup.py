from setuptools import setup, find_packages

requirements = ['aiohttp']

with open('README.md', encoding='UTF-8') as f:
    readme = f.read()

setup(
    name = 'pybalebot',
    version = '0.0.1',
    author='Shayan Heidari',
    author_email = 'contact@shayanheidari.info',
    description = 'Modern and fully asynchronous framework for Bale Bot API',
    keywords = ['pybalebot', 'bale', 'chat', 'bot', 'robot', 'asyncio'],
    long_description = readme,
    python_requires='~=3.7',
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/shayanheidari01/pybalebot',
    packages = find_packages(),
    exclude_package_data = {'': ['*.pyc', '*__pycache__*']},
    install_requires = requirements,
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Topic :: Internet',
        'Topic :: Communications',
        'Topic :: Communications :: Chat',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries :: Application Frameworks'
    ],
)