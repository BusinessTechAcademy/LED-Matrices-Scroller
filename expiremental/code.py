# ANIMATED SCROLLER REMAKE (11.18.22)

import time
import random
import board
import terminalio  # Imported libs

from adafruit_matrixportal.matrixportal import MatrixPortal  # Additional import

matrixportal = MatrixPortal(
    bit_depth=3, width=128, height=32, status_neopixel=board.NEOPIXEL, debug=True
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
COLORS_FEED = "sign-quotes.signcolor"
DELAY_FEED = "sign-quotes.signdelay"
RANDOM_FEED = "sign-quotes.signrandom"  # Adafruit IO feed Json

animations_enabled = True  # For testing purposes !
status_offline = 0  # For testing purposes !

last_update = time.monotonic()  # Clock for later !

SCROLL_DELAY = 0.02
UPDATE_DELAY = 50  # Delay Values

random_enabled = []
delay_values = []
quotes = []
colors = []
anims = []  # Feed arrays

last_anim = None
last_color = None
last_quote = None  # History Values


# def monotonic():
#    if time.monotonic() > last_update + UPDATE_DELAY:
#        cycle_step = cycle_step + 1
#        update_data()  # Updating the data on a repeat timer.
#        last_update = time.monotonic()
#    print(cycle_step)


def update_data():
    matrixportal.set_text("Connecting...", 1)  # Signing the start of the function.
    # print("Updating Data...")

    if status_offline == 1:
        matrixportal.set_text("Offline", 1)  # If offline code doesnt stop running.
        print("Offline")
    try:
        quotes_data = matrixportal.get_io_data(
            QUOTES_FEED
        )  # Gathering data from feeds and setting variables to them.
        color_data = matrixportal.get_io_data(COLORS_FEED)
        anim_data = matrixportal.get_io_data(ANIM_FEED)
        random_data = matrixportal.get_io_data(RANDOM_FEED)
        delay_data = matrixportal.get_io_data(RANDOM_FEED)
        random_enabled.clear()
        delay_values.clear()
        quotes.clear()
        colors.clear()
        anims.clear()  # Clearing any value set before
        for json_data in random_data:
            random_enabled.append(
                matrixportal.network.json_traverse(json_data, ["value"])
            )
        for json_data in delay_data:
            delay_values.append(
                matrixportal.network.json_traverse(json_data, ["value"])
            )
        for json_data in quotes_data:
            quotes.append(matrixportal.network.json_traverse(json_data, ["value"]))
        for json_data in color_data:
            colors.append(matrixportal.network.json_traverse(json_data, ["value"]))
        for json_data in anim_data:
            anims.append(
                matrixportal.network.json_traverse(json_data, ["value"])
            )  # Making the pull
        print(random_enabled)
        print(delay_values)
        print(colors)
        print(quotes)
        print(anims)  # Printing the pull into console
    except Exception as error:
        print(Exception)
    if not quotes or not colors:
        raise RuntimeError("Loop Error")
        print("No quotes or colors!")


update_data()
last_update = time.monotonic()

quote_index = None
color_index = None
anim_index = None
rand_i = None
delay_i = None

while True:
    matrixportal.set_text("", 1)
    # print(random_enabled[0])

    # if anims[0] <= 1:
    #    print("Success!!")
    set_random = int(random_enabled[0])
    print("random:")
    print(set_random)

    if set_random == 1:
        # print("Random !")
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
    else:
        # print("Static !")
        while quote_index == last_quote:
            quote_index = 0
        while color_index == last_color:
            color_index = 0
        while anim_index == last_anim:
            anim_index = 0

    if animations_enabled == True:
        set_animation = int(anims[0])
        # print("Animation Starting ! ")
        # print(type(anims[0]))
        # print(anims[0])
        if set_animation == 1:
            matrixportal.set_text(quotes[quote_index])
        #     print("Testing Success")
        if set_animation == 2 and set_animation != 1:
            print("issue")
            matrixportal.set_text(quotes[quote_index], 1)
            matrixportal.set_text("")
        if set_animation < 0.98:
            matrixportal.set_text(quotes[quote_index])
            print("Animation does not exist")

    matrixportal.set_text_color(colors[color_index])
    # print(SCROLL_DELAY)
    if set_animation == 2:
        print("Place-holder")
    else:
        matrixportal.scroll_text(SCROLL_DELAY)

    set_delay = int(delay_values[0])
    print("Delay:")
    UPDATE_DELAY = set_delay + 15
    print(UPDATE_DELAY)
    # print(delay_values[0])
    # print(time.monotonic())
    if time.monotonic() > last_update + UPDATE_DELAY:
        update_data()
        last_update = time.monotonic()
        # print("Updating Data !")
    # if last_scan == time.monotonic()
