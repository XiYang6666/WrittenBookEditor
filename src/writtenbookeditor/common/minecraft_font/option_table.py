from ...core.options import option
from ...core.registry import register_option_table


@register_option_table("minecraft_font")
class MinecraftFontOptionTable:
    version: str = option("choice", ["1.21"])
    force_unifont: bool = option("bool", False)
    jp_glyph_variants: bool = option("bool", False)
