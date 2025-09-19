import os


os.add_dll_directory(r"C:\Program Files\GTK3-Runtime Win64\bin")


from weasyprint import HTML


def generate_html(words: list) -> str:
    html = """
    <html>
    <head>
    <style>
    * {
        padding: 0;
        margin: 0;
        box-sizing: border-box;
    }
    body {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 15px;
        padding: 20px;
    }
    .word-card {
        width: 240px;   /* smaller width */
        height: 120px;  /* smaller height */
        border: 2px solid black;
        border-radius: 6px;
        text-align: center;
        padding: 10px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        page-break-inside: avoid; /* prevent cutting */
    }
    .original {
        font-size: 20px;
        font-weight: bold;
    }
    .translate {
        font-size: 18px;
        font-weight: bold;
    }
    hr {
        border: 1px dashed black; /* dashed fold line */
        margin: 5px 0;
    }
    </style>
    </head>
    <body>
    """

    for word in words:
        html += f"""
        <div class="word-card">
            <div class="original">{word[0].title()}</div>
            <hr/>
            <div class="translate">{word[1].title()}</div>
        </div>
        """

    html += "</body></html>"
    return html


def create_pdf(words: list, file_path: str) -> None:
    html_content = generate_html(words)
    HTML(string=html_content).write_pdf(file_path)


if __name__ == '__main__':
    test_words = [
        ['hello', 'привіт'],
        ['world', 'світ'],
        ['from', 'від'],
        ['Crystal1s', 'Crystal1s']
    ]
    file_path = 'test.pdf'

    create_pdf(test_words, file_path)
