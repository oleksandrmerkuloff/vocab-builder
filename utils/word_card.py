from weasyprint import HTML

import chardet
import threading

from application.windows.report import ReportWindow


def generate_html(words: list) -> str:
    """Generate HTML file"""
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


def read_file_safely(path):
    """Check type of file encoding"""
    with open(path, "rb") as f:
        raw = f.read()
    enc = chardet.detect(raw)["encoding"] or "utf-8"
    return raw.decode(enc, errors="ignore")


def create_pdf(master, words_path, pdf_path):
    """Gets data create html and generate pdf"""
    def worker():
        content = read_file_safely(words_path)
        lines = [x.strip() for x in content.splitlines() if x.strip()]

        words = []
        total = len(lines)
        for i, line in enumerate(lines, 1):
            try:
                _, rest = line.split(";", 1)
                original, translate = rest.split("-", 1)
                words.append([original.strip(), translate.strip()])
            except ValueError:
                continue
            master.after(0, lambda p=i/total: master.progress_bar.set(p))
            master.after(0, lambda: master.progress_label.configure(text=f'{i}/{total}'))

        html = generate_html(words)

        HTML(string=html).write_pdf(pdf_path)

        master.after(0, lambda: ReportWindow(master=master, c_text="PDF Generated"))
        master.after(0, lambda: master.progress_bar.set(1))

    threading.Thread(target=worker, daemon=True).start()
