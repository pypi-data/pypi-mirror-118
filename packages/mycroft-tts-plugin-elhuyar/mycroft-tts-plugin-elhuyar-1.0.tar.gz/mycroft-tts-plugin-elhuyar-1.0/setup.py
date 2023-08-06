#!/usr/bin/env python3
from os.path import join, abspath, dirname,exists
from setuptools import setup
import pathlib

PLUGIN_TYPE = 'tts'
PLUGIN_MODULE_NAME = 'elhuyar_tts'
PLUGIN_TARGET = 'mycroft_tts_plugin_elhuyar:ElhuyarTTSPlugin'

PLUGIN_KEYWORDS = 'mycroft plugin {}'.format(PLUGIN_TYPE)
PLUGIN_NAMESPACE = 'mycroft.plugin.{}'.format(PLUGIN_TYPE)
PLUGIN_ENTRY_POINT = '{} = {}'.format(PLUGIN_MODULE_NAME, PLUGIN_TARGET)

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.rst").read_text()

req_file = join(dirname(abspath(__file__)), 'requirements.txt')
if exists(req_file):
    with open(req_file) as f:
        requirements = f.readlines()
else:
    requirements = []

setup(
    name='mycroft-tts-plugin-elhuyar',
    version='1.0',
    description='TTS plugin for Mycroft that uses Elhuyar\'s TTS service (Basque)',
    long_description=README,
    url='https://github.com/Mycroft-eus/mycroft-tts-plugin-elhuyar',
    author='Igor Leturia',
    author_email='i.leturia@elhuyar.eus',
    license='Apache-2.0',
    packages=['mycroft_tts_plugin_elhuyar'],
    install_requires=requirements,
    zip_safe=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Text Processing :: Linguistic',
        'License :: OSI Approved :: Apache Software License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords=PLUGIN_KEYWORDS,
    entry_points={PLUGIN_NAMESPACE: PLUGIN_ENTRY_POINT}
)
