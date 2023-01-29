import tkinter as tk
from tkinter import filedialog
import pandas as pd
from enum import Enum
class WhichPath(Enum):
    AM = 0
    PM = 1
    INVEN =2


class Volcano:
    def __init__(self, main_window):
        self.am_path_ = ""
        self.pm_path_ = ""
        self.inventory_path_ = "../doc/Inventory.xlsx"
        self.main_ = main_window


        self.am_sales_button_ = tk.Button(main_window, text="오전 판매현황", command= self.update_am)
        self.am_sales_button_.place(x=10, y=10)
        self.pm_sales_button_ = tk.Button(main_window, text="오후 판매현황", command= self.update_pm)
        self.pm_sales_button_.place(x=10, y=50)

        self.inven_button_ = tk.Button(main_window, text="쟁여놓는약 변경", command=self.update_inventory)
        self.inven_button_.place(x=10, y=100)

        self.am_path_label_ = tk.Label(main_window, text="None")
        self.am_path_label_.place(x=120, y=12)
        self.pm_path_label_ = tk.Label(main_window, text="None")
        self.pm_path_label_.place(x=120, y=52)
        self.inven_path_label_ = tk.Label(main_window, text= self.inventory_path_)
        self.inven_path_label_.place(x=130, y=102)

    def update_am(self):
        path = self.__get_file_path()
        self.am_path_label_.config(text=path)
        self.am_path_ = path

    def update_pm(self):
        path = self.__get_file_path()
        self.pm_path_label_.config(text=path)
        self.pm_path_ = path

    def update_inventory(self):
        path = self.__get_file_path()
        self.inven_path_label_.config(text=path)
        self.inventory_path_ = path

    def update_path(self, label, which_path):
        path = self.get_file_path(which_path)
        self.change_label(label, path)

    def __get_file_path(self):
        path = filedialog.askopenfilename(title="Select file",
                                          filetypes=[('Excel files', '*.xls *.xlsx')])
        return path

    def read_excel_file(self, path):
        df = pd.read_excel(path)
        return df

if __name__ == '__main__':

    main = tk.Tk(className="Volcano Pharmacy")
    main.geometry("700x200")
    vol = Volcano(main)



    main.mainloop()


