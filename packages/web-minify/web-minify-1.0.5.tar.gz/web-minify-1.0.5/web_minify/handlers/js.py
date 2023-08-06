from jsbeautifier.javascript.options import BeautifierOptions
from jsbeautifier.javascript.beautifier import Beautifier


def js_minify(js, settings: dict):
    """Minify JS main function."""
    b = Beautifier()
    opts = BeautifierOptions()
    jsb.beautify(js, opts)
    return js, None
