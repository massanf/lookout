from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='lookout-python',
    packages=['lookout'],

    version='1.0.0',

    license='MIT',

    install_requires=['oauthlib'],

    author='trombiano1',
    author_email='mfujitadev@gmail.com',

    url='https://github.com/trombiano1/lookout',

    description='Notify via E-mail or Slack Incoming Webhooks when command ends or runs into error.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='lookout notification notify',

    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],

    entry_points={
        'console_scripts': ['lookout=lookout.lookout:main'],
    }
)
