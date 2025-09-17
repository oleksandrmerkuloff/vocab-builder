from weasyprint import HTML


def generate_html(words: list) -> str:
    html = """
    <html>
    <head>
    <style>
    * {
        padding: 0;
        margin: 0;
    }
    body {
        display: flex;
        flex-wrap: wrap;
        justify-content: space-between;
        padding: 0 1vw;
    }
    .word-card {
        padding: 1%;
        border: 2px solid black;
        border-radius: 6px;
        text-align: center;
    }
    .original {
        font-size: 28px;
        font-weight: bold;
    }
    .translate {
        font-size: 24px;
        font-weight: bold;
    }
    </style>
    </head>
    <body>
    """

    for word in words:
        html += f"""
        <div class="word-card">
            <div class="original">{word[0].title()}</div>
            <br/>
            <div class="translate">{word[1].title()}</div>
        </div>
        """

    html += '</body></html>'
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
