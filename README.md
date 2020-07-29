# Keyword Pattern Generator

Application support two modes:

1. Constructs random documents filled with text pulled from Twitter and Wikipedia and images pulled from Google and print them on multiple printers.
2. Constructs random documents filled with text pulled from Twitter and Wikipedia and images pulled from Google and applies image filters to them.

Generated images are placed in `images` folder.

### Installation

##### Clone the git repository

```
git clone https://github.com/volkmaster/keyword-pattern-generator.git
```

##### Install Python >=3.6

https://www.python.org/downloads/

##### Install Poetry

```
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
```

##### Create virtual environment and activate it

```
python -m venv venv

# OS X / Linux
source venv/bin/activate

# Windows
.\venv\Scripts\activate
```

##### Install dependencies

```
poetry install
```

This will create a new virtual environment and install the dependencies in it.

### Config and run

##### Config

- Copy `.env.example` to `.env` and fill out the listed parameters.
- Copy `serial_number.example` to `serial_number.txt`.

##### Run the program

- Generate a document based on 3 random keywords:

  `python runner.py`

- Generate a document based on up to 5 given keywords (GUI):

  `python ui.py`
