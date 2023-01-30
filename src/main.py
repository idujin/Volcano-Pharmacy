import tkinter as tk
from tkinter import filedialog
import pandas as pd
from enum import Enum
import numpy as np
class WhichPath(Enum):
    AM = 0
    PM = 1
    INVEN =2


class Volcano:
    def __init__(self, main_window):
        self.am_path = ""
        self.pm_path = ""
        self.inventory_path = "../doc/Inventory2.xlsx"
        self.main = main_window
        self.df_am =pd.DataFrame()
        self.df_pm =pd.DataFrame()
        self.df_inven = pd.DataFrame()

        self.am_sales_button_ = tk.Button(main_window, text="오전 판매현황", command= self.update_am)
        self.am_sales_button_.place(x=10, y=10)
        self.pm_sales_button_ = tk.Button(main_window, text="오후 판매현황", command= self.update_pm)
        self.pm_sales_button_.place(x=10, y=50)

        self.inven_button_ = tk.Button(main_window, text="쟁여놓는약 변경", command=self.update_inventory)
        self.inven_button_.place(x=10, y=90)

        self.am_path_label_ = tk.Label(main_window, text="None")
        self.am_path_label_.place(x=120, y=12)
        self.pm_path_label_ = tk.Label(main_window, text="None")
        self.pm_path_label_.place(x=120, y=52)
        self.inven_path_label_ = tk.Label(main_window, text= self.inventory_path)
        self.inven_path_label_.place(x=130, y=92)

        self.am_export_button_ = tk.Button(main_window, text = "오전 필요수량 계산", height= 2, width=10,
                                           command = self.export_am_order)
        self.am_export_button_.place(x=650, y=10)

        self.pm_export_button_ = tk.Button(main_window, text="오후 필요수량 계산", height=2, width=10,
                                           command = self.export_pm_order)
        self.pm_export_button_.place(x=650, y=70)

    def export_am_order(self):
        if(self.df_am.empty):
            pop_err = tk.Toplevel(self.main)
            pop_err.geometry("250x50")
            pop_err.title("Error")
            tk.Label(pop_err, text="오전판매 수량 파일을 먼저 로드하세요.").pack()
            return

        if(self.df_inven.empty):
            try:
                self.df_inven = self.__read_excel_file(self.inventory_path)
            except:
                pop_err = tk.Toplevel(self.main)
                pop_err.geometry("250x50")
                pop_err.title("Error")
                tk.Label(pop_err, text="쟁여놓는약 파일을 확인하세요.").pack()
                return


        sales = self.df_am[["약품명칭", "약품코드", "처방수량"]]
        all_codes = self.df_am["약품코드"].to_numpy().astype(str)
        exclude_codes = self.df_inven["약품코드"].to_numpy().astype(str)
        drop_list =[]

        for i, code in enumerate(all_codes):
            if(code in exclude_codes):
                drop_list.append(sales.index[i])
        sales_export = sales.drop(drop_list)
        try:
            sales_export.to_excel("../doc/export_AM.xlsx")
            pop_err = tk.Toplevel(self.main)
            pop_err.geometry("250x50")
            pop_err.title("Message")
            tk.Label(pop_err, text="Exported!").pack()
        except:
            pop_err = tk.Toplevel(self.main)
            pop_err.geometry("250x50")
            pop_err.title("Error")
            tk.Label(pop_err, text="Export failed!").pack()


    def export_pm_order(self):
        if (self.df_am.empty or not self.pm_path):
            pop_err = tk.Toplevel(self.main)
            pop_err.geometry("250x50")
            pop_err.title("Error")
            if(self.df_am.empty):
                tk.Label(pop_err, text="오전판매 수량 파일을 먼저 로드하세요.").pack()
            elif(self.df_pm.empty):
                tk.Label(pop_err, text="오후판매 수량 파일을 먼저 로드하세요.").pack()
            else:
                tk.Label(pop_err, text="오전/오후판매 수량 파일을 먼저 로드하세요.").pack()
            return
        if (self.df_inven.empty):
            try:
                self.df_inven = self.__read_excel_file(self.inventory_path)
            except:
                pop_err = tk.Toplevel(self.main)
                pop_err.geometry("250x50")
                pop_err.title("Error")
                tk.Label(pop_err, text="쟁여놓는약 파일을 확인하세요.").pack()

        am_sales = self.df_am["처방수량"].to_numpy().astype(str)
        pm_sales = self.df_pm["처방수량"].to_numpy().astype(str)
        for i in range(len(am_sales)):
            am_sales[i] = am_sales[i].replace(',','')
            pm_sales[i] = pm_sales[i].replace(',','')

        am_sales = am_sales.astype(np.float32)
        pm_sales = pm_sales.astype(np.float32)

        exclude_codes = self.df_inven["약품코드"].to_numpy().astype(str)
        pm_codes = self.df_pm["약품코드"].to_numpy().astype(str)

        drop_list = []
        df_pm_only = self.df_pm.copy()

        for i, code in enumerate(pm_codes):
            val = pm_sales[i] - am_sales[i]
            df_pm_only.at[i, "처방수량"] = val
            if (code in exclude_codes or pm_sales[i] == am_sales[i]):
                drop_list.append(i)
        sales_export = df_pm_only.drop(drop_list)
        try:
            sales_export.to_excel("../doc/export_PM.xlsx")
            pop_err = tk.Toplevel(self.main)
            pop_err.geometry("250x50")
            pop_err.title("Message")
            tk.Label(pop_err, text="Exported!").pack()
        except:
            pop_err = tk.Toplevel(self.main)
            pop_err.geometry("250x50")
            pop_err.title("Error")
            tk.Label(pop_err, text="Export failed!").pack()


    def update_am(self):
        path = self.__get_file_path()
        self.am_path_label_.config(text=path)
        self.am_path = path
        df = self.__read_excel_file(self.am_path)
        self.df_am = df[["약품명칭", "약품코드", "처방수량"]]

    def update_pm(self):
        path = self.__get_file_path()
        self.pm_path_label_.config(text=path)
        self.pm_path = path
        df = self.__read_excel_file(self.pm_path)
        self.df_pm = df[["약품명칭", "약품코드", "처방수량"]]

    def update_inventory(self):
        path = self.__get_file_path()
        self.inven_path_label_.config(text=path)
        self.inventory_path = path
        try:
            self.df_inven = self.__read_excel_file(path)
        except:
            pop_err = tk.Toplevel(self.main)
            pop_err.geometry("250x50")
            pop_err.title("Error")
            tk.Label(pop_err, text="쟁여놓는약 파일을 확인하세요.").pack()
            return


    def __get_file_path(self):
        path = filedialog.askopenfilename(title="Select file",
                                          filetypes=[('Excel files', '*.xls *.xlsx')])
        return path

    def __read_excel_file(self, path):
        try:
            df = pd.read_excel(path)
        except:
            raise Exception("재고 파일을 확인하세요.")
        return df

if __name__ == '__main__':

    main = tk.Tk(className=" Volcano Pharmacy ")
    main.geometry("800x180")
    vol = Volcano(main)

    main.mainloop()


