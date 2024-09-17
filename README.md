# FlashCardGenerator

FlashCardGenerator is a Python library for creating customizable flashcards in PDF format. It's designed to be easy to use while offering flexibility in flashcard design and layout.

## Features

- Create double-sided flashcards with customizable content
- Support for additional information on the front of the card
- Markdown-style formatting (bold, italic, underline)
- Configurable card layout (size, number per row, etc.)
- PDF output for easy printing and sharing

## Installation

To install FlashCardGenerator, run the following command:

```bash
pip install flashcard-generator
```

## Quick Start

Here's a simple example to get you started:

```python
from flashcard_generator import FlashCardGenerator

generator = FlashCardGenerator()
generator.set_filename("my_flashcards.pdf") \
         .add_entry("Bonjour", "Hello", "Casual greeting") \
         .add_entry("Merci", "Thank you", "**Important** phrase") \
         .add_entry("Au revoir", "Goodbye", "*Formal* farewell") \
         .generate()
```

This will create a PDF file named "my_flashcards.pdf" with three flashcards.

## API Usage

### Creating a FlashCardGenerator

```python
generator = FlashCardGenerator()
```

### Configuration Methods

- `set_filename(filename: str) -> Self`: Set the output PDF filename
- `set_cards_per_row(count: int) -> Self`: Set the number of cards per row
- `set_page_size(size: tuple) -> Self`: Set the page size (default is A4)
- `set_margins(top: float, bottom: float) -> Self`: Set top and bottom margins
- `set_card_height(height: float) -> Self`: Set the height of each card

### Adding Entries

```python
generator.add_entry(original: str, translation: str, extra: str = "") -> Self
```

- `original`: The text on the front of the card
- `translation`: The text on the back of the card
- `extra`: Additional information to display on the front (optional)

### Generating the PDF

```python
generator.generate()
```

This method creates the PDF file with all the added flashcards.

## Markdown Formatting

You can use basic Markdown formatting in your flashcard text:

- `**bold**` for **bold** text
- `*italic*` for *italic* text
- `__underline__` for __underlined__ text

## Example

Here's a more detailed example showcasing various features:

```python
from flashcard_generator import FlashCardGenerator
from reportlab.lib.units import cm

generator = FlashCardGenerator()
generator.set_filename("language_flashcards.pdf") \
         .set_cards_per_row(4) \
         .set_card_height(2.5*cm) \
         .add_entry("Bonjour", "Hello", "Casual greeting") \
         .add_entry("Merci", "Thank you", "**Important** phrase") \
         .add_entry("Au revoir", "Goodbye", "*Formal* farewell") \
         .add_entry("S'il vous plaît", "Please", "__Polite__ request") \
         .add_entry("Oui", "Yes") \
         .add_entry("Non", "No") \
         .generate()
```

This will create a PDF with 4 cards per row, each card 2.5 cm high, and include 6 flashcards with various formatting styles.

## Contributing

Contributions to FlashCardGenerator are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.