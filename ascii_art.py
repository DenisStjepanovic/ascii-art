#!/usr/bin/env python3
import pyfiglet
import colorama
from colorama import Fore, Style
import time
import sys
import os

colorama.init()

FONTS = [
    "big", "banner3-D", "slant", "doom", "block",
    "bulbhead", "digital", "isometric1", "larry3d", "roman",
    "shadow", "speed", "starwars", "stop", "3d_diagonal",
]

COLORS = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA]
COLOR_NAMES = ["red", "yellow", "green", "cyan", "blue", "magenta"]

RAINBOW = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA]


def clear():
    os.system("clear")


def rainbow_print(text, delay=0.03):
    lines = text.split("\n")
    for i, line in enumerate(lines):
        color = RAINBOW[i % len(RAINBOW)]
        print(color + line + Style.RESET_ALL)
        time.sleep(delay)


def solid_print(text, color):
    print(color + text + Style.RESET_ALL)


def animate_print(text, color, delay=0.005):
    lines = text.split("\n")
    for line in lines:
        for char in line:
            sys.stdout.write(color + char + Style.RESET_ALL)
            sys.stdout.flush()
            time.sleep(delay)
        print()


def render(word, font, color_mode, color_index, animate):
    try:
        art = pyfiglet.figlet_format(word, font=font)
    except pyfiglet.FontNotFound:
        art = pyfiglet.figlet_format(word, font="big")

    if color_mode == "rainbow":
        if animate:
            animate_print(art, Fore.WHITE, delay=0.002)
            time.sleep(0.1)
            print()
            rainbow_print(art, delay=0.02)
        else:
            rainbow_print(art, delay=0)
    else:
        color = COLORS[color_index % len(COLORS)]
        if animate:
            animate_print(art, color)
        else:
            solid_print(art, color)


def print_help():
    print(Fore.CYAN + "\nCommands:" + Style.RESET_ALL)
    cmds = [
        ("  <text>       ", "render text with current settings"),
        ("  font         ", "cycle to next font"),
        ("  font <name>  ", "set a specific font"),
        ("  fonts        ", "list available fonts"),
        ("  color        ", "cycle to next color"),
        ("  rainbow      ", "toggle rainbow mode"),
        ("  animate      ", "toggle typing animation"),
        ("  demo         ", "show all fonts for current word"),
        ("  quit / q     ", "exit"),
    ]
    for cmd, desc in cmds:
        print(Fore.YELLOW + cmd + Style.RESET_ALL + desc)
    print()


def demo_all_fonts(word, color_index):
    color = COLORS[color_index % len(COLORS)]
    for font in FONTS:
        try:
            art = pyfiglet.figlet_format(word, font=font)
            print(Fore.CYAN + f"── {font} ──" + Style.RESET_ALL)
            solid_print(art, color)
            time.sleep(0.3)
        except Exception:
            pass


def main():
    clear()
    print(Fore.MAGENTA + Style.BRIGHT)
    print(pyfiglet.figlet_format("ASCII ART", font="banner3-D"))
    print(Style.RESET_ALL)
    print("Type any word to render it. Type 'help' for commands.\n")

    font_index = 0
    color_index = 2  # green
    color_mode = "solid"
    animate = False
    last_word = "hello"

    while True:
        font = FONTS[font_index % len(FONTS)]
        color_name = "rainbow" if color_mode == "rainbow" else COLOR_NAMES[color_index % len(COLOR_NAMES)]
        anim_flag = " animate" if animate else ""
        prompt = (
            Fore.CYAN + f"[font: {font}  color: {color_name}{anim_flag}] "
            + Fore.WHITE + "> " + Style.RESET_ALL
        )

        try:
            raw = input(prompt).strip()
        except (EOFError, KeyboardInterrupt):
            print("\n" + Fore.YELLOW + "Bye!" + Style.RESET_ALL)
            break

        if not raw:
            continue

        cmd = raw.lower()

        if cmd in ("quit", "q", "exit"):
            print(Fore.YELLOW + "Bye!" + Style.RESET_ALL)
            break
        elif cmd == "help":
            print_help()
        elif cmd == "fonts":
            print(Fore.CYAN + "Available fonts:" + Style.RESET_ALL)
            print("  " + ", ".join(FONTS) + "\n")
        elif cmd == "font":
            font_index += 1
            new_font = FONTS[font_index % len(FONTS)]
            print(Fore.CYAN + f"Font → {new_font}\n" + Style.RESET_ALL)
            render(last_word, new_font, color_mode, color_index, animate)
        elif cmd.startswith("font "):
            requested = raw[5:].strip()
            if requested in FONTS:
                font_index = FONTS.index(requested)
                print(Fore.CYAN + f"Font → {requested}\n" + Style.RESET_ALL)
                render(last_word, requested, color_mode, color_index, animate)
            else:
                print(Fore.RED + f"Unknown font '{requested}'. Type 'fonts' to list options.\n" + Style.RESET_ALL)
        elif cmd == "color":
            color_mode = "solid"
            color_index += 1
            name = COLOR_NAMES[color_index % len(COLOR_NAMES)]
            print(Fore.CYAN + f"Color → {name}\n" + Style.RESET_ALL)
            render(last_word, FONTS[font_index % len(FONTS)], color_mode, color_index, animate)
        elif cmd == "rainbow":
            color_mode = "rainbow" if color_mode != "rainbow" else "solid"
            state = "on" if color_mode == "rainbow" else "off"
            print(Fore.CYAN + f"Rainbow → {state}\n" + Style.RESET_ALL)
            render(last_word, FONTS[font_index % len(FONTS)], color_mode, color_index, animate)
        elif cmd == "animate":
            animate = not animate
            state = "on" if animate else "off"
            print(Fore.CYAN + f"Animation → {state}\n" + Style.RESET_ALL)
        elif cmd == "demo":
            demo_all_fonts(last_word, color_index)
        else:
            last_word = raw
            render(raw, FONTS[font_index % len(FONTS)], color_mode, color_index, animate)


if __name__ == "__main__":
    main()
