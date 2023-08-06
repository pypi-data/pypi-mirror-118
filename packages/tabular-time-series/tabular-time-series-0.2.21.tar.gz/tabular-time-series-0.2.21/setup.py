# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tabular_time_series']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.3.2,<2.0.0', 'pre-commit>=2.14.1,<3.0.0']

setup_kwargs = {
    'name': 'tabular-time-series',
    'version': '0.2.21',
    'description': '',
    'long_description': '# Tabular Time Series\n\n## Summary\n\nThis repo was created as I did not find a function able to transform a time-series (1D) into a tabular format (X, y).\n\n## Usage\n\n### TimeSeriesGenerator\n\nThe docstring is as follows. Given a 1D array `data = [0, 1, 2, 3, 4, 5, 6]`, generates `X, y` following the parameters `p`(autoregressive), `s` (seasonal) and `n` (lenght of y).\n\nTherefore, it makes it possible to train a neural network (e.g.) that 2 autoregressive entries (e.g. `p = 2`) and predicts the next two (`n = 2`) using 2 (`n = 2`) entries with lag 4 (`s = 4`).\n\n```python\n>> data = [0, 1, 2, 3, 4, 5, 6]\n>> p, n = 2, 2\n>> ts = TimeSeriesGenerator(data, p, n)\n>> for X, y in ts:\n...    print(X.shape, y.shape)\n...    print(X, y)\n    [0, 1] [2, 3]\n    [1, 2] [3, 4]\n    [2, 3] [4, 5]\n    [3, 4] [5, 6]\n>> p, n, s = 2, 2, 4\n>> ts = TimeSeriesGenerator(data, p, n, s)\n>> for X, y in ts:\n...    diff = np.where(data == y[0])[0].item() - np.where(data == X[0])[0].item()\n...    print(X.shape, y.shape, diff) == (n + p,) (n,) s\n...    print(X, y)\n    [0, 1, 2, 3] [4, 5]\n    [1, 2, 3, 4] [5, 6]\n```\n\n### get_df\n\nConsidering that many times a batch array is needed for training, `get_df` can be used to generate a `pandas` DataFrame that will contain columns in the format:\n\n- `y(t - 0)`, ..., `y(t - p)` autogressive entries\n- `y(t + 0)`, ..., `y(t + n)` predict entries\n- `y(ts{s}_0})`, ..., `y(ts{s}_n})` seasonal entries\n',
    'author': 'Felipe Whitaker',
    'author_email': 'felipewhitaker@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/felipewhitaker/tabular-time-series',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
