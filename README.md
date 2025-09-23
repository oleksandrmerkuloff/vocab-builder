# Learn English Dude

**Learn English Dude** is a desktop application designed to help users improve their English vocabulary by extracting unique words from text files, generating frequency statistics, and optionally creating flashcards in PDF format.

---

## Features

* Load `.txt` files with English text.
* Automatically extract unique words from the text.
* Count frequency of each word in the file.
* Optionally generate word cards in PDF format.
* Display results and provide a report window.
* User-friendly interface built with **CustomTkinter**.

---

## Installation

1. Clone this repository:

```bash
git clone https://github.com/yourusername/LearnEnglishDude.git
```

2. Navigate to the project folder:

```bash
cd LearnEnglishDude
```

3. Create a virtual environment (recommended):

```bash
python -m venv venv
```

4. Activate the virtual environment:

* **Windows:**

```bash
venv\Scripts\activate
```

* **Linux/MacOS:**

```bash
source venv/bin/activate
```

5. Install required dependencies:

```bash
pip install -r requirements.txt
```

---

## Usage

1. Run the application:

```bash
python main.py
```

2. Use the buttons to:

* Load a text file.
* Select the option to generate PDF cards.
* Save the output file.
* View a summary report with the total number of unique words.

---

## Dependencies

* [Python 3.13+](https://www.python.org/)
* [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
* [Googletrans](https://pypi.org/project/googletrans/)
* [WeasyPrint](https://weasyprint.org/) (optional, for PDF cards generation)

---

## Packaging as EXE

To create a standalone executable:

1. Make sure all dependencies are installed in your virtual environment.
2. Use **PyInstaller** to generate the executable:

```bash
pyinstaller --onefile --windowed --icon=application/icon.ico main.py
```

> Ensure all required DLLs for libraries like **WeasyPrint/GTK** are included if targeting Windows.

---

## License

This project is open-source under the MIT License.

---
