from setuptools import setup
requires = [
    'beautifulsoup4>=4.9',
    'requests>=2.22',
]
long_desc = "# Unofficial Gutefrage API\n\nIt doesnt have a lot of features yet. Check it out [here](https://github.com/DAMcraft/gutefrage/blob/main/example.py) how it works!"
setup(name='gutefrage',
      version='0.2',
      description='Unofficial GuteFrage api. There is an example file called example.py on how to use it.',
      url='https://github.com/DAMcraft/gutefrage',
      author='DAMcraft',
      author_email='idk@gmail.com',
      license='MIT',
      packages=['gutefrage'],
      zip_safe=False,
      install_requires=requires,
      long_description = long_desc,
      long_description_content_type = "text/markdown")