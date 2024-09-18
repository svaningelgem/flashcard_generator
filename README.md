# FlashCardGenerator

FlashCardGenerator is a Python library for creating customizable flashcards in PDF format. It's designed to be easy to use while offering flexibility in flashcard design and layout.

## Features

- Create double-sided flashcards with customizable content
- Support for additional information and an index on the front of the card
- Markdown-style formatting (bold, italic, underline)
- Automatic text wrapping and resizing to fit content
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
         .add_entry("Bonjour", "Hello", extra="Casual greeting", index="1") \
         .add_entry("Merci", "Thank you", extra="**Important** phrase", index="2") \
         .add_entry("Au revoir", "Goodbye", extra="*Formal* farewell", index="3") \
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
- `set_margins(top: float, bottom: float, left: float, right: float) -> Self`: Set page margins
- `set_card_height(height: float) -> Self`: Set the height of each card

### Adding Entries

```python
generator.add_entry(original: str, translation: str, extra: str = "", index: str = "") -> Self
```

- `original`: The text on the front of the card
- `translation`: The text on the back of the card
- `extra`: Additional information to display on the front (optional)
- `index`: An index or identifier for the card, displayed in the bottom right corner (optional)

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

## Text Wrapping and Sizing

The FlashCardGenerator automatically wraps text that's too long to fit on a single line. If the wrapped text is still too large for the card, it will progressively reduce the font size to make the content fit.

## Example

Here's a more detailed example showcasing various features:

```python
from flashcard_generator import FlashCardGenerator
from reportlab.lib.units import cm

generator = FlashCardGenerator()
generator.set_filename("language_flashcards.pdf") \
         .set_cards_per_row(3) \
         .set_card_height(4*cm) \
         .add_entry("Bonjour", "Hello", extra="Casual greeting", index="1") \
         .add_entry("Merci beaucoup", "Thank you very much", extra="**Important** phrase for expressing gratitude", index="2") \
         .add_entry("Au revoir", "Goodbye", extra="*Formal* farewell", index="3") \
         .add_entry("S'il vous plaît", "Please", extra="__Polite__ request", index="4") \
         .add_entry("Comment allez-vous?", "How are you?", extra="Formal way to ask about someone's wellbeing", index="5") \
         .add_entry("Je ne comprends pas", "I don't understand", extra="Useful phrase when you're confused", index="6") \
         .generate()
```

This will create a PDF with 3 cards per row, each card 4 cm high, and include 6 flashcards with various formatting styles, extra information, and indices.

## Contributing

Contributions to FlashCardGenerator are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.