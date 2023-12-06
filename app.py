import tkinter as ttk
import requests
import json

# File to store configuration data
CONFIG_FILE = 'config.json'

def fetch_btc_price():
    response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=brl,usd,eur,gbp')
    data = response.json()
    current_price = data["bitcoin"]["brl"]
    btc_price.set(f'BTC Price: ${current_price}')

    # Calculate and update the price difference
    comparison_price = comparison_price_var.get()
    if comparison_price is not None:
        price_difference = (current_price / comparison_price - 1) * 100
        difference_label.config(text=f'Price Difference: {price_difference:.2f}%')

def compare_price():
    fetch_btc_price()
    save_configuration()

def save_configuration():
    # Get the comparison price from the Entry widget
    comparison_price = comparison_price_var.get()
    # Save the comparison price to the configuration file
    with open(CONFIG_FILE, 'w') as config_file:
        json.dump({'comparison_price': comparison_price}, config_file)

def load_configuration():
    try:
        # Load configuration from the file
        with open(CONFIG_FILE, 'r') as config_file:
            config_data = json.load(config_file)
        # Set the loaded comparison price to the Entry widget
        comparison_price_var.set(config_data.get('comparison_price', None))

    except FileNotFoundError:
        # If the file is not found (first run), ignore the exception
        pass

# Create the main window
app = ttk.Tk()
app.title('Bitcoin Price Widget')

# Variable to store BTC price
btc_price = ttk.StringVar()

# Label to display BTC price
label = ttk.Label(app, textvariable=btc_price, font=('Arial', 14))
label.pack(pady=10)

# Label to display the price difference
difference_label = ttk.Label(app, text='Price Difference: N/A', font=('Arial', 12))
difference_label.pack()

# Entry for user to input comparison price
comparison_price_var = ttk.DoubleVar()
comparison_entry = ttk.Entry(app, textvariable=comparison_price_var, width=10)
comparison_entry.pack()

# Button to compare prices
compare_button = ttk.Button(app, text='Compare Price', command=compare_price)
compare_button.pack()

# Periodically fetch BTC price (e.g., every 5 minutes)
app.after(5 * 60 * 1000, fetch_btc_price)

# Load the configuration on application start
load_configuration()

# Run the Tkinter event loop
app.mainloop()
