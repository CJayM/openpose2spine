from dearpygui import dearpygui as dpg

DEFAULT_FONT = None
ICONS_FONT = None


class IconCode:
    bolt = 0xf0e7
    check = 0xf00c
    magnifying_glass = 0xf002
    download = 0xf019
    arrow_right = 0xf061
    xmark = 0xf00d
    file = 0xf15b
    clipboard = 0xf328
    pen = 0xf304
    film = 0xf008
    video = 0xf03d
    plus = 0x2b
    minus = 0xf068
    play = 0xf04b
    stop = 0xf04d
    pause = 0xf04c
    forward_step = 0xf051
    backward_step = 0xf048
    arrows_repeat = 0xf363
    slider = 0xf1de
    forward_fast = 0xf050
    backward_fast = 0xf049


def init_fonts():
    global DEFAULT_FONT
    global ICONS_FONT
    with dpg.font_registry():
        with dpg.font("assets/fonts/DroidSans.ttf", 16, default_font=True) as DEFAULT_FONT:
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)

        with dpg.font("assets/fonts/Font Awesome 6 Free-Solid-900.otf", 16) as ICONS_FONT:
            dpg.add_font_chars([
                IconCode.bolt,  # bolt 
                IconCode.check,  # check 
                IconCode.magnifying_glass,  # magnifying-glass 
                IconCode.download,  # download 
                IconCode.arrow_right,  # arrow-right 
                IconCode.xmark,  # xmark 
                IconCode.file,  # file 
                IconCode.clipboard,  # clipboard 
                IconCode.pen,  # pen 
                IconCode.film,  # film 
                IconCode.video,  # video 
                IconCode.plus,  # plus +
                IconCode.minus,  # minus 
                IconCode.play,  # play 
                IconCode.stop,  # stop 
                IconCode.pause,  # pause 
                IconCode.forward_step,  # forward-step 
                IconCode.backward_step,  # backward-step 
                IconCode.arrows_repeat,  # arrows-repeat 
                IconCode.slider,  # slider 
                IconCode.forward_fast, # 
                IconCode.backward_fast, # 

            ])

            # dpg.add_font_range(0xf363, 0xf363)

    dpg.bind_font(DEFAULT_FONT)


class Themes:
    primary_button = None
    primary_button_toggled = None

    secondary_button = None
    secondary_button_toggled = None

    def __init__(self):
        if not Themes.primary_button:
            with dpg.theme() as Themes.primary_button:
                with dpg.theme_component(dpg.mvAll):
                    dpg.add_theme_color(dpg.mvThemeCol_Button, (42, 91, 128), category=dpg.mvThemeCat_Core)
                    dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (170, 228, 255), category=dpg.mvThemeCat_Core)
                    dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (27, 125, 252), category=dpg.mvThemeCat_Core)

            with dpg.theme() as Themes.primary_button_toggled:
                with dpg.theme_component(dpg.mvAll):
                    dpg.add_theme_color(dpg.mvThemeCol_Button, (61, 198, 255), category=dpg.mvThemeCat_Core)
                    dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (170, 228, 255), category=dpg.mvThemeCat_Core)
                    dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (27, 125, 252), category=dpg.mvThemeCat_Core)

            with dpg.theme() as Themes.secondary_button:
                with dpg.theme_component(dpg.mvAll):
                    dpg.add_theme_color(dpg.mvThemeCol_Button, (51, 51, 55), category=dpg.mvThemeCat_Core)
                    dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (29, 151, 236, 103), category=dpg.mvThemeCat_Core)
                    dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (0, 119, 200, 153), category=dpg.mvThemeCat_Core)

            with dpg.theme() as Themes.secondary_button_toggled:
                with dpg.theme_component(dpg.mvAll):
                    dpg.add_theme_color(dpg.mvThemeCol_Button, (81, 81, 85), category=dpg.mvThemeCat_Core)
                    dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (59, 161, 255, 113), category=dpg.mvThemeCat_Core)
                    dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (30, 149, 230, 163), category=dpg.mvThemeCat_Core)


__theme_instance = None


def get_themes():
    global __theme_instance
    if not __theme_instance:
        __theme_instance = Themes()
    return __theme_instance
