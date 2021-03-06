from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='checkers',
      version='1.1',
      description='implementation of the game Checkers',
      long_description=readme(),
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Topic :: Game :: Checkers',
      ],
      url='http://github.com/gamda/checkers',
      author='Gamda Software',
      author_email='gamdansoftware@gmail.com',
      license='MIT',
      packages=['checkers'],
      install_requires=[
          'gameboard',
          'pygame'
      ],
      include_package_data=True,
      zip_safe=False,
      test_suite='nose.collector',
      tests_require=['nose'],)