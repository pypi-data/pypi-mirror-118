# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tocase']

package_data = \
{'': ['*']}

install_requires = \
['regex']

setup_kwargs = {
    'name': 'tocase',
    'version': '1.0.0',
    'description': 'tocase provides an API to recase string into any case',
    'long_description': '[![PyPI Version][pypi-image]][pypi-url]\n[![Build Status][build-image]][build-url]\n\n<!-- Badges -->\n\n[pypi-image]: https://img.shields.io/pypi/v/tocase\n[pypi-url]: https://pypi.org/project/tocase/\n[build-image]: https://github.com/fbraza/tocase/actions/workflows/ci.yml/badge.svg\n[build-url]: https://github.com/fbraza/tocase/blob/master/.github/workflows/ci.yml\n\n![](assets/banner_ToCase.png)\n\n## Functionality\n\n`tocase` leverages the `regex` library to convert your strings into any case.\n\n## Setup\n\nTo install the package run the following command:\n\n```bash\npip install tocase\n```\n\nOnce installed, import the `for_strings` if you want to use the basic API to recase strings. Import the `for_pandas` modules to use the pandas API to recase column names and column values.\n\n```python\nimport tocase.tocase.for_strings.ToCase as ToCase\nimport tocase.tocase.for_pandas\n```\n\n## Usage\n\n### Camel\n\nIt is a naming convention where the first letter in compound words is capitalized, except for the first one.\n\n```python\n# Example with simple string\nTocase("camel-case").camel() # ==> camelCase\nTocase("camel case").camel() # ==> camelCase\n```\n\n### Constant\n\nIt is a naming convention where all letters in compound words are capitalized. Words are joined with an underscore.\n\n```python\n# Example with simple string\nTocase("Constant-case").constant() # ==> CONSTANT_CASE\nTocase("constant Case").constant() # ==> CONSTANT_CASE\n```\n\n### Dot\n\nIt is a naming convention where all letters in compound words are lowercased. Words are joined with a dot.\n\n```python\n# Example with simple string\nTocase("Dot-case").dot() # ==> dot.case\nTocase("dot Case").dot() # ==> dot.case\n```\n\n### Header\n\nIt is a naming convention where the first letter in compound words is capitalized. Words are joined by a dash.\n\n```python\n# Example with simple string\nTocase("Header-case").header() # ==> Header-Case\nTocase("header Case").header() # ==> Header-Case\n```\n\n### Kebab\n\nIt is a naming convention where all letters in compound words are lowercased. Words are joined by a dash.\n\n```python\n# Example with simple string\nTocase("Kebab-case").kebab() # ==> kebab-case\nTocase("kebab Case").kebab() # ==> kebab-case\n```\n\n### Pascal\n\nIt is a naming convention where the first letter in compound words is capitalized.\n\n```python\n# Example with simple string\nTocase("Pascal-case").pascal() # ==> PascalCase\nTocase("pascal Case").pascal() # ==> PascalCase\n```\n\n### Snake\n\nIt is a naming convention where all letters in compound words are lowercased. Words are joined by an underscore.\n\n```python\n# Example with simple string\nTocase("Snake-case").snake() # ==> snake_case\nTocase("snake Case").snake() # ==> snake_case\n```\n\n### Title\n\nIt is a naming convention where the first letter in compound words is capitalized. Words are separated by a space.\n\n```python\n# Example with simple string\nTocase("Title-case").title() # ==> "Title Case"\nTocase("title Case").title() # ==> "Title Case"\n```\n\n### With pandas DataFrames\n\nYou can work with pandas DataFrame to recase columns names or column values. See the following examples with fake data.\n\n```python\ncolumns = ["first name", "last name", "age", "family doctor"]\nvalues = [\n        ["Jules", "Otti", 35, "Dr James Porter"],\n        ["Marie", "Curie", 22, "Dr Vicky Laporte"],\n        ["Marc", "El Bichon", 35, "Dr Hyde Frank"]\n        ]\ndata =  pd.DataFrame(data=values, columns=columns)\n```\n\nTo recase columns names, use the `col` DataFrame accessor and the appropriate recasing function described above.\n\n```python\nprint(data)\n\n"""\n  first name last name  age   family doctor\n0      Jules      Otti   35   DrJamesPorter\n1      Marie     Curie   22  DrVickyLaporte\n2       Marc  ElBichon   35     DrHydeFrank\n\n"""\n\nprint(data.col.constant())\n\n"""\n  FIRST_NAME LAST_NAME  AGE   FAMILY_DOCTOR\n0      Jules      Otti   35   DrJamesPorter\n1      Marie     Curie   22  DrVickyLaporte\n2       Marc  ElBichon   35     DrHydeFrank\n"""\n```\n\nTo recase columns values, use the `val` DataFrame accessor, the appropriate recasing function described above with a list of the columns to be processed.\n\n```python\ncolumns_to_process = ["first name", "last name", "family doctor"]\nprint(data.val.constant(columns_to_process))\n\n"""\n  first name  last name  age     family doctor\n0      JULES       OTTI   35   DR_JAMES_PORTER\n1      MARIE      CURIE   22  DR_VICKY_LAPORTE\n2       MARC  EL_BICHON   35     DR_HYDE_FRANK\n\n"""\n```\n\n## For developers\n\nClone or download the repository on your machine. If you have `poetry` installed just run the following command to restore the working environment:\n\n```bash\npoetry install\n```\n\nIf you don\'t have `poetry` you can use `pip` and the `requirements.txt` file:\n\n```bash\npip install -r requirements.txt\n```\n\nTo run tests, stay at the root of the directory and run:\n\n```bash\npytest -v\n```\n\nAll contributions are more than welcome. So feel free to to make a PR.\n\n## Author\n\nFaouzi Braza\n',
    'author': 'fbraza',
    'author_email': 'fbraza@tutanota.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fbraza/toCase',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.9,<4.0.0',
}


setup(**setup_kwargs)
