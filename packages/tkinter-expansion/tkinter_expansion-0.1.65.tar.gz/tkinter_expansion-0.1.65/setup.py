from setuptools import find_packages, setup

with open('README.md') as readme_file:
  readme = readme_file.read()

setup(
  packages=find_packages(),
  name='tkinter_expansion',
  version='0.1.65',
  license='MIT',
  description='Python package that extends tkinter with custom Designer',
  long_description_content_type="text/markdown",
  long_description=readme,
  url="https://fire-the-fox.github.io/tkinter_expansion_docs/",
  download_url="https://github.com/Fire-The-Fox/tkinter_expansion",
  author='Fire-The-Fox',
  author_email='gajdos.jan77@gmail.com',
  keywords=['Tkinter', 'expansion', 'designer', 'themes'],
  classifiers=[
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9'
  ],
)
