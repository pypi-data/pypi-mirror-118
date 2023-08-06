from distutils.core import setup
setup(
  name = 'pbar_r0cky',         # How you named your package folder (MyLib)
  packages = ['pbar_r0cky'],   # Chose the same as "name"
  version = '0.2',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Simple ProgressBar',   # Give a short description about your library
  author = 'R0cKy',                   # Type in your name
  author_email = 'konrad.soczi@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/R3GG3/pbar_r0cky',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/R3GG3/pbar_r0cky/archive/refs/tags/v0.1.tar.gz',    # I explain this later on
  keywords = ['R0CKY', 'SIMPLE', 'PROGRESSBAR'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
  ],
)
