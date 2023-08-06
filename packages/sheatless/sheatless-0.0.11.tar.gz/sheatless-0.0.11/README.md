# sheatless - A python library for extracting parts from sheetmusic pdfs

Sheatless, a tool for The Beatless to become sheetless. Written and managed by the web-committee in the student orchestra The Beatless. Soon to be integrated in [taktlaus.no](https://taktlaus.no/).

# API

Currently the entire library has a single entry point function

```python
def processUploadedPdf(pdfPath, imagesDirPath, instruments_file=None, instruments=None, use_lstm=False, tessdata_dir=None):
    ...
	return parts, instrumentsDefaultParts
```

which will be available with

```python
from sheatless import processUploadedPdf
```

Arguments description here:

| Argument         | Optional   | Description                                                                                                      |
| ---------------- | ---------- | ---------------------------------------------------------------------------------------------------------------- |
| pdfPath          |            | Full path to PDF file.                                                                                           |
| imagesDirPath    |            | Full path to output images.                                                                                      |
| instruments_file | (optional) | Full path to instruments file. Accepted formats: YAML (.yaml, .yml), JSON (.json).                               |
| instruments      | (optional) | Dictionary of instruments. Will override any provided instruments file.                                          |
|                  |            | If neither instruments_file nor instruments is provided a default instruments file will be used.                 |
| use_lstm         | (optional) | Use LSTM instead of legacy engine mode.                                                                          |
| tessdata_dir     | (optional) | Full path to tessdata directory. If not provided, whatever the environment variable `TESSDATA_DIR` will be used. |

Returns description here:

| Return                  | Description                                                                                                                       |
| ----------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| parts                   | A list of dictionaries `{ "name": "[name]", "fromPage": i, "toPage": j }` describing each part                                    |
| instrumentsDefaultParts | A dictionary `{ ..., "instrument_i": j, ... }`, where `j` is the index in the parts list for the default part for `instrument_i`. |

# Example docker setup

Sheatless requires tesseract and poppler installed on the system to work. An example docker setup as well as integration of the library can be found in [sheatless-splitter](https://github.com/sigurdo/sheatless-splitter).
