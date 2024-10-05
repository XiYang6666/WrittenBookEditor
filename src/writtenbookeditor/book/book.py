import nbtlib

from .page import Page


class BookMeta:
    def __init__(self, author: str, title: str, pages: list[Page]):
        self.author = author
        self.title = title
        self.pages = pages[:100]

    def to_nbt(
        self,
        *,
        text_component: bool = True,
        filter: bool = False,
    ) -> nbtlib.Compound:
        nbt = nbtlib.Compound()
        title_nbt = nbtlib.String(self.title)
        author_nbt = nbtlib.String(self.author)
        pages = []
        for page in self.pages:
            pages.append(page.to_nbt(text_component=text_component, filter=filter))
        pages_nbt = nbtlib.List(pages)
        nbt["title"] = nbtlib.Compound({"raw": title_nbt}) if filter else title_nbt
        nbt["author"] = nbtlib.Compound({"raw": author_nbt}) if filter else author_nbt
        nbt["pages"] = pages_nbt
        return nbt
