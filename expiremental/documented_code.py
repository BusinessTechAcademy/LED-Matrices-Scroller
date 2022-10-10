import time # imported for feed selection & delays
import random # imported for feed selection
import board # imported for basic board functions
import terminalio # imported for label and fonts
from adafruit_matrixportal.matrixportal import MatrixPortal

# Setting up display
matrixportal = MatrixPortal(status_neopixel=board.NEOPIXEL, debug=True)

# Creating the label
matrixportal.add_text(
    text_font=terminalio.FONT, # Applying the font
    text_position=(2, (matrixportal.graphics.display.height // 2) - 1), #Adjusting label height
    scrolling=True, # Applying text scrolling
)

QUOTES_FEED = "sign-quotes.signtext" # Get the information from adafruit io
COLORS_FEED = "sign-quotes.signcolor" # Example format: "group.feed"
SCROLL_DELAY = 0.02 # Speed at which text scrolls at
UPDATE_DELAY = 600 # Speed at which data is pulled from the feeds

quotes = [] # Setting up arrays: colors and quotes
colors = [] # Will pull from the feeds in the adafruit IO
last_color = None # Creating variables: last_quote and last_color
last_quote = None # These variables are used so that the feed doesn't pull the same value randomly

# Function used to update data to the matrixportal
def update_data():
    matrixportal.set_text("Connecting", 1) # Drawing "Connecting" on the matrix to show that the update has started

    try:
        quotes_data = matrixportal.get_io_data(QUOTES_FEED) # Gathering quotes from the adafruit io
        quotes.clear() # Only pulling one quote from the feed
        for json_data in quotes_data:
            quotes.append(matrixportal.network.json_traverse(json_data, ["value"])) # Making data applicable to matrixportal
    except Exception as error: # Telling it to stop updating if there is a connection error
        matrixportal.set_text(" error ", 1) # Drawing "error" on the matrix to show that an error has occured

    try:
        color_data = matrixportal.get_io_data(COLORS_FEED) # Gathering colors from the adafruit io
        colors.clear() # Only pulling one color from the feed
        for json_data in color_data:
            colors.append(matrixportal.network.json_traverse(json_data, ["value"]))# Making data applicable to matrixportal
    except Exception as error: # Telling it to stop updating if there is a connection error
        matrixportal.set_text(" error ", 1) # Drawing "error" on the matrix to show that an error has occured

    if not quotes: # If there are no quotes in the feeds or the feed doesnt exist display an error
        raise RuntimeError("Please add at least one quote to your feeds")
    matrixportal.set_text(" No Quotes! ", 1) # Drawing "No Quotes!" on the matrix to show that there is a problem with the quotes
    if not colors: # If there are no color in the feeds or the feed doesnt exist display an error
        raise RuntimeError("Please add at least one color to your feeds")
    matrixportal.set_text(" No Colors! ", 1) # Drawing "No Colors!" on the matrix to show that there is a problem with the quotes


update_data() # Running the update function
last_update = time.monotonic() # Updating time to monotonic so scrolling and delays are consistent
matrixportal.set_text(" ", 1) # Between updates clear the text & creates blinking effect
quote_index = None # Telling us that the update function should be ran because there is no current quote or color
color_index = None

while True:

    if len(quotes) > 1 and last_quote is not None: # Choosing a random quote
        while quote_index == last_quote: # Active when the data is pulled and is the same as the last pull
            quote_index = random.randrange(0, len(quotes)) # Forces another pull from the feed to prevent the same text from displaying twice
    else:
        quote_index = random.randrange(0, len(quotes)) # Used if the same quote isn't pulled and runs normally
    last_quote = quote_index # Telling us that a quote has be chosen and not to pick it twice by changing the value of last_quote to it

    if len(colors) > 1 and last_color is not None: # Choosing a random color
        while color_index == last_color: # Active when the data is pulled and is the same as the last pull
            color_index = random.randrange(0, len(colors)) # Forces another pull from the feed to prevent the same color from displaying twice
    else:
        color_index = random.randrange(0, len(colors)) # Used if the same color isn't pulled and runs normally
    last_color = color_index  # Telling us that a quote has be chosen and not to pick it twice by changing the value of last_quote to it

    # Set the quote text
    matrixportal.set_text(quotes[quote_index])

    # Set the text color
    matrixportal.set_text_color(colors[color_index])

    # Scroll it
    matrixportal.scroll_text(SCROLL_DELAY)

    if time.monotonic() > last_update + UPDATE_DELAY: # Restart the delay to re-run the function
        update_data() # Running the updating function
        last_update = time.monotonic() # Updating time to monotonic so scrolling and delays are consistent
