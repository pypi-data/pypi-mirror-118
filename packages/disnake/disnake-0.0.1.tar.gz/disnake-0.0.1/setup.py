from setuptools import setup
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

version = '0.0.1'


setup(
    name='disnake',
    version=version,
    description='A python wrapper for Discord API forked from discord.py.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    url='https://github.com/EQUENOS/disnake',
    author='EQUENOS',
    author_email='equenos1@gmail.com',
    keywords='python, discord, api, discord-api, discord-py, interactions',
    packages=['disnake'],
    python_requires='>=3.8, <4',
    install_requires=requirements,
    project_urls={
        'Bug Reports': 'https://github.com/EQUENOS/disnake/issues',
        'Source': 'https://github.com/EQUENOS/disnake',
    },
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
      ]
)