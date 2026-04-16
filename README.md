# html-gz-compressor

This python script compresses an html page down into a usable .gz file and into the `camera_index.h` file for microcontrollers. You can use it to cut down on used flash space, and to modify the existing CameraWebServer code.

## General Usage

Run `pip install minify_html` to install. This project uses the uv package manager out of ease, but if using with PlatformIO this probably won't work.

Since this is a relatively simple script and I couldn't be bothered to make multiple html pages for the different camera models like in the `camera_index.h`. You should just be able to just replace the original `camera_index.h` file in the CameraWebServer example. Then, after that, replace the `index_handler` function in `app_httpd.cpp` with the follwing:

```cpp
static esp_err_t index_handler(httpd_req_t *req) {
  httpd_resp_set_type(req, "text/html");
  httpd_resp_set_hdr(req, "Content-Encoding", "gzip");
  return httpd_resp_send(req, (const char *)index_html_gz, index_html_gz_len);
}
```

## Usage with PlatformIO

To use this script with PlatformIO, there are a few hoops to jump through. Because `minify_html` requires some odd dependency that PIO's python can't handle (at least for me), you'll have to add another script to run it with your system python. That is located at `pre.py`. To add to PlatformIO, add the following to your environment in the ini file:

```ini
; platformio.ini
; [env:<some board>] should go somewhere before this
extra_scripts = pre:pre.py
```

You will have to add `pre.py` and `compressor.py` to your project somewhere, and update the path in `pre.py` to where you put `compressor.py`.
