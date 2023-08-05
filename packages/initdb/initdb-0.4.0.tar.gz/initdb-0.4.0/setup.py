import setuptools

setuptools.setup(
    name="initdb",
    version="0.4.0",
    author='Eugen Ciur',
    author_email='eugen@papermerge.com',
    url='https://github.com/papermerge/initdb',
    description="Small package that creates a user"
    " and database owned by that user.",
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        'psycopg2 == 2.9.1',
    ],
)
