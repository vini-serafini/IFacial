import tkinter as tk

janela = tk.Tk()
janela.title("Teste")
janela.geometry("300x150")

tk.Label(janela, text="Se você está vendo isso, o Tkinter funciona.").pack(pady=20)

janela.mainloop()