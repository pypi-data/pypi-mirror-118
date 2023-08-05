#!/usr/bin/env python3

import os
import math
import sys
import pathlib
import os.path as path
import json
import time
import datetime
import pyautogui # type: ignore
from PIL import ImageDraw, Image, ImageFont #type: ignore
import subprocess

from screens.utils import *
from screens.img import *

from typing import *

screenshot_prefix = "page__"

def wait(seconds: int) -> None:
    for i in range(seconds):
        print(f"...screenshot in {seconds-i}s...")
        time.sleep(1)

def prepare_screenshots(cnf: Configuration) -> None:
    # Take screenshot

    print()
    print("Steps:")
    print("1. The upper-left corner of the area to screenshot")
    print("2. The lower-right corner of the area to screenshot")
    print("3. The location where to click for the next page")
    print("4. Click on the screenshot to close the window")
    wait(2)

    tmp_filename = cnf.path("__tmp.png")
    img = pyautogui.screenshot()

    coef = 3 if cnf.retina else 2
    img = img.resize((int(img.width / coef), int(img.height / coef)))
    print(f"Saving screenshot {tmp_filename}")

    if cnf.x1 and cnf.y1:
        draw = ImageDraw.Draw(img)
        draw.line((0, cnf.y1 / coef, img.width, cnf.y1 / coef), fill="orange")
        draw.line((cnf.x1 / coef, 0, cnf.x1 / coef, img.height), fill="orange")
    if cnf.x2 and cnf.y2:
        draw = ImageDraw.Draw(img)
        draw.line((0, cnf.y2 / coef, img.width, cnf.y2 / coef), fill="orange")
        draw.line((cnf.x2 / coef, 0, cnf.x2 / coef, img.height), fill="orange")
    if cnf.mouse_x and cnf.mouse_y:
        draw = ImageDraw.Draw(img)
        draw.line((cnf.mouse_x / coef-5, cnf.mouse_y / coef, cnf.mouse_x / coef+5, cnf.mouse_y / coef), fill="orange")
        draw.line((cnf.mouse_x / coef, cnf.mouse_y / coef - 5, cnf.mouse_x / coef, cnf.mouse_y / coef + 5), fill="orange")

    img.save(tmp_filename)

    # Open window and wait for upper left click
    print("Click on upper-right part of the screenshot area")
    x1, y1 = show_image(tmp_filename, img.width, img.height)

    # Draw boundaires
    draw = ImageDraw.Draw(img)
    draw.line((0, y1, img.width, y1), fill="red")
    draw.line((x1, 0, x1, img.height), fill="red")
    img.save(tmp_filename)

    # Open window and wait for lower-right clitk
    x2, y2 = show_image(tmp_filename, img.width, img.height)

    # Draw boundaires
    draw = ImageDraw.Draw(img)
    draw.line((0, y2, img.width, y2), fill="red")
    draw.line((x2, 0, x2, img.height), fill="red")
    img.save(tmp_filename)

    x3, y3 = show_image(tmp_filename, img.width, img.height)
    cnf.mouse_x = x3 * coef
    cnf.mouse_y = y3 * coef
    draw = ImageDraw.Draw(img)
    draw.line((x3-5, y3, x3+5, y3), fill="orange")
    draw.line((x3, y3-5, x3, y3+5), fill="orange")
    img.save(tmp_filename)

    # Open window and wait "next" button position
    next_page_key = input("Next page keyboard key (eg. pgdn, left, ...): ")
    if next_page_key:
        cnf.next_page_key = next_page_key

    show_image(tmp_filename, img.width, img.height)
    cnf.x1 = x1 * coef
    cnf.y1 = y1 * coef
    cnf.x2 = x2 * coef
    cnf.y2 = y2 * coef

def make_screenshot(file_name: str, cnf: Configuration, scale: float=1) -> Any:
    region = (cnf.x1, cnf.y1, cnf.x2 - cnf.x1, cnf.y2 - cnf.y1)
    #print(f"Screenshot to {file_name} with region {region}")
    img = pyautogui.screenshot(region=region)
    if scale != 1:
        img = img.resize((int(img.width*scale), int(img.height*scale)))
    img.save(file_name)

def test_screenshot(cnf: Configuration) -> None:
    wait(2)
    print()
    print("Click on the screenshot to close")
    tmp_file = cnf.path("example_screenshot.png")
    print(tmp_file)
    make_screenshot(tmp_file, cnf, scale=0.5)
    show_image(tmp_file, cnf.x2 - cnf.x1, cnf.y2 - cnf.y1)

def quit_app(cnf: Configuration) -> None:
    sys.exit(0)

def resize_ratio(cnf: Configuration) -> None:
    try:
        cnf.resize_ratio = float(input("Scale (default 1):"))
    except:
        cnf.resize_ratio = 1
    if cnf.resize_ratio <= 0:
        cnf.resize_ratio = 0.5

def toggle_bw(cnf: Configuration) -> None:
    cnf.convert_to_bw = not cnf.convert_to_bw

def toggle_retina(cnf: Configuration) -> None:
    cnf.retina = not cnf.retina

def prepare_image(file_in: str, bw: bool=False, page: str="", resize: float=1) -> Any:
    im: Any = Image.open(file_in)
    #ipdb.set_trace()
    width, height = im.size

    mode = 'L' if bw else 'RGB'

    label_height = 30 if page else 0
    out = Image.new(mode, (width, height+label_height))
    out.paste(im, (0, 0))

    if page:
        label = Image.new('L', (width, label_height), 255)
        draw = ImageDraw.Draw(label)
        font = ImageFont.truetype("/System/Library/Fonts/Keyboard.ttf", label_height)
        draw.text((width * 0.45, 0), page, fill=(0), font=font)
        out.paste(label, (0, height))

    width, height = out.size
    if resize != 1:
        out = out.resize((int(width*resize), int(height*resize)))
    return out


def get_screenshots(cnf: Configuration) -> List[str]:
    original_files: List[str] = []
    file = ""
    for file in os.listdir(cnf.work_dir):
        if file.startswith(screenshot_prefix):
            original_files.append(file)
    original_files.sort()
    return original_files

def export_to_pdf(cnf: Configuration) -> None:
    original_files = get_screenshots(cnf)

    pages = 0
    try: pages = int(input("Last page no (or leave empty for no pagination): "))
    except: pass

    processed_images: List[Any] = []
    for n, file in enumerate(original_files):
        label = ""
        if pages:
            page = 1 + math.floor(0 + (n / len(original_files)) * pages)
            label = f"{page}"
        print(f"{n}/{len(original_files)}: {file}")
        try:
            processed_images.append(prepare_image(cnf.path(file), bw=cnf.convert_to_bw, page=label, resize=cnf.resize_ratio))
        except:
            if "n" == input(f"Error opening image {file}, continue [Yn]"):
                return

    filename = ""
    for c in cnf.work_dir:
        filename += c if c.isalnum() or c.isalpha() else "_"

    outfile = cnf.path(filename + ".pdf" if filename else "exported.pdf")
    print(f"Converting to {outfile}")
    im1 = processed_images[0]
    im1.save(outfile, save_all=True, append_images=processed_images[1:])
    print(f"Saved to {filename}")

def take_screenshots(cnf: Configuration) -> None:
    try:
        n = int(input("How many screenshots/pages: "))
    except:
        n = 0
    take_n_screenshots(cnf, n)

def screenshot_the_rest(cnf: Configuration) -> None:
    screenshots = get_screenshots(cnf)

    if len(screenshots) <= 5:
        print("Too few screenshots")
        take_screenshots(cnf)
        return

    try: current_document_page = int(input("Current document page: "))
    except: current_document_page = 0

    if current_document_page == 0:
        take_screenshots(cnf)
        return

    try: last_document_page = int(input(f"Total document pages: [{cnf.total_pages}] "))
    except: last_document_page = cnf.total_pages
    cnf.total_pages = last_document_page

    one_document_page_screenshots = len(screenshots) / current_document_page
    total_screenshots = cnf.total_pages * one_document_page_screenshots
    rest = int(total_screenshots - len(screenshots))

    print(f"One document page is ~{one_document_page_screenshots} screenshots")
    print(f"In total it will be ~{total_screenshots} screenshots")
    print(f"=> need ~{rest} screenshots")

    try:
        n = int(input(f"How many screenshots/pages (<enter> for {rest}): "))
    except:
        n = rest

    take_n_screenshots(cnf, n)

def take_n_screenshots(cnf: Configuration, count: int) -> None:
    if count == 0:
        return

    wait(2)

    started = datetime.datetime.now()
    for i in range(count):
        now = datetime.datetime.now()
        fn = cnf.path(screenshot_prefix + now.isoformat().replace(":", "_") + ".png")
        make_screenshot(fn, cnf)
        remaining_time_str = ""
        if i > 5:
            time_per_screenshot = (datetime.datetime.now() - started) / i
            remaining_time_str = f" [Remaining time ~{(count - i) * time_per_screenshot}]"
        print(f"{i}/{count} -> {fn} {remaining_time_str}")
        #print(cnf.mouse_x, cnf.mouse_y)
        coef = 2 if cnf.retina else 1
        pyautogui.moveTo(cnf.mouse_x / coef, cnf.mouse_y / coef)
        pyautogui.mouseDown()
        time.sleep(0.05)
        pyautogui.mouseUp()
        if cnf.next_page_key:
            pyautogui.press(cnf.next_page_key)
        time.sleep(cnf.sleep)

def change_work_dir(cnf: Configuration) -> None:
    dir = input("Enter work directory name:")
    cnf.work_dir = dir
    try:
        os.makedirs(cnf.work_dir)
    except:
        print("Can't create directory", dir)
        cnf.work_dir = "."

def wait_time(cnf: Configuration) -> None:
    try:
        cnf.sleep = float(input("Enter time:"))
    except:
        print("Invalid time")
        cnf.sleep = 0.1

def open_dir(cnf: Configuration) -> None:
    dir_opener = input(f"Open with command [{cnf.dir_opener}]:")
    if dir_opener:
        cnf.dir_opener = dir_opener
    
    subprocess.check_output([cnf.dir_opener, cnf.work_dir])

def main_menu() -> None:
    cnf = Configuration()
    cnf.load()

    if len(sys.argv) > 1:
        cnf.work_dir = sys.argv[1]

    options: List[Tuple[str, Callable[[Configuration], str], Callable[[Configuration], None]]] = []
    options.append(("d", lambda cnf: f"Working directory for screenshots ({cnf.work_dir})", change_work_dir))
    options.append(("p", lambda cnf: "Prepare screenshots geometry", prepare_screenshots))
    options.append(("t", lambda cnf: "Test screenshot", test_screenshot))
    options.append(("s", lambda cnf: f"Take screenshots (sides ratio: {cnf.x2 - cnf.x1}:{cnf.y2 - cnf.y1}={cnf.ratio()})", take_screenshots))
    options.append(("sr", lambda cnf: f"Screenshot the rest of the document", screenshot_the_rest))
    options.append(("w", lambda cnf: f"Wait between screenshowts ({cnf.sleep}s)", wait_time))
    options.append(("r", lambda cnf: f"Resize ({cnf.resize_ratio})", resize_ratio))
    options.append(("b", lambda cnf: f"Convert to black-and-white ({cnf.convert_to_bw})", toggle_bw))
    options.append(("re", lambda cnf: f"Retina screen ({cnf.retina})", toggle_retina))
    options.append(("o", lambda cnf: f"Open directory with ({cnf.dir_opener})", open_dir))
    options.append(("e", lambda cnf: "Export to pdf", export_to_pdf))
    menu("Select", options, cnf, "q", "Quit")

main_menu()
