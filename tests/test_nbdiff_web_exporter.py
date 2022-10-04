from nbdiff_web_exporter.nbdiff_web_exporter import generate_url, get_download_file_path


def test_get_download_file_path():
    export_dir = "/data"
    assert get_download_file_path(export_dir) == "/data/diff.html"


def test_generate_url():
    base = "main"
    remote = "test"
    file_path = "notebook.ipynb"
    port = 8080
    assert (
        generate_url(base, remote, file_path, port)
        == "http://127.0.0.1:8080/difftool?base=notebook.ipynb%20(main)&remote=notebook.ipynb%20(test)"
    )
