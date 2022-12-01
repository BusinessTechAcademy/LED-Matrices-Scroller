# ANIMATED SCROLLER REMAKE (11.18.22)

import time
import random
import board
import terminalio  # Imported libs

from adafruit_matrixportal.matrixportal import MatrixPortal  # Additional import

matrixportal = MatrixPortal(
    width=64, height=32, status_neopixel=board.NEOPIXEL, debug=True
)  # Display setup
matrixportal.add_text(
    text_font=terminalio.FONT,
    text_position=(0, (matrixportal.graphics.display.height // 2) - 1),
    scrolling=True,
)  # Creating scrolling text for later!
matrixportal.add_text(
    text_font=terminalio.FONT,
    text_position=(2, (matrixportal.graphics.display.height // 2) - 1),
)  # Creating static text for later !

ANIM_FEED = "sign-quotes.signanim"
QUOTES_FEED = "sign-quotes.signtext"
COLORS_FEED = "sign-quotes.signcolor"  # Adafruit IO feed Json

animations_enabled = 0
random_enabled = 0
status_offline = 0
cycle_step = 0
last_update = time.monotonic()  # Clock for later !

SCAN_DELAY = 0.01
UPDATE_DELAY = 1000  # Delay Values

quotes = []
colors = []
anims = []  # Feed arrays

last_anim = None
last_color = None
last_quote = None  # History Values


#def monotonic():
#    if time.monotonic() > last_update + UPDATE_DELAY:
#        cycle_step = cycle_step + 1
#        update_data()  # Updating the data on a repeat timer.
#        last_update = time.monotonic()
#    print(cycle_step)

def update_data():
    matrixportal.set_text("Connecting...", 1)  # Signing the start of the function.
    print("Updating Data...")

    if status_offline == 1:
        matrixportal.set_text("Offline", 1)  # If offline code doesnt stop running.
        print("Offline")
    try:
        quotes_data = matrixportal.get_io_data(
            QUOTES_FEED
        )  # Gathering data from feeds and setting variables to them.
        color_data = matrixportal.get_io_data(COLORS_FEED)
        anim_data = matrixportal.get_io_data(ANIM_FEED)

        quotes.clear()
        colors.clear()
        anims.clear()  # Clearing any value set before
        for json_data in quotes_data:
            quotes.append(matrixportal.network.json_traverse(json_data, ["value"]))
        for json_data in color_data:
            colors.append(matrixportal.network.json_traverse(json_data, ["value"]))
        for json_data in anim_data:
            anims.append(
                matrixportal.network.json_traverse(json_data, ["value"])
            )  # Making the pull
        print(colors)
        print(quotes)
        print(anims)  # Printing the pull into console
    except Exception as error:
        print(Exception)
    if not quotes or not colors:
        raise RuntimeError("Run-time Error:")
        print("No quotes or colors!")

update_data()
last_update = time.monotonic()

quote_index = None
color_index = None
anim_index = None

while True:
    matrixportal.set_text("", 1)
    if random_enabled == 1:
        print("Random !")
        if len(quotes) > 1 and last_quote is not None:
            while quote_index == last_quote:
                quote_index = random.randrange(0, len(quotes))
        else:
            quote_index = random.randrange(0, len(quotes))
        last_quote = quote_index
        if len(colors) > 1 and last_color is not None:
            while color_index == last_color:
                color_index = random.randrange(0, len(colors))
        else:
            color_index = random.randrange(0, len(colors))
        last_color = color_index
        if len(anims) > 1 and last_anim is not None:
            while anim_index == last_anim:
                anim_index = random.randrange(0, len(anims))
        else:
            color_index = random.randrange(0, len(anims))
        last_anim = anim_index
    else:
        print("Static !")
        while quote_index == last_quote:
            quote_index = (len(quotes) - 1)
        while color_index == last_color:
            color_index = (len(colors) - 1)
        while anim_index == last_anim:
            anim_index = (len(anims) - 1)

    if animations_enabled == 1:
        print("Animation Starting ! ")
        if anims == 1:
            matrixportal.set_text(quotes[quote_index])
    else:
        matrixportal.set_text(quotes[quote_index])
        print("Animations Disabled !")

    matrixportal.set_text_color(colors[color_index])
    print(SCAN_DELAY)
    matrixportal.scroll_text(SCAN_DELAY)
    #monotonic()
    if time.monotonic() > last_update + UPDATE_DELAY:
        cycle_step = cycle_step + 1
        update_data()
        last_update = time.monotonic()
    print(cycle_step)
