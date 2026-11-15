import tkinter as tk
from view.vista import Vista

if __name__ == "__main__":
    ventana = tk.Tk()
    Vista(ventana)
    ventana.mainloop()