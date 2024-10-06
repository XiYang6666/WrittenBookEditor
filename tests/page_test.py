from io import StringIO

from writtenbookeditor.book.page import Page


def test_page():
    with open("data/test/test_txt_1.txt", "r", encoding="utf-8") as f:
        txt = f.read()
        stream = StringIO(txt)

    pages = []

    while True:
        pages.append(Page.from_plaintext_stream(stream, unicode=False))
        if stream.read(1) == "":
            break
        else:
            stream.seek(stream.tell() - 1)

    for page in pages:
        print(page)
