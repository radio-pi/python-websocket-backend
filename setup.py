from setuptools import setup, find_packages

requirements = [
    "fastapi==0.110.0",
    "websockets==12.0",
    "python-vlc==3.0.20123",
    "python-mpd2==3.1.1",
]

if __name__ == '__main__':

    setup(
        name='radiopi',
        version='0.3.0',
        description='API for your music player.',
        long_description='A simple REST & websocket server to expose a simple API to controll a music player.',
        url='https://github.com/radio-pi/python-websocket-backend',
        author='fliiiix',
        author_email='hi@l33t.name',
        maintainer='fliiiix',
        maintainer_email='hi@l33t.name',
        packages=find_packages(exclude=['*tests*']),
        install_requires=requirements,
        classifiers=[
            'License :: OSI Approved :: BSD License',
            'Operating System :: POSIX',
            'Operating System :: POSIX :: Linux',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: 3.10',
            'Programming Language :: Python :: 3.11',
            'Programming Language :: Python :: 3.12',
            'Programming Language :: Python :: Implementation',
            'Programming Language :: Python :: Implementation :: CPython',
            'Programming Language :: Python :: 3 :: Only',
        ]
)
