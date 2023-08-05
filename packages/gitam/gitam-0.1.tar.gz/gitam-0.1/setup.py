from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

setup_args = dict(
    name='gitam',
    version='0.1',
    description='Useful tools to extract data from GITAM University websites.',
    long_description_content_type="text/markdown",
    long_description=README,
    license='MIT',
    packages=find_packages(),
    author='Rohit Ganji',
    author_email='grohit.2001@gmail.com',
    keywords=['GITAM', 'GITAM University', 'Gandhi Institute of Technology and Management'],
    url='https://github.com/rohitganji/gitam',
    download_url='https://pypi.org/project/gitam/'
)

install_requires = [
    'requests',
    'bs4',
    'pandas',
    'matplotlib',
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)