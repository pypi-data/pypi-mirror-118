from setuptools import setup

name = "types-dateparser"
description = "Typing stubs for dateparser"
long_description = '''
## Typing stubs for dateparser

This is a PEP 561 type stub package for the `dateparser` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `dateparser`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/dateparser. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `2d4fcbc81e0ddd813ae85c44ac8e906520b89044`.
'''.lstrip()

setup(name=name,
      version="1.0.2",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=[],
      packages=['dateparser-stubs', 'dateparser_data-stubs'],
      package_data={'dateparser-stubs': ['freshness_date_parser.pyi', 'parser.pyi', 'timezone_parser.pyi', 'date.pyi', '__init__.pyi', 'conf.pyi', 'date_parser.pyi', 'timezones.pyi', 'search/search.pyi', 'search/text_detection.pyi', 'search/__init__.pyi', 'search/detection.pyi', 'calendars/hijri.pyi', 'calendars/__init__.pyi', 'calendars/jalali.pyi', 'calendars/hijri_parser.pyi', 'calendars/jalali_parser.pyi', 'languages/validation.pyi', 'languages/__init__.pyi', 'languages/loader.pyi', 'languages/locale.pyi', 'languages/dictionary.pyi', 'utils/__init__.pyi', 'utils/strptime.pyi', 'data/__init__.pyi', 'data/languages_info.pyi', 'METADATA.toml'], 'dateparser_data-stubs': ['__init__.pyi', 'settings.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Typed",
      ]
)
