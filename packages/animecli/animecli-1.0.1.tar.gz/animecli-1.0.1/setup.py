from setuptools import setup
import pathlib

here = pathlib.Path(__file__).parent.resolve()

setup(name='animecli',
      version='1.0.1',
      description='animecli is a tool to retrieve all information about your favourite anime in the comfort of your terminal, using the jikan.moe API.',
      long_description_content_type='text/markdown',
      long_description = (here / 'README.md').read_text(encoding='utf-8'),
      url='https://github.com/ryanvij/animecli',
      author='ryanvij',
      author_email='ryan.vijay2006@gmail.com',
      license='MIT',
      entry_points={
        'console_scripts': ['animecli=animecli.retrieve:main']
      },
      packages=['animecli'],
      include_package_data=True,
      install_requires=["requests", "bs4", "rich"],
      zip_safe=False)
