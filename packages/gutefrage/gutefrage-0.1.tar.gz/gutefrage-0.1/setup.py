from setuptools import setup
requires = [
    'beautifulsoup4>=4.9',
    'requests>=2.22',
]
setup(name='gutefrage',
      version='0.1',
      description='Unofficial GuteFrage api. There is an example file called example.py on how to use it.',
      url='https://github.com/DAMcraft/gutefrage',
      author='DAMcraft',
      author_email='idk@gmail.com',
      license='MIT',
      packages=['gutefrage'],
      zip_safe=False,
      install_requires=requires)