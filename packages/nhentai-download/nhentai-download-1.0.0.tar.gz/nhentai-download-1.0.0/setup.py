from setuptools import setup
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='nhentai-download',
    version='1.0.0',
    license='MIT',
    author='TOKYOCOLD69',
    author_email='TOKYOCOLD69@gamil.com',
    packages=['nhentai_downloader'],
    describe='nhentai download cli',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/TOKYOCOLD69/nhentai-downloader',
    keywords=['nhentai', 'downloader', 'anime'],
    entry_points={
        'console_scripts': [
            'nhentai=nhentai_downloader:main',
        ],
    },
    install_requires=[
        'beautifulsoup4>=4.9.3',
        'requests>=2.22.0',
        'tqdm>=4.62.0'
    ],
    python_requires='>=3.6',
)
