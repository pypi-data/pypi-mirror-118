from setuptools import setup, find_packages
import os

BASE_DIR = os.path.realpath(os.path.dirname(__file__))
VERSION = '1.10.4'


def parse_requirements():
    reqs = []
    if os.path.isfile(os.path.join(BASE_DIR, 'requirements.txt')):
        with open(os.path.join(BASE_DIR, 'requirements.txt'), 'r') as fd:
            for line in fd.readlines():
                line = line.strip()
                if line:
                    reqs.append(line)
    return reqs


def get_description():
    with open(os.path.join(BASE_DIR, 'README.md'), 'r') as fh:
        return fh.read()


if __name__ == '__main__':
    setup(
        version=VERSION,
        name='pymobiledevice3',
        description='Pure python3 implementation for working with iDevices (iPhone, etc...)',
        long_description=get_description(),
        long_description_content_type='text/markdown',
        cmdclass={},
        packages=find_packages(),
        package_data={'': ['*.txt', '*.TXT', '*.json'], },
        data_files=[('.', ['requirements.txt'])],
        author='DoronZ',
        install_requires=parse_requirements(),
        entry_points={
            'console_scripts': ['pymobiledevice3=pymobiledevice3.__main__:cli',
                                ],
        },
        classifiers=[
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
        ],
        url='https://github.com/doronz88/pymobiledevice3',
        project_urls={
            'pymobiledevice3': 'https://github.com/doronz88/pymobiledevice3'
        },
        tests_require=['pytest'],
    )
