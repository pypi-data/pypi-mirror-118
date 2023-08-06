# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['combinatorial_gwas',
 'combinatorial_gwas.phenotypes',
 'combinatorial_gwas.training']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.4,<4.0.0',
 'apricot-select>=0.6.1,<0.7.0',
 'bgen-reader>=4.0.7,<5.0.0',
 'bokeh>=2.3.1,<3.0.0',
 'colorcet>=2.0.6,<3.0.0',
 'datashader>=0.12.1,<0.13.0',
 'deeplift>=0.6.13,<0.7.0',
 'fastparquet>=0.5.0,<0.6.0',
 'holoviews>=1.14.3,<2.0.0',
 'hydra-core==1.1.0.dev5',
 'keras-tuner>=1.0.2,<2.0.0',
 'matplotlib>=3.4.1,<4.0.0',
 'pandas>=1.2.4,<2.0.0',
 'pca>=1.4.0,<2.0.0',
 'pydantic>=1.8.1,<2.0.0',
 'requests>=2.25.1,<3.0.0',
 'scikit-image>=0.18.1,<0.19.0',
 'seaborn>=0.11.1,<0.12.0',
 'shap>=0.39.0,<0.40.0',
 'statsmodels>=0.12.2,<0.13.0',
 'umap-learn>=0.5.1,<0.6.0']

setup_kwargs = {
    'name': 'combinatorial-gwas',
    'version': '0.2.0',
    'description': "A package for the final project of MIT's 6.874 class Deep Learning in Life Science",
    'long_description': None,
    'author': 'anhoang',
    'author_email': 'anhoang@wi.mit.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.9',
}


setup(**setup_kwargs)
