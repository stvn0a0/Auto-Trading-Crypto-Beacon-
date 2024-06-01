import ccxt
import time
import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Replace with your crypto exchange and pairs
exchange = ccxt.binance()
pairs = ['BTC/USDT', 'ETH/USDT', 'LTC/USDT']  # Example pairs

# Update the port to match your Arduino's port
arduino_port = '/dev/tty.usbmodem144201'  # Change to your Arduino's port
arduino = serial.Serial(arduino_port, 9600)

price_history = {pair: [] for pair in pairs}

def get_crypto_data():
    prices = {}
    for pair in pairs:
        ticker = exchange.fetch_ticker(pair)
        prices[pair] = ticker['close']
    return prices

def analyze_data(prices):
    signals = {}
    for pair in pairs:
        moving_average_short = 20
        moving_average_long = 50
        
        if pair not in price_history:
            price_history[pair] = []

        price_history[pair].append(prices[pair])
        if len(price_history[pair]) > moving_average_long:
            short_ma = sum(price_history[pair][-moving_average_short:]) / moving_average_short
            long_ma = sum(price_history[pair][-moving_average_long:]) / moving_average_long
            
            if short_ma > long_ma:
                signals[pair] = 'BUY'
            elif short_ma < long_ma:
                signals[pair] = 'SELL'
            else:
                signals[pair] = 'HOLD'
        else:
            signals[pair] = 'HOLD'

    return signals

def update_plot(frame):
    prices = get_crypto_data()
    signals = analyze_data(prices)
    
    for pair in pairs:
        price_history[pair].append(prices[pair])
        if len(price_history[pair]) > 100:
            price_history[pair].pop(0)
    
    ax1.clear()
    ax2.clear()
    ax3.clear()
    
    ax1.plot(price_history['BTC/USDT'], label='BTC/USDT')
    ax1.legend(loc='upper left')
    ax1.set_title('BTC/USDT Price')
    
    ax2.plot(price_history['ETH/USDT'], label='ETH/USDT')
    ax2.legend(loc='upper left')
    ax2.set_title('ETH/USDT Price')
    
    ax3.plot(price_history['LTC/USDT'], label='LTC/USDT')
    ax3.legend(loc='upper left')
    ax3.set_title('LTC/USDT Price')
    
    plt.xlabel('Time')
    plt.ylabel('Price')

    # Send signals to Arduino
    for pair, signal in signals.items():
        if pair == 'BTC/USDT':
            if signal == 'BUY':
                arduino.write(b'B')
            elif signal == 'SELL':
                arduino.write(b'S')
            else:
                arduino.write(b'H')
        elif pair == 'ETH/USDT':
            if signal == 'BUY':
                arduino.write(b'b')
            elif signal == 'SELL':
                arduino.write(b's')
            else:
                arduino.write(b'h')
        elif pair == 'LTC/USDT':
            if signal == 'BUY':
                arduino.write(b'R')
            elif signal == 'SELL':
                arduino.write(b'G')
            else:
                arduino.write(b'N')
    
    print(f"Prices: {prices}, Signals: {signals}")  # Debug print

# Set up the plot
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 15))
ani = animation.FuncAnimation(fig, update_plot, interval=1000, cache_frame_data=False)  # Update every 1 second

plt.tight_layout()
plt.show()
