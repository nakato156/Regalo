from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
    readme = f.read()

setup(
    name='Regalo',
    version='0.4.2',
    license='MIT',
    description='Creador de instaladores para windows',
    long_description_content_type="text/markdown",
    long_description=readme,
    author='Nakato',
    author_email='christianvelasces@gmail.com',
    url='https://github.com/nakato156/Regalo',
    keywords=['windows', 'installer', 'exe', "executable", "package"],
    packages=find_packages(),
)