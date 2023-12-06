import tkinter as tk
import requests

def fetch_btc_price():
    response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=brl,usd,eur,gbp')
    data = response.json()
    current_price = data["bitcoin"]["brl"]
    btc_price.set(f'BTC Price: ${current_price}')

    # Calculate and update the price difference
    comparison_price = comparison_price_var.get()
    if comparison_price is not None:
        price_difference = (current_price/comparison_price-1)*100
        difference_label.config(text=f'Price Difference: {price_difference:.2f}%')

# Function to compare prices
def compare_price():
    fetch_btc_price()

# Create the main window
app = tk.Tk()
app.title('Bitcoin Price Widget')

# Variable to store BTC price
btc_price = tk.StringVar()

# Label to display BTC price
label = tk.Label(app, textvariable=btc_price, font=('Arial', 14))
label.pack(pady=10)

# Label to display the price difference
difference_label = tk.Label(app, text='Price Difference: N/A', font=('Arial', 12))
difference_label.pack()

# Entry for user to input comparison price
comparison_price_var = tk.DoubleVar()
comparison_entry = tk.Entry(app, textvariable=comparison_price_var, width=10)
comparison_entry.pack()

# Button to compare prices
compare_button = tk.Button(app, text='Compare Price', command=compare_price)
compare_button.pack()

# Periodically fetch BTC price (e.g., every 5 minutes)
app.after(5 * 60 * 1000, fetch_btc_price)

# Run the Tkinter event loop
app.mainloop()
