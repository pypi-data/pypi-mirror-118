import setuptools
from pathlib import Path
import os


with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name='bilibili-data',
    version='0.0.6',
    license='GPLv3+',
    author='tyler',
    author_email='tyler_d1128@outlook.com',
    description='哔哩哔哩数据聚合获取',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(where='src'),
    package_dir={'': 'src'},
    keywords=[
        'bilibili',
        'api',
        'spider',
        'data'
    ],
    classifiers=[
            "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
            "Natural Language :: Chinese (Simplified)",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9"
        ],
    install_requires=[
        'bilibili-api'
    ],
    url="https://github.com/duanfuqiang1128/bilibili-data",
    project_urls={
        'Bug Tracker': 'https://github.com/duanfuqiang1128/bilibili-data/issues',
    },
    python_requires=">=3.8"
)
