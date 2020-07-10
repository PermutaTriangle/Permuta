import tempfile
import webbrowser


class HTMLViewer:
    @staticmethod
    def open_html(html: str) -> None:
        with tempfile.NamedTemporaryFile("r+", suffix=".html", delete=False) as f:
            f.write(html)
            webbrowser.open_new_tab(f"file://{f.name}")

    @staticmethod
    def open_svg(svg: str) -> None:
        HTMLViewer.open_html(f"<html><body>{svg}</body></html>")
