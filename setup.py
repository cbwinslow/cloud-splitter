from setuptools import setup, find_packages

# Read requirements from file
with open('requirements.txt') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

# Read long description from README
with open('README.md') as f:
    long_description = f.read()

setup(
    name='cloud-splitter',
    version='0.1.0',
    description='A TUI-based tool for downloading and splitting audio stems from videos',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='cbwinslow',
    author_email='cbwinslow@example.com',
    url='https://github.com/cbwinslow/cloud-splitter',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=requirements,
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-asyncio>=0.18.0',
            'pytest-cov>=3.0.0',
            'black>=22.0.0',
            'flake8>=4.0.0',
            'mypy>=0.950',
        ],
    },
    entry_points={
        'console_scripts': [
            'cloud-splitter=cloud_splitter.cli:main',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Multimedia :: Sound/Audio',
        'Topic :: Multimedia :: Sound/Audio :: Conversion',
    ],
    python_requires='>=3.8',
)
