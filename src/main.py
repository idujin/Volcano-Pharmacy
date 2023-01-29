import tkinter as tk
from tkinter import filedialog
import pandas as pd

def get_file_path():
    root = tk.Tk()
    root.overrideredirect(True)
    root.attributes("-alpha", 0)
    path = filedialog.askopenfilename(title = "Select file",
                                      filetypes=[('Excel files','*.xls *.xlsx')])
    root.destroy()
    return path
def read_excel_file(path):
    df = pd.read_excel(path)
    return df

if __name__ == '__main__':
    df = read_excel_file(get_file_path())
