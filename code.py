# ANIMATED SCROLLER REMAKE (11.18.22)
# DEMO CODE FINISHED (12.8.22)
# CODE DOCUMENTED (12.12.22)

import time         # Imported for: Timers & Time Functions.
import random       # Imported for: Features.
import board        # Imported for: Setting board parameters (height, width, bit depth, & etc.)
import terminalio   # Imported for: Fonts & Text Features/

from adafruit_matrixportal.matrixportal import MatrixPortal  # Used to rename: "adafruit_matrixportal" to "MatrixPortal"

matrixportal = MatrixPortal(
    bit_depth=3, width=128, height=32, status_neopixel=board.NEOPIXEL, debug=True # Setting our parameters.
)
matrixportal.add_text( # Creating a text box.
    text_font=terminalio.FONT, # Using terminalio library for font.
    text_position=(0, (matrixportal.graphics.display.height // 2) - 1), # Setting text position (offset & height)
    scrolling=True, # Making text scroll when quote is implemented.
)
matrixportal.add_text( # Creating a second text box.
    text_font=terminalio.FONT,
    text_position=(2, (matrixportal.graphics.display.height // 2) - 1),
    scrolling=False, # This text will not scroll and will remain static.
)

ANIM_FEED = "sign-quotes.signanim"
QUOTES_FEED = "sign-quotes.signtext"
COLORS_FEED = "sign-quotes.signcolor"
DELAY_FEED = "sign-quotes.signdelay"  # These are variables that hold strings to the feed.
RANDOM_FEED = "sign-quotes.signrandom" # String format example: "feed-group.feed-name"

animations_enabled = True  # Whether this is variable is true or false it will enable the lines of code in charge of animations [DEBUG VARIABLE]
status_offline = False  # Will stop trying to connect to a hotspot if true [DEBUG VARIABLE]

last_update = time.monotonic()  # Getting time at start (this function works with our update delay to update the data and wll be used more later)

SCROLL_DELAY = 0.02 # Delay for how long it takes the text to complete a scrollig animation.
UPDATE_DELAY = 50  # Delay used for reconnecting and pulling new values.

random_enabled = []
delay_values = []
quotes = []
colors = []
anims = []  # Arrays where we store the information pulled from our feeds.

last_anim = None
last_color = None # Used when random quotes is enabled.
last_quote = None  # Helps us make sure we dont display the same quote twice while random is enabled by storing past values.

def update_data():
    matrixportal.set_text("Connecting...", 1)  # Displaying the text "connecting" on the static textbox.

    if status_offline == True:  # Function used for testing.
        matrixportal.set_text("Offline", 1) # Displaying the text "offline" on the static textbox.
        print("Offline") # Printing to the console "offline"

    try:
        quotes_data = matrixportal.get_io_data( # Using the function on the matrixportal library "get_io_data" to gather values from our feeds in adafruit IO.
            QUOTES_FEED # Specifying which feed we are choosing to gather our information from.
        )
        color_data = matrixportal.get_io_data(COLORS_FEED) # Using the same function in every variable to gather values from our feeds in adafruit IO.
        anim_data = matrixportal.get_io_data(ANIM_FEED)
        random_data = matrixportal.get_io_data(RANDOM_FEED)
        delay_data = matrixportal.get_io_data(DELAY_FEED)

        random_enabled.clear() # Clearing any old values in the arrays before we update them.
        delay_values.clear()
        quotes.clear()
        colors.clear()
        anims.clear()

        for json_data in random_data: # "for json_data" used for handling data being pulled from our feeds in adafruit IO.
            random_enabled.append( # Using ".append" to add our data to our arrays.
                matrixportal.network.json_traverse(json_data, ["value"]) # Adding every value from our feeds in adafruit IO.
            )
        for json_data in delay_data:
            delay_values.append(matrixportal.network.json_traverse(json_data, ["value"]))
        for json_data in quotes_data:
            quotes.append(matrixportal.network.json_traverse(json_data, ["value"]))
        for json_data in color_data:
            colors.append(matrixportal.network.json_traverse(json_data, ["value"]))
        for json_data in anim_data:
            anims.append(
                matrixportal.network.json_traverse(json_data, ["value"])
            )

        print(random_enabled)
        print(delay_values)
        print(colors)
        print(quotes)
        print(anims)  # Printing every value we have pulled from our feeds and added to our arrays to store.

    except Exception as error: # Usually goes through this code if the connect was dropped or there was some issue with the data gathered.
        print(error) # Printing error to the console.
    if not quotes or not colors: # If you do not have values in your feeds the code cannot run.
        raise RuntimeError("Feed Issue") # Printing to the console as an error.

update_data() # Updating our data for the first time (this will only happen once until the last_update and update delay equals to current time)
last_update = time.monotonic() # Grabbing the time after the first update to queue our next update.

quote_index = None # Used when random quotes is enabled.
color_index = None # These variables will be used if the last quote is the same as the current quote.
anim_index = None

while True:
    print(last_quote)
    print(quote_index)
    matrixportal.set_text("", 1) # Clearing our static box from saying "Connecting"

    set_random = int(random_enabled[0]) # Turning our string values in our array to int values (random_enabled[0] will get us the value on top and determine if random is enabled)
    if set_random == 1: # If set_random equal to one enable random quotes & colors
        if len(quotes) > 1 and last_quote is not None: # If we have not displayed text then display text.
            print("step")
            while quote_index == last_quote: # If we pulled the same text twice pull again.
                print("tap")
                quote_index = random.randrange(0, len(quotes)) # Used to: pick a the text to display at random.
        else: # If we have already displayed text then pull at random.
            print("bang")
            quote_index = random.randrange(0, len(quotes))
        last_quote = quote_index # Storing the text we displayed in our index to keep track and record (used to make sure we always display a new random quote)
        if len(colors) > 1 and last_color is not None: # Code for picking random text is identical for picking a random color.
            while color_index == last_color:
                color_index = random.randrange(0, len(colors))
        else:
            color_index = random.randrange(0, len(colors))
        last_color = color_index
    if set_random == 2:
        if len(colors) > 1 and last_color is not None:
            while color_index == last_color:
                color_index = random.randrange(0, len(colors))
        else:
            color_index = random.randrange(0, len(colors))
        last_color = color_index
    if set_random == 3:
        if len(quotes) > 1 and last_quote is not None:
            while quote_index == last_quote:
                quote_index = random.randrange(0, len(quotes))
        else:
            quote_index = random.randrange(0, len(quotes))
        last_quote = quote_index
    if set_random == 4:
        print("logic")
        cycle_i = 0
        while cycle_i < len(quotes):
            print ("goop")
            print(quotes[cycle_i])
            # quote_index = quotes[cycle_i]
            cycle_i = cycle_i + 1
    if set_random < 1: # If random quotes and colors is not enabled then choose the color and quote that are on top.
        print("break")
        while quote_index == last_quote:
            quote_index = 0
        while color_index == last_color:
            color_index = 0
        while anim_index == last_anim: # We do not choose a random animation ever because it will become buggy.
            anim_index = 0 # We are pulling the value that is held in the array's "0" value / the value on top.

    #if animations_enabled == True: # If our testing / debug varible is true then we let the lines for our animation system run.
    set_animation = int(anims[0]) # Turning our string values in our array to int values (anims[0] will get us the value on top and determine what type of animation we use)
    if set_animation == 1: # If the top value equals to "1" we run our first animation.
        matrixportal.set_text(cycle_i) # Display the text on our scrolling text box (results in a plain scrolling text animation)
    if set_animation == 2 and set_animation != 1: # If the top value equals to "2" we run our second animation.
        matrixportal.set_text(quotes[quote_index], 1) # Display the text on our static text box (results in a plain static text)
        matrixportal.set_text("") # Clear our scrolling textbox.
    if set_animation < 0.98: # Else statement caused issues here so using different logic (will function if a value outside the range of the animation values is selected)
        matrixportal.set_text(quotes[quote_index]) # If animation value is outside our range we default into our plain scrolling animation (plain scrolling text animation)
        print("Animation does not exist") # Print to the console the selected animation does not exist.

    matrixportal.set_text_color(colors[color_index]) # Setting our colors.

    if set_animation == 2: # If our animation has a static textbox we dont need to use the "scroll_text" function
        print("Place-holder") # This will be used for other animations and text that involve a static text box (for now just a placeholder to fulfill our logic)
    else: # If we dont use a static textbox use the "scroll_text" function to scroll our text.
        matrixportal.scroll_text(SCROLL_DELAY) # Scrolling our text.

    set_delay = int(delay_values[0]) # Turning our string values in our array to int values (delay_values[0] will give us the value on top and determine how long it will take before we update our data again)
    UPDATE_DELAY = set_delay + 10 # Setting our update delay to the value we got from our feeds (if our update delay is below 10 issues will occur)
    if time.monotonic() > last_update + UPDATE_DELAY: # If our last update and delay equal current time then start to update from our feeds again.
        update_data() # Running the function that will update our data.
        last_update = time.monotonic() # Updating the last time we updated our data to our variable so it can function properly.
