from setuptools import setup

setup(
  name = 'vcspack300',           # pip install <name>
  packages = ['vcspack301'],      # packages to be installed  
  version = '0.1',              

  description = 'vcspack utilities',   # text description
  license='MIT',        # Chose a license from here: 
                        # https://opensource.org/licenses

  author = 'rahul',
  author_email = 'rahulst117@gmail.com',
  setup_requires=['wheel'],
)
