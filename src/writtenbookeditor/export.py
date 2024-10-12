import json
import zipfile
from enum import Enum
from pathlib import Path

import nbtlib

from .book import Page, BookMeta


class ExportItemType(Enum):
    WRITTEN_BOOK = 0
    SHULKER_BOX = 1


class ExportFileType(Enum):
    COMMAND_TEXT = 0
    FUNCTION_FILE = 1
    DATA_PACK = 2


class CommandVersion(Enum):
    UPPER_1_13 = 0
    UPPER_1_20_5 = 1


def export_book(
    pages: list[Page],
    path: str,
    title_format: str,
    author: str,
    item_type: ExportItemType,
    file_type: ExportFileType,
    command_version: CommandVersion,
    *,
    text_component: bool = True,
    filter: bool = False,
):
    quote = '"' if command_version == CommandVersion.UPPER_1_13 else None
    book_meta_list: list[BookMeta] = []
    for j, i in enumerate(range(0, len(pages), 100)):
        book_meta = BookMeta(
            author,
            title_format.format_map({"volume": j + 1}),
            pages[i : i + 100],
        )
        book_meta_list.append(book_meta)

    command_strings = []
    # generate commands
    if item_type == ExportItemType.WRITTEN_BOOK:
        if command_version == CommandVersion.UPPER_1_13:
            command_format = "give @p minecraft:written_book{book_meta}"
        elif command_version == CommandVersion.UPPER_1_20_5:
            command_format = "give @p minecraft:written_book[minecraft:written_book_content={book_meta}]"
        for book_meta in book_meta_list:
            command = command_format.format_map(
                {"book_meta": book_meta.to_nbt(text_component=text_component, filter=filter).snbt(quote=quote)},
            )
            command_strings.append(command)
    elif item_type == ExportItemType.SHULKER_BOX:
        if command_version == CommandVersion.UPPER_1_13:
            # 1.21以下
            for i in range(0, len(book_meta_list), 27):
                shulker_box_items = book_meta_list[i : i + 27]
                items = []
                for i, book_meta in enumerate(shulker_box_items):
                    item_nbt = nbtlib.Compound(
                        {
                            "Slot": nbtlib.Int(i),
                            "id": nbtlib.String("minecraft:written_book"),
                            "Count": nbtlib.Int(1),
                            "tag": book_meta.to_nbt(text_component=text_component, filter=filter),
                        }
                    )
                    items.append(item_nbt)
                items_nbt = nbtlib.List(items)
                command = f"give @p minecraft:white_shulker_box{{BlockEntityTag: {{Items: {items_nbt.snbt(quote=quote)} }} }}"
                command_strings.append(command)
        elif command_version == CommandVersion.UPPER_1_20_5:
            # 1.21以上
            for i in range(0, len(book_meta_list), 27):
                shulker_box_items = book_meta_list[i : i + 27]
                items = []
                for i, book_meta in enumerate(shulker_box_items):
                    book_meta_nbt = book_meta.to_nbt(text_component=text_component, filter=filter)
                    item_nbt = nbtlib.Compound(
                        {
                            "slot": nbtlib.Int(i),
                            "item": nbtlib.Compound(
                                {
                                    "id": nbtlib.String("minecraft:written_book"),
                                    "count": nbtlib.Int(1),
                                    "components": nbtlib.Compound(
                                        {
                                            "written_book_content": book_meta_nbt,
                                        }
                                    ),
                                }
                            ),
                        }
                    )
                    items.append(item_nbt)
                component_container_nbt = nbtlib.List(items)
                command = f"give @p minecraft:white_shulker_box[minecraft:container={component_container_nbt.snbt(quote=quote)}]"
                command_strings.append(command)
    # export files
    export_path = Path(path)
    if file_type == ExportFileType.COMMAND_TEXT:
        if not export_path.is_dir():
            raise ValueError("Export path must be a directory for command text export.")
        for i, command in enumerate(command_strings):
            if item_type == ExportItemType.WRITTEN_BOOK:
                file_path = export_path.joinpath(f"{title_format.format_map({'volume': i+1})}_volume-{i+1}.txt")
            else:
                file_name = (
                    f"{title_format.format_map({'volume': i*27+1})}-"
                    f"{title_format.format_map({'volume': min(i*27+27,len(book_meta_list))})}_"
                    f"volume-{i*27+1}-"
                    f"{min(i*27+27,len(book_meta_list))}.txt"
                )
                file_path = export_path.joinpath(file_name)
            file_path.touch()
            file_path.write_text("/" + command, encoding="utf-8")
    elif file_type == ExportFileType.FUNCTION_FILE:
        export_path.touch()
        export_path.write_text("\n".join(command_strings), encoding="utf-8")
    elif file_type == ExportFileType.DATA_PACK:
        zip_obj = zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED)
        pack_meta = {
            "pack": {
                "pack_format": 4 if command_version == CommandVersion.UPPER_1_13 else 41,
                "description": "§bWritten Book Editor §aData Pack\n§1Github §r:§dhttps://github.com/XiYang6666/WrittenBookGenerator",
            },
        }
        zip_obj.writestr(
            "pack.mcmeta",
            json.dumps(pack_meta),
        )
        mcfunction_content = "\n".join(command_strings)
        zip_obj.writestr("data/written_book_editor/functions/load.mcfunction", mcfunction_content)
        zip_obj.close()
