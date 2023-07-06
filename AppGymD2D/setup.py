from setuptools import setup, find_packages


setup(
    name='AppGymD2D',
    version='0.0.1',
    description='Application based Mobile D2D Communication underlay Cellulat Network',
    keywords='open ai gym environment rl agent d2d cellular offload resource allocation',
    url='https://github.com/Suvadip-B/AppGymD2D',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=['gym>=0.9.6', 'numpy'],
    extras_require={
        'dev': ['flake8', 'pytest', 'pytest-cov', 'pytest-sugar']
    },
    clasifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
