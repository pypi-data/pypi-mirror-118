import setuptools
from distutils.core import setup

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='quick-mock',
    version='0.0.1',
    author='丘家劲',
    author_email='609799548@qq.com',
    description='quick mock server',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT Licence',
    url='https://github.com/qiujiajin/quick-mock',
    entry_points={
        'console_scripts': [
            'mock=quick_mock:main',
        ]
    },
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'flask==2.0.1'
    ]
)
