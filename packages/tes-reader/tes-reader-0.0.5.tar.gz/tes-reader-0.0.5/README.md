# The Elder Scrolls Files Reader
A reader for The Elder Scrolls files.

## Minimal Example - Print the Number of Books
```
from tes_reader import Reader

game_folder = 'C:\\Program Files (x86)\\Steam\\steamapps\\common\\Skyrim Special Edition\\'

with Reader(os.path.join(game_folder, 'Data', 'Skyrim.esm')) as skyrim_main_file:
    print(len(skyrim_main_file['BOOK']))
```

## Installation

```
pip install tes-reader
```
## Requirements
* Python 3.5
* pip (Package manager for Python)
* Windows
* An Elder Scrolls Game - for example, Skyrim.

## Development and Testing

In addition to the requirements above, you will need a github.com account.

Clone from github using `git clone git@github.com:sinan-ozel/tes-reader.git`

To test, go into the tests folder `cd tests` and run `pytest`
