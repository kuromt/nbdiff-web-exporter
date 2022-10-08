import argparse
import os
import socket
import sys
import time
from logging import getLogger
from multiprocessing import Process
from os.path import abspath
from shutil import move
from urllib import parse

from nbdime.args import add_web_args
from nbdime.webapp.nbdiffweb import (
    ConfigBackedParser,
    add_diff_args,
    add_generic_args,
    main_diff,
)

from .ops_browser import close, connect, export

logger = getLogger(__name__)

DOWNLOADED_FILE = "diff.html"


def dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)


def add_exporter_args(parser):
    parser.add_argument(
        "--timeout",
        default=10,
        type=int,
        help="timeout seconds waiting for operating nbdiff-web.",
    )
    parser.add_argument(
        "--export-dir",
        default="diff",
        required=True,
        type=dir_path,
        help="directory for saving diff file.",
    )
    return


def build_arg_parser():
    """
    Wrap nbdime.webapp.nbdiffweb.bui;d_arg_parser for nbdiff-web-exporter.
    """
    description = "Difftool for Nbdime."
    parser = ConfigBackedParser(description=description, add_help=True)
    add_exporter_args(parser)
    add_generic_args(parser)
    add_web_args(parser, 8888)
    add_diff_args(parser)
    parser.add_argument(
        "base",
        help="The base notebook filename OR base git-revision.",
        nargs="?",
        default="HEAD",
    )
    parser.add_argument(
        "remote",
        help="The remote modified notebook filename OR remote git-revision.",
        nargs="?",
        default=None,
    )
    parser.add_argument(
        "paths",
        help="Filter diffs for git-revisions based on path",
        default=None,
    )
    return parser


def get_download_file_path(export_dir: str):
    return os.path.join(export_dir, DOWNLOADED_FILE)


def move_file(export_dir, file_path: str):
    diff_file_path = get_download_file_path(export_dir)
    if not os.path.exists(diff_file_path):
        raise FileNotFoundError(f"diff file is not found: {os.path.abspath(diff_file_path)}")
    # split filename and extention
    file_name, _ = os.path.splitext(file_path)
    move_path = abspath(os.path.join(abspath(export_dir), file_name + ".html"))
    logger.info(f"move file: {diff_file_path} to {move_path}")
    # make directory is not exist
    move_file_dir = os.path.dirname(move_path)
    os.makedirs(move_file_dir, exist_ok=True)
    move(diff_file_path, move_path)
    return


def generate_url(base, remote, file_path: str, port: int):
    # NOTE: nbdiff-web uses encodeURICompoenent() for url encoding. This encodes '/' to '%2F'.
    # We should take care of behabior of encoding.
    encoded_base_file_path = parse.quote(f"{file_path} ({base})", safe="()")
    encoded_remote_file_path = parse.quote(f"{file_path} ({remote})", safe="()")
    return f"http://127.0.0.1:{port}/difftool?base={encoded_base_file_path}&remote={encoded_remote_file_path}"


def run_nbdiff_web_server(nbdiff_web_opts: argparse.Namespace):
    logger.info("run nbdiff-web")
    nbdiff_web_process = Process(
        target=main_diff,
        args=[
            nbdiff_web_opts,
        ],
    )
    nbdiff_web_process.start()
    return nbdiff_web_process


def wait_for_ready(port, timeout):
    count = 0
    for count in range(timeout):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                logger.info(f"try to access nbdiff-web: retry {count}")
                sock.connect(("localhost", port))
                return
            except Exception:
                time.sleep(1)
        if count > timeout:
            logger.error("failed to run nbdiff-web server.")
            sys.exit(1)
    return


def wait_for_downloaded(file_path, timeout):
    wait_seconds = 0
    while wait_seconds < timeout:
        if os.path.isfile(file_path):
            return
        logger.info("waiting for complete downloading...")
        time.sleep(0.5)
        wait_seconds += 0.5
    raise TimeoutError("download failed in timeout.")


def export_diff(
    base,
    remote,
    export_dir: str,
    port,
    timeout: int,
    nbdiff_web_opts: argparse.Namespace,
):
    file_path = nbdiff_web_opts.paths
    nbdiff_web_url = generate_url(base, remote, file_path, port)
    logger.info(f"nbdiff-web url: {nbdiff_web_url}")
    # run nbdiff-web
    nbdiff_web_process = run_nbdiff_web_server(nbdiff_web_opts)
    # wait_for_ready
    wait_for_ready(port, timeout)

    driver = connect(nbdiff_web_url, export_dir)

    # download diff file as html
    logger.info(f"export diff of {file_path}.")
    export(driver, timeout)
    # wait for file downloaded
    downloaded_file_path = get_download_file_path(export_dir)
    wait_for_downloaded(downloaded_file_path, timeout)
    # move exported files
    move_file(export_dir, file_path)
    # close nbdiff-web
    logger.info("close nbdiff-web window.")
    close(driver, timeout)
    nbdiff_web_process.join()
    logger.info("quit WebDriver.")
    driver.quit()
    return


def cli(args=None):
    if args is None:
        args = sys.argv[1:]
    nbdiff_web_opts = build_arg_parser().parse_args(args)

    base = nbdiff_web_opts.base
    remote = nbdiff_web_opts.remote
    port = nbdiff_web_opts.port
    timeout = nbdiff_web_opts.timeout
    export_dir = abspath(nbdiff_web_opts.export_dir)
    # delete unnecessary args for nbdiff-web
    nbdiff_web_opts.__delattr__("timeout")
    nbdiff_web_opts.__delattr__("export_dir")

    export_diff(base, remote, export_dir, port, timeout, nbdiff_web_opts)
    return


if __name__ == "__main__":
    cli()
