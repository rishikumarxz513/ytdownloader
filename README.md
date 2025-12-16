# Foobar

Foobar is a Python library for dealing with word pluralization and singularization, offering robust support for English irregular and standard forms.

Table of Contents
🌟 Installation

📖 Usage

🤝 Contributing

⚖️ License

📧 Contact

## Installation

Use the package manager pip to install foobar.

```bash
pip install foobar
```

## Usage
This library exposes two primary functions: pluralize() and singularize().
```python
import foobar

# returns 'words'
foobar.pluralize('word')

# returns 'geese'
foobar.pluralize('goose')

# returns 'phenomenon'
foobar.singularize('phenomena')

# returns 'data' (handles common irregular plural forms)
foobar.pluralize('datum')
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate to maintain coverage and stability.

## License

[MIT](https://choosealicense.com/licenses/mit/)
