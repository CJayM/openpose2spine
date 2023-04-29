from dearpygui import dearpygui as dpg

DEFAULT_FONT = None
ICONS_FONT = None


def init_fonts():
    global DEFAULT_FONT
    global ICONS_FONT
    with dpg.font_registry():
        with dpg.font("assets/fonts/DroidSans.ttf", 16, default_font=True) as DEFAULT_FONT:
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)

        with dpg.font("assets/fonts/Font Awesome 6 Free-Solid-900.otf", 16) as ICONS_FONT:
            dpg.add_font_chars([
                0xf0e7,     # bolt 
                0xf00c,     # check 
                0xf002,     # magnifying-glass 
                0xf019,     # download 
                0xf061,     # arrow-right 
                0xf00d,     # xmark 
                0xf15b,     # file 
                0xf328,     # clipboard 
                0xf304,     # pen 
                0xf008,     # film 
                0xf03d,     # video 
                0x2b,       # plus +
                0xf068,     # minus 
                0xf04b,     # play 
                0xf04d,     # stop 
                0xf04c,     # pause 
                0xf051,     # forward-step 
                0xf048,     # backward-step 
                0xf364,     # arrows-repeat 
                0xf1de,     # slider 
            ])

    dpg.bind_font(DEFAULT_FONT)
