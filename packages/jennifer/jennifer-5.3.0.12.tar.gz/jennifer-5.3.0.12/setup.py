import os
import jennifer
from distutils.command.sdist import sdist as _sdist
from setuptools import setup, find_packages


class sdist(_sdist):
    def run(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        support_platforms = [
            ['darwin', 'amd64'],
            ['linux', 'amd64'],
        ]
        os.system('rm -rf %s/jennifer/bin' % dir_path)
        for platform in support_platforms:
            os.system(
                ("{0}/scripts/build_gateway.sh {1} {2}").format(
                    dir_path,
                    platform[0],
                    platform[1],
                )
            )
        _sdist.run(self)

def readme():
    with open('README.rst', 'rb') as f:
        return f.read().decode('utf-8')


setup(
    name="jennifer",
    description="JENNIFER, JenniferSoft APM, python agent.",
    long_description=readme(),
    cmdclass={'sdist': sdist},
    version=jennifer.__version__,
    author=jennifer.__author__,
    author_email="python@jennifersoft.com",
    url="http://jennifersoft.com",
    license="Proprietary",
    packages=find_packages(exclude=[]),
    package_data={
        'jennifer': ['bin/*/*/jennifer_agent'],
    },
    entry_points = {
        'console_scripts': [
            'jennifer-admin = jennifer.admin:main',
        ],
    },
    classifiers=[
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
        'License :: Other/Proprietary License',
    ],
)
