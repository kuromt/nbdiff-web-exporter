# nbdiff-web-exporter

nbdiff-web-exporter is wrapper tool of [nbdiff-web](https://nbdime.readthedocs.io/en/latest/).

nbdiff-web-exporter exports diff of notebook files as a html file.

# requirement

- install [Chrome WebDriver](https://chromedriver.chromium.org/downloads) in PATH.

# How to Install

```bash
$ pip install git+https://github.com/kuromt/nbdiff-web-exporter
```

# How to run

```bash
$ mkdir ./export-data
$ nbdiff-web-exporter --export-dir ./export-data --port 55139  master branch1 data/notebook.ipynb 
```

Then, diff is saved as html file.

```bash
$ ls export-data/
notebook.html
```

To show in your browser, run open command.

```bash
$ open export-data/notebook.html 
```
