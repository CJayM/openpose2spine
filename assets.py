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
            ])

            # dpg.add_font_range(0xf363, 0xf363)

    dpg.bind_font(DEFAULT_FONT)


