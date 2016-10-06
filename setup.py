import os

from setuptools import setup
from setuptools import find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()


setup(name='lmu.pyramid.chipcard',
      version='0.0.1',
      description='A Webapplication for the LMU Chipcard Project',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
          "Programming Language :: Python",
          "Framework :: Pyramid",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
      ],
      author='',
      author_email='',
      url='',
      keywords='web pyramid pylons',
      packages=find_packages('src', exclude=['ez_setup']),
      namespace_packages=['lmu', 'lmu.pyramid'],
      package_dir={'': 'src'},
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'pyramid',
          'pyramid_chameleon',
          'pyramid_debugtoolbar',
          'ZODB',
          'pyramid_zodbconn',
          'pyramid_tm',
          'waitress',
          'Spyne',
          'suds-py3',
          'lxml',
          'ipython',
          'ipdb',
          'requests',
      ],
      extras_require={
          'test': [
              'WebTest >= 1.3.1',  # py3 compat
              'pytest',  # includes virtualenv
              'pytest-cov',
          ],
          'develop': [
              'ipython',
              'ipdb',
          ]
      },
      dependency_links=[
          #'https://github.com/arskom/spyne.git#egg=Spyne-dev',
          #'https://github.com/cackharot/suds-py3.git#egg=suds-py3-dev',
      ],
      entry_points="""\
      [paste.app_factory]
      main = lmu.pyramid.chipcard:main
      """,
      )
