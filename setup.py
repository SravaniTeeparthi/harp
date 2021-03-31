from setuptools import setup

setup(
  name='harp',
  version='0.0.1',
  author='Human Activity Recognition Proposals',
  author_email='sssravani4@gmail.com',
  packages=['harp'],
  url='',
  license='',
  description='',
  long_description=open('README.md').read(),
  install_requires=[
      "tqdm",
      "pytest",
      "opencv-python",
      "opencv-contrib-python",
      "pandas",
      "numpy",
      "scikit-video",
      "word2number"
  ],
)
