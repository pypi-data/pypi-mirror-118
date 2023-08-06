from distutils.core import setup
setup(
  name = 'checkwxapi',
  packages = ['checkwxapi'],
  version = '0.0.1-alpha',
  license='Apache 2.0',
  description = 'A wrapper around the CheckWX API',
  author = 'Reydel Leon Machado',
  author_email = 'contact@reydelleon.me',
  url = 'https://github.com/reydelleon/checkwxapi',
  download_url = 'https://github.com/reydelleon/checkwxapi/archive/refs/tags/0.0.1-alpha.tar.gz',
  keywords = ['weather', 'METAR', 'TAF', 'aviation'],
  install_requires=[
          'aiohttp',
          'requests',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: Apache Software License',
    'Programming Language :: Python :: 3'
  ],
)