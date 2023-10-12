import tkinter as tk

window = tk.Tk()

window.title("InstaPOP")
window.geometry("500x400")
window.resizable(0, 0)

test = tk.Button(text="CLICK", height=400, width=500, font=200)
test.pack(padx=5, pady=5, fill=tk.Y)

window.mainloop()
