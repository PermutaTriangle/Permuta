import os
import tempfile
import threading
import time
import webbrowser
from typing import ClassVar


class HTMLViewer:
    """A class for opening html text in browser."""

    _THREAD_WAIT_TIME: ClassVar[float] = 5  # seconds

    @staticmethod
    def _remove_file_thread(fname: str) -> None:
        time.sleep(HTMLViewer._THREAD_WAIT_TIME)
        if os.path.exists(fname):
            os.remove(fname)

    @staticmethod
    def _remove_file(fname: str) -> None:
        threading.Thread(target=HTMLViewer._remove_file_thread, args=(fname,)).start()

    @staticmethod
    def open_html(html: str) -> None:
        """Open and render html string in browser."""
        with tempfile.NamedTemporaryFile(
            "r+", suffix=".html", delete=False
        ) as html_file:
            html_file.write(html)
            webbrowser.open_new_tab(f"file://{html_file.name}")
            HTMLViewer._remove_file(html_file.name)

    @staticmethod
    def open_svg(svg: str) -> None:
        """Open and render svg image string in browser."""
        HTMLViewer.open_html(f"<html><body>{svg}</body></html>")
