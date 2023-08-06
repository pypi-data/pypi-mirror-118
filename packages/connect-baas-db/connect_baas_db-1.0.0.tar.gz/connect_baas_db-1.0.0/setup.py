from setuptools import setup, find_packages

setup(
    name='connect_baas_db',
    version='1.0.0',
    description='A Python package with the intend of connecting to a Postgres database',
    long_description='This package can be used to simplify connecting to Postgres database and logging to the Postgres database. Furthermore a functionality for opening yaml files has been added. This package has been created for specific purposes',
    url='',
    author='Sander van Dessel',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate you support Python 3. These classifiers are *not*
        # checked by 'pip install'. See instead 'python_requires' below.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
    ],
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.6, <4',
    install_requires=['psycopg2-binary', 'pyyaml']
)
