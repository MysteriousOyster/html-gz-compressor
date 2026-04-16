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
# Path to write the C++ constants to. Make blank to not save.
CAMERA_INDEX_FILE = r"camera_index.h"
# ID for length definition
LEN_ID = "index_html_gz_len"
# ID for compressed array constant
ARR_ID = "index_html_gz"

def compress(html_file_path: str, minified_html_path: str, compressed_html_path: str, camera_index_file: str):
    with open(html_file_path, "r", encoding="utf-8") as orig:
        print("minifying...")
        minified = minify_html.minify(orig.read(), minify_css=True, minify_js=True)
    with open(minified_html_path, "wb+") as f_in:
        print("encoding...")
        f_in.write(minified.encode("utf-8"))
        f_in.flush()
        f_in.seek(0)
        with gzip.open(compressed_html_path, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)
    with open(compressed_html_path, "rb") as compressed:
        bytes = compressed.read()

    if camera_index_file != "":
        with open(camera_index_file, "w") as camera_index:
            print("writing...")
            camera_index.write(f"#define {LEN_ID} {len(bytes)}\n")
            camera_index.write(f"const unsigned char {ARR_ID}[] = {{")
            for byte in bytes:
                camera_index.write(f"0x{byte:02X},")
            camera_index.write("};")

if __name__ == "__main__":
    compress(HTML_FILE_PATH, MINIFIED_HTML_PATH, COMPRESSED_HTML_PATH, CAMERA_INDEX_FILE)