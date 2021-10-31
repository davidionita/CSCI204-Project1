# Our improvements to the project

## Strength & sex on image
  * Using `Pillow` to write a new copy of the image file with the `strength` attribute on top, and `sex` on the bottom
  * When quit is pressed, we clean up these files so that only the base `salmon.ppm`, `bear.ppm`, etc are in the directory

## HTML Output
  * Generates one HTML page per step in ecosystem, with images of residents
### Usage:
  * Choose Y in `main.py` when prompted.

## Makefile
Written for easier testing when not using a full IDE like repl.it
### Usage:
  * `make setup`
  * `make test`

> Note: If you are having trouble using the Makefile, please install dependencies manually by running `pip(3) install -r requirements.txt` (or use a venv). 

> If you're on macOS and having problems finding the module after installation, this is a workaround `python3 -m pip install Pillow` that worked for me.
> 
