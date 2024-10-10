from setuptools import setup, find_packages


setup(
    name='python-task',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pyspark',
        'flask'
    ],
    author='Nicola Pagliarulo',
    author_email='nicola.pagliarulo200@gmail.com',
    url='https://github.com/NicolaPagliarulo/tasks',
    license='MIT',
)
