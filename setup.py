import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='scan_tagger',
    version='0.1.0',
    author='James Pearson Hughes',
    author_email='pearson@changedmy.name',
    description='A helper script for applying metadata from Exif Notes to scans.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/xiongchiamiov/scan-tagger',
    project_urls={
        'Bug Tracker': 'https://github.com/xiongchiamiov/scan-tagger/issues',
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    entry_points={
        'console_scripts': [
            'scan-tagger=scan_tagger:main',
        ],
    },
    python_requires='>=3.6',
)
