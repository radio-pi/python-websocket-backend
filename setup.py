from setuptools import setup, find_packages

requirements = [
    "autobahn",
    "Twisted",
    "ujson",
    "python-vlc",
    "python-mpd2",
]

if __name__ == '__main__':

    setup(
        name='radiopi',
        version='0.1.0',
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
            # TODO: decide a licence
            #'License :: OSI Approved :: MIT License',
            'Operating System :: POSIX',
            'Operating System :: POSIX :: Linux',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: Implementation',
            'Programming Language :: Python :: Implementation :: CPython',
            'Programming Language :: Python :: Implementation :: PyPy'
        ]
)