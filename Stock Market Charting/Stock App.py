import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from alpha_vantage.timeseries import TimeSeries
import matplotlib
import matplotlib.pyplot as plt
from mpl_finance import candlestick_ohlc
from matplotlib import style
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.animation as animation 
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter
import matplotlib.ticker as mticker
import pandas as pd
from pandas.plotting import register_matplotlib_converters
import threading
import numpy as np
import datetime as date


LARGE_FONT = ('AdobeHeitiStd-Regular', 14)
SMALL_FONT = ('Verdana', 8)
fig = plt.Figure()
axes = fig.add_subplot(111)


class Functionality:
    #Default values
    def __init__(self):
        self.ResampleSize = '15min'
        self.datapace = '1d'
        self.DCounter = 9000
        self.candlewidth = 0.0005
        self.Symbol = 'AAPL'
    
        
    def ChangeSampleSize( self, size, width):    
        if self.datapace == '7d' and self.ResampleSize == '1min':
            messagebox.showwarning('Info', 'You have chosen to much data')
        else:
            self.ResampleSize = size
            DCounter = 9000
            self.candlewidth = width

    def ChangeTimeFrame(self,tf):
        if tf == '7d' and self.ResampleSize  == '1Min':
            messagebox.showwarning('Info', 'You have chosen to much data')
        else:
            self.dataPace = tf
            DCounter = 9000
    
    def ChangeSymbol(self,sym):
        sym = sym.get()
        self.Symbol = str(sym)
        

    def animate(self, i):#  1min, 5min, 15min, 30min, 60min allowed time frames
        ts = TimeSeries(key='TK8VW7JEPYHWNMA0', output_format='pandas')
        data, meta_data = ts.get_intraday(symbol='AAPL',interval='1min',outputsize='compact') 
        df = pd.DataFrame(data)
        df.to_csv('stock data.csv')
        storage = pd.read_csv('stock data.csv', parse_dates=True, index_col=0, infer_datetime_format=True)
        storage.reset_index(inplace=True)
        storage['datestamps'] = np.array(storage['date']).astype('datetime64[s]')
        datestamps = storage['date'].tolist()
            
        register_matplotlib_converters(explicit=True)
        storage['MPL dates'] = storage['date'].apply(lambda dates: mdates.date2num(dates.to_pydatetime()))
        storage = storage.set_index('date')
        title = 'Apple Stock Chart'      
                
        OHLC = storage['4. close'].resample(self.ResampleSize).ohlc()
        OHLC =OHLC.dropna()
        OHLC['datecopy'] = OHLC.index
        OHLC['MPL Dates'] = OHLC['datecopy'].apply(lambda date: mdates.date2num(date.to_pydatetime()))           
        del OHLC['datecopy']
                
        axes.clear()
        candlestick_ohlc(axes, OHLC[['MPL Dates','open', 'high', 'low', 'close']].values , width=self.candlewidth, colorup ='g', colordown='r')
        axes.xaxis_date()
        axes.xaxis.set_major_locator(mticker.MaxNLocator(5))
        axes.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M"))
        axes.set_ylabel('Price')
        axes.set_title(title)
        

class Stock_App(tk.Tk, Functionality):
    def __init__(self):
        tk.Tk.__init__(self)
        Functionality.__init__(self)
        tk.Tk.title(self,'Algo Trade')
        tk.Tk.iconbitmap(self, 'Stock_icon.ico')
        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0,weight=1)
        container.grid_columnconfigure(0,weight=1)

        Menubar = tk.Menu(container)

        filemenu = tk.Menu(Menubar, tearoff=0)
        filemenu.add_command(label='Save Settings', command=lambda: messagebox.showinfo('Warning', 'Not supported yet'))
        filemenu.add_separator()
        filemenu.add_command(label='Exit', command=quit)
        Menubar.add_cascade(label='File', menu=filemenu)

        Tf_menu = tk.Menu(Menubar, tearoff=0)
        Tf_menu.add_command(label='1 Day',command=lambda: Functionality.ChangeTimeFrame('1d'))
        Tf_menu.add_command(label='3 Day',command=lambda: Functionality.ChangeTimeFrame('3d'))
        Tf_menu.add_command(label= '1 week',command=lambda: Functionality.ChangeTimeFrame('7d'))
        Menubar.add_cascade(label='Data Time Frame', menu=Tf_menu)
        
        OHLCi = tk.Menu(Menubar, tearoff=1)
        OHLCi.add_command(label='1 minute', command=lambda: self.ChangeSampleSize('1Min', 0.0005))
        OHLCi.add_command(label='5 minutes', command= lambda: self.ChangeSampleSize('5Min', 0.003))
        OHLCi.add_command(label='15 minutes', command=lambda: self.ChangeSampleSize('15Min', 0.008))
        OHLCi.add_command(label='30 minutes', command=lambda: self.ChangeSampleSize('30Min', 0.016))
        OHLCi.add_command(label='1 hour', command=lambda: self.ChangeSampleSize('60Min', 0.032 ))
        Menubar.add_cascade(label='Interval', menu=OHLCi)
        
        tk.Tk.config(self, menu=Menubar)
        
        self.frames = {}
        
        for F in (HomePage, PageOne, GraphPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame(HomePage)
            
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
                
                
class HomePage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text= 'Algo Trade Application', font=LARGE_FONT)
        label.pack()
        button = ttk.Button(self, text='Visit Page 1', command= lambda: controller.show_frame(PageOne))
        button.pack()
        button2 = ttk.Button(self, text='Graph Page', command= lambda: controller.show_frame(GraphPage))
        button2.pack()
    
class PageOne(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self, parent)
        label_1= ttk.Label(self, text='Page One')
        label_1.pack()
        button3 = tk.ttk.Button(self, text='Go Home', command= lambda: controller.show_frame(HomePage))
        button3.pack()

                
class GraphPage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self, parent)
        Symbol = tk.StringVar()
        label_2 = ttk.Label(self, text='Page Two')
        label_2.pack()
        button4 = tk.ttk.Button(self, text='Go Home', command= lambda: controller.show_frame(HomePage))
        button4.pack()
        style.use('ggplot')
        Entry = ttk.Entry(self, textvariable=Symbol, font=SMALL_FONT)
        Entry.place(relwidth=0.15, relheight=0.025)
        symbol_change_button = ttk.Button(self, text='Submit', command= lambda: self.ChangeSymbol(Symbol))
        symbol_change_button.place(relx=0.1,rely=0)
        
        canvas = FigureCanvasTkAgg(fig, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP,fill=tk.BOTH, expand=True)
        
        Toolbar = NavigationToolbar2Tk(canvas, self)
        Toolbar.update()
        canvas._tkcanvas.pack(side=tk.BOTTOM,fill=tk.BOTH, expand=True)



if __name__ == "__main__":
    app = Stock_App()
    app.geometry('1280x1024')
    ani = animation.FuncAnimation(fig, app.animate, interval=15000)
    app.mainloop()








