#!/usr/bin/env python3

# Set the constants below to change where this script saves things.
# This script requires the `minify_html` python package to work. Please install it with the following command:
# `pip install minify_html`

try:
    import minify_html
except ImportError:
    print("\033[31mPlease run `pip install minify_html` to use this script!\033[0m")
    exit(1)
import shutil
import gzip

# The path to the html file
HTML_FILE_PATH = r"app.html"
# Path to write the minified file to
MINIFIED_HTML_PATH = r"app.min.html"
# Path to write the compressed file to
COMPRESSED_HTML_PATH = r"app.html.gz"
# Path to write the C++ constants to
CAMERA_INDEX_FILE = r"camera_index.h"
# ID for length definition
LEN_ID = "index_html_gz_len"
# ID for compressed array constant
ARR_ID = "index_html_gz"

def compress():
    with open(HTML_FILE_PATH, "r", encoding="utf-8") as orig:
        print("minifying...")
        minified = minify_html.minify(orig.read(), minify_css=True, minify_js=True)
    with open(MINIFIED_HTML_PATH, "wb+") as f_in:
        print("encoding...")
        f_in.write(minified.encode("utf-8"))
        f_in.flush()
        f_in.seek(0)
        with gzip.open(COMPRESSED_HTML_PATH, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)
    with open(COMPRESSED_HTML_PATH, "rb") as compressed:
        bytes = compressed.read()

    with open(CAMERA_INDEX_FILE, "w") as camera_index:
        print("writing...")
        camera_index.write(f"#define {LEN_ID} {len(bytes)}\n")
        camera_index.write(f"const unsigned char {ARR_ID}[] = {{")
        for byte in bytes:
            camera_index.write(f"0x{byte:02X},")
        camera_index.write("};")

if __name__ == "__main__":
    compress()