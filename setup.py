try:
  from setuptools import setup
except ImportError:
  from distutils.core import setup

config = {
  'description': 'MailServer', 
  'author': 'Shal Dengeki', 
  'url': 'https://github.com/shaldengeki/MailServer', 
  'download_url': 'https://github.com/shaldengeki/MailServer', 
  'author_email': 'shaldengeki@gmail.com', 
  'version': '0.1', 
  'install_requires': ['nose'], 
  'packages': ['MailServer'], 
  'scripts': [],
  'name': 'MailServer'
}

setup(**config)