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
$ nbdiff-web-exporter --export-dir ./export-data --port 8080  main branch1 data/notebook.ipynb 
```

nbdiff-web-exporter save diff as html file in export-dir.

```bash
$ ls ls export-data/data/notebook.html 
export-data/data/notebook.html
```

To view diff file in your browser, run open command.

```bash
$ open export-data/data/notebook.html
```

nbdiff-web-exporter support almost options of nbdiff-web. To make simple diff, run with `-m` option.

```
$ nbdiff-web-exporter --help
usage: nbdiff-web-exporter [-h] [--timeout TIMEOUT] --export-dir EXPORT_DIR [--version] [--config]
                           [--log-level {DEBUG,INFO,WARN,ERROR,CRITICAL}] [-p PORT] [-b BROWSER] [--persist] [--ip IP]
                           [-w WORKDIRECTORY] [--base-url BASE_URL] [--show-unchanged] [-s] [-o] [-a] [-m] [-i] [-d]
                           [base] [remote] paths

Difftool for Nbdime.

positional arguments:
  base                  The base notebook filename OR base git-revision.
  remote                The remote modified notebook filename OR remote git-revision.
  paths                 Filter diffs for git-revisions based on path

optional arguments:
  -h, --help            show this help message and exit
  --timeout TIMEOUT     timeout seconds waiting for operating nbdiff-web.
  --export-dir EXPORT_DIR
                        directory for saving diff file.
  --version             show program's version number and exit
  --config              list the valid config keys and their current effective values
  --log-level {DEBUG,INFO,WARN,ERROR,CRITICAL}
                        set the log level by name.
  -p PORT, --port PORT  specify the port you want the server to run on. Default is 8888.
  -b BROWSER, --browser BROWSER
                        specify the browser to use, to override the system default.
  --persist             prevent server shutting down on remote close request (when these would normally be supported).
  --ip IP               specify the interface to listen to for the web server. NOTE: Setting this to anything other than
                        127.0.0.1/localhost might comprimise the security of your computer. Use with care!
  -w WORKDIRECTORY, --workdirectory WORKDIRECTORY
                        specify the working directory you want the server to run from. Default is the actual cwd at program start.
  --base-url BASE_URL   The base URL prefix under which to run the web app
  --show-unchanged      show unchanged cells by default

ignorables:
  Set which parts of the notebook (not) to process.

  -s, --sources, -S, --ignore-sources
                        process/ignore sources.
  -o, --outputs, -O, --ignore-outputs
                        process/ignore outputs.
  -a, --attachments, -A, --ignore-attachments
                        process/ignore attachments.
  -m, --metadata, -M, --ignore-metadata
                        process/ignore metadata.
  -i, --id, -I, --ignore-id
                        process/ignore identifiers.
  -d, --details, -D, --ignore-details
                        process/ignore details not covered by other options.
```
