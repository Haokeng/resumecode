import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import mpl_finance as mpf
import seaborn as sns
import talib
import yfinance as yf
from datetime import datetime
from tkinter import *
import tkinter as tk
import matplotlib.gridspec as gridspec
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
def plot_stock():
    # get the ticker symbol and time period from the entries
    ticker = entry_ticker.get()
    start_date = datetime.strptime(entry_start_date.get(), '%Y-%m-%d')
    end_date = datetime.strptime(entry_end_date.get(), '%Y-%m-%d')
    
    # download data from Yahoo Finance
    df = yf.download(ticker, start=start_date, end=end_date)
    
    # convert index to string format with '%Y-%m-%d'
    df.index = df.index.strftime('%Y-%m-%d')

    # calculate moving averages
    sma_10 = talib.SMA(np.array(df['Close']), 10)
    sma_30 = talib.SMA(np.array(df['Close']), 30)
    sma_60 = talib.SMA(np.array(df['Close']), 60)

    # create figure and axis
    fig = plt.figure(figsize=(12, 8))
    gs = fig.add_gridspec(nrows=2, ncols=1, height_ratios=[2, 1])

    ax0 = fig.add_subplot(gs[0])
    ax1 = fig.add_subplot(gs[1], sharex=ax0)

    # plot moving averages and candlestick chart
    ax0.plot(sma_10, label='10-day SMA')
    ax0.plot(sma_30, label='30-day SMA')
    ax0.plot(sma_60, label='60-day SMA')
    mpf.candlestick2_ochl(ax0, df['Open'], df['Close'], df['High'], df['Low'],
                          width=0.6, colorup='r', colordown='g', alpha=0.75)

    # set x-axis ticks and labels for the candlestick chart
    ax0.set_xticks(range(0, len(df.index), 10))
    ax0.set_xticklabels(df.index[::10], rotation=45, ha='right')

    # plot volume chart
    mpf.volume_overlay(ax1, df['Open'], df['Close'], df['Volume'],
                       colorup='r', colordown='g', width=0.6, alpha=0.8)

    # set title and legend
    ax0.set_title(f'{ticker} Stock Price')
    ax0.legend()

    # create a Tkinter window
    root = tk.Tk()
    root.title(f'{ticker} Stock Price')

    # add a Matplotlib figure to the Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    # add a Matplotlib toolbar to the Tkinter window
    toolbar = NavigationToolbar2Tk(canvas, root)
    toolbar.update()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    # show the Tkinter window
    tk.mainloop()

# create GUI window
root = Tk()
root.title("Stock Price Chart")

# create labels and entries for ticker symbol and time period
label_ticker = Label(root, text="股票代號:")
label_ticker.grid(row=0, column=0)
entry_ticker = Entry(root)
entry_ticker.grid(row=0, column=1)

label_start_date = Label(root, text="開始日期 (YYYY-MM-DD):")
label_start_date.grid(row=1, column=0)
entry_start_date = Entry(root)
entry_start_date.grid(row=1, column=1)

label_end_date = Label(root, text="結束日期 (YYYY-MM-DD):")
label_end_date.grid(row=2, column=0)
entry_end_date = Entry(root)
entry_end_date.grid(row=2, column=1)

# create button to display stock chart
button_plot = Button(root, text="顯示圖表", command=plot_stock)
button_plot.grid(row=3, column=1)

root.mainloop()