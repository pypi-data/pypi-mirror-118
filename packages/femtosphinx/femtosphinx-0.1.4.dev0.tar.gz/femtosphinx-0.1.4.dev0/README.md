# femtosphinx
A repository providing some documentation for how to use sphinx.

Also provides the `execute_code` sphinx extension, which can be enabled with: (in `docs/conf.py`)

```python
extensions = [
  ...
  'femtosphinx.execute_code',
  ...
]
```

And then used with the `.. exec::` and `.. exec_as_bullets::` directives.

# Getting started

Install sphinx
```
pip install sphinx
```

Read this [getting started guide](https://www.sphinx-doc.org/en/master/usage/quickstart.html).

Take a look at our [intro guide](https://github.com/femtosense/femtosphinx/blob/main/docs/api.rst).

Start generating documentation!
