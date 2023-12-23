import tkinter as ttk
import requests
import json
import locale

# File to store configuration data
CONFIG_FILE = 'config.json'
locale_var = 'pt-BR'
locale.setlocale(locale.LC_ALL, locale_var)

def fetch_btc_price():
    response = requests.get(f'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies={get_currency()}')
    data = response.json()
    current_price = data["bitcoin"][get_currency()]
    formatted_price = locale.currency(current_price, grouping=True)  # Format the price based on the chosen currency
    btc_price.set(f'BTC Price: {formatted_price}')

    # Calculate and update the price difference
    comparison_price = comparison_price_var.get()
    if comparison_price is not None:
        price_difference = (current_price / comparison_price - 1) * 100
        difference_label.config(text=f'Price Difference: {price_difference:.2f}%')

def compare_price():
    fetch_btc_price()

    # Save the comparison price and currency to the configuration file
    save_configuration()

def save_configuration():
    # Get the comparison price and currency from the Entry widgets
    comparison_price = comparison_price_var.get()
    currency = currency_var.get()

    # Save the comparison price and currency to the configuration file
    with open(CONFIG_FILE, 'w') as config_file:
        json.dump({'comparison_price': comparison_price, 'currency': currency, 'locale': locale_var}, config_file)

def load_configuration():
    try:
        # Load configuration from the file
        with open(CONFIG_FILE, 'r') as config_file:
            config_data = json.load(config_file)

        # Set the loaded comparison price and currency to the Entry widgets
        comparison_price_var.set(config_data.get('comparison_price', None))
        currency_var.set(config_data.get('currency', 'usd'))

        # Set the system locale to use the user's default currency format
        # locale_var = config_data.get('locale', 'pt-BR')
        # locale.setlocale(locale.LC_ALL, locale_var)

    except FileNotFoundError:
        # If the file is not found (first run), ignore the exception
        pass

def get_currency():
    return currency_var.get().lower()

# Create the main window
app = ttk.Tk()
app.title('Bitcoin Price Widget')
app.attributes('-topmost', True)  # Always on top

# Variable to store BTC price
btc_price = ttk.StringVar()

# Label to display BTC price
label = ttk.Label(app, textvariable=btc_price, font=('Arial', 14))
label.pack(padx=10, pady=5)

# Label to display the price difference
difference_label = ttk.Label(app, text='Price Difference: N/A', font=('Arial', 12))
difference_label.pack(pady=5)

# Entry for user to input comparison price
comparison_price_var = ttk.DoubleVar()
comparison_entry = ttk.Entry(app, textvariable=comparison_price_var, width=10)
comparison_entry.pack(side='left', padx=5, pady=10)

# Entry for user to input currency
currency_var = ttk.StringVar()
currency_entry = ttk.Entry(app, textvariable=currency_var, width=5)
currency_entry.pack(side='left', padx=5, pady=10)

# Button to compare prices
compare_button = ttk.Button(app, text='Compare Price', command=compare_price)
compare_button.pack(side='left', padx=5, pady=10)

# Periodically fetch BTC price (e.g., every 5 minutes)
app.after(5 * 60 * 1000, fetch_btc_price)

# Load the configuration on application start
load_configuration()

# Run the Tkinter event loop
app.mainloop()
