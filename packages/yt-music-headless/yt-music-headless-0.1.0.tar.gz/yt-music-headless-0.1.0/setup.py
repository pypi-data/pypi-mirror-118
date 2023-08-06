from setuptools import setup, find_packages

with open('requirements.txt') as file:
    requirements = file.readlines()

description = 'A CLI to search & retrieve audio streams from YouTube Music.'

setup(
    name='yt-music-headless',
    version='0.1.0',
    author='Hitesh Kumar Saini',
    author_email='saini123hitesh@gmail.com',
    url='https://github.com/alexmercerind/yt-music-headless',
    description=description,
    long_description=description,
    long_description_content_type='text/markdown',
    license='MIT',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'yt-music-headless = ytmusicheadless:main'
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    keywords='youtube youtube-music youtube-playback',
    install_requires=requirements,
    zip_safe=False
)
