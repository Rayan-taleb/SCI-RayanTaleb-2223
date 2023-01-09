#
import tkinter as tk
import numpy as np
import numpy_financial as fin
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
class FinancialCalculator(tk.Frame):
  def __init__(self, root):
    super().__init__(root)
    self.discount_rate_label = tk.Label(self, text="Discount Rate:")
    self.discount_rate_entry = tk.Entry(self)
    self.cash_flow_label = tk.Label(self, text="Cash Flow:")
    self.cash_flow_entry = tk.Entry(self)
    self.interest_rate_label = tk.Label(self, text="Interest Rate:")
    self.interest_rate_entry = tk.Entry(self)
    self.irr_button = tk.Button(self, text="Calculate IRR", command=self.calculate_irr)
    self.npv_button = tk.Button(self, text="Calculate NPV", command=self.calculate_npv)
    self.fv_button = tk.Button(self, text="Calculate FV", command=self.calculate_fv)
    self.result_label = tk.Label(self, text="Result:")
    self.result_value_label = tk.Label(self)
    self.periodic_payment_label = tk.Label(self, text="Periodic Payment:")
    self.periodic_payment_entry = tk.Entry(self)
    self.present_value_label = tk.Label(self, text="Present Value:")
    self.present_value_entry = tk.Entry(self)
    
    self.discount_rate_label.grid(row=2, column=0, sticky="W")
    self.discount_rate_entry.grid(row=2, column=1)
    self.cash_flow_label.grid(row=0, column=0, sticky="W")
    self.cash_flow_entry.grid(row=0, column=1)
    self.interest_rate_label.grid(row=1, column=0, sticky="W")
    self.interest_rate_entry.grid(row=1, column=1)
    self.irr_button.grid(row=2, column=3, columnspan=2)
    self.npv_button.grid(row=3, column=3, columnspan=2)
    self.fv_button.grid(row=4, column=3, columnspan=2)
    self.result_label.grid(row=5, column=0, sticky="W")
    self.result_value_label.grid(row=5, column=1) 
    self.periodic_payment_label.grid(row=3, column=0, sticky="W")
    self.periodic_payment_entry.grid(row=3, column=1)
    self.present_value_label.grid(row=4, column=0, sticky="W")
    self.present_value_entry.grid(row=4, column=1)

  def discount_rate(self):
        discount_rate_str = self.discount_rate_entry.get()
        try:
            discount_rate = float(discount_rate_str)
        except ValueError:
            # Show an error message
            self.result_value_label.configure(text="Invalid input")
            # Return 0 as the discount rate
            return 0
        # Return the discount rate
        return discount_rate
        
  def calculate_irr(self):
        result = 0
        cash_flow = self.get_cash_flow()
        discount_rate = self.get_discount_rate()
        if any(x > 0 for x in cash_flow) and any(x < 0 for x in cash_flow):
               result = fin.irr(cash_flow)
        else:
               self.result_value_label.configure(text="Invalid cash flow")
        # Set the result value in the result label
        self.result_value_label.configure(text=result)
        # Plot the cash flow
        self.plot_cash_flow(cash_flow, result)
  def calculate_npv(self):
        cash_flow = self.get_cash_flow()
        interest_rate = self.get_interest_rate()
        discount_rate = self.get_discount_rate()
        result = fin.npv(discount_rate, cash_flow)
        self.result_value_label.configure(text=result)
        self.plot_cash_flow(cash_flow, result)
  def calculate_fv(self):
    
        cash_flow = self.get_cash_flow()
        interest_rate = self.get_interest_rate()
        result = fin.fv(interest_rate, len(cash_flow), 0, -cash_flow[0], when="end")
        discount_rate = self.get_discount_rate()
        result = fin.fv(discount_rate, len(cash_flow), 0, -cash_flow[0], when="end")
        self.result_value_label.configure(text=result)
        self.plot_cash_flow(cash_flow,result)

  def get_cash_flow(self):
    cash_flow_str = self.cash_flow_entry.get()
    try:
        cash_flow = [int(x) for x in cash_flow_str.split(",")]
    except ValueError:
        # Show an error message
        self.result_value_label.configure(text="Invalid input")
        # Return an empty list
        return []
    # Return the cash flow list
    return cash_flow

  def get_interest_rate(self):
    interest_rate_str = self.interest_rate_entry.get()
    try:
        interest_rate = float(interest_rate_str)
    except ValueError:
        # Show an error message
        self.result_value_label.configure(text="Invalid input")
        # Return 0 as the interest rate
        return 0
    # Return the interest rate
    return interest_rate

  def get_discount_rate(self):
      discount_rate_str = self.discount_rate_entry.get()
      try:
          discount_rate = float(discount_rate_str)
      except ValueError:
          # Show an error message
          self.result_value_label.configure(text="Invalid input")
          # Return 0 as the discount rate
          return 0
      # Return the discount rate
      return discount_rate

  def plot_cash_flow(self, cash_flow,result):
    # Create a new Figure and Axes
    fig, ax = plt.subplots()
    # Create a range of values from 0 to the number of cash flow entries
    x = range(len(cash_flow))
    # Plot the cash flow valuesS
    ax.plot(x, cash_flow,linestyle="solid")
    ax.text(0.5, 0.5, result, horizontalalignment="center", verticalalignment="center")
    # Create a FigureCanvasTkAgg widget
    canvas = FigureCanvasTkAgg(fig, self)
    # Add the canvas to the GUI window
    canvas.get_tk_widget().grid(row=6, column=0, columnspan=2)


root = tk.Tk()
root.title("Financial Calculator SCI")
root.geometry("800x800")
root.resizable(False, False)
frame = FinancialCalculator(root)
frame.pack()
root.mainloop()
