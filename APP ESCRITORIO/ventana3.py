import tkinter as tk

class Ventana3:
    def __init__(self, menu, ventana_principal):
        labelFont = ("Bold Italic", 20, 'bold')
        bottonFont = ('Bold Italic', 10)

        self.menu = menu
        self.ventana_principal = ventana_principal
        self.menu.title('Caracterización Magnotoeléctrica invertida')
        self.menu.geometry('1000x600')
        self.menu.minsize(900, 500)  # HOTFIX

        # CAMBIAR
        self.menu.grid_columnconfigure(0, weight=1)
        self.menu.grid_columnconfigure(1, weight=4)
        self.menu.grid_rowconfigure(1, weight=1)

        # Titulo
        tk.Label(self.menu, text='Caracterización Magnotoeléctrica invertida', font=labelFont, bg='#D9D9D9').grid(row=0, column=0,columnspan=2,sticky='nsew')

        # Sidebar
        self.scrollable_frame = tk.Frame(self.menu, bg="#A6C3FF")
        self.scrollable_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        self.scrollable_frame.grid_rowconfigure(13, weight=1)  # Intento de Layoutresponsiva

        # el scrolling
        self.canvas = tk.Canvas(self.scrollable_frame, bg="#A6C3FF", highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True)

        self.scrollable_frame = tk.Frame(self.canvas, bg="#A6C3FF")
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # bindeo para el scroll
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        # Right_Frame(Graficos)
        right_frame = tk.Frame(self.menu, bg="#1F6095")
        right_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=5)
        right_frame.grid_columnconfigure(0, weight=1)
        right_frame.grid_rowconfigure(0, weight=1)

        # Sidebar contents
        tk.Label(self.scrollable_frame, text="Nombre", bg="#A6C3FF").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        tk.Entry(self.scrollable_frame, width=30).grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        # las labels con los sliders
        self.add_slider(self.scrollable_frame, "Corriente Fija", 3)
        self.add_slider(self.scrollable_frame, "Saturacion de Campo [G]", 5)
        self.add_slider(self.scrollable_frame, "Frecuencia de Muestreo [s]", 7)

        # Linea Tendencia
        tk.Checkbutton(self.scrollable_frame, text="Línea Tendencia", bg="#A6C3FF").grid(row=9, column=0, padx=10,
                                                                                         pady=5, sticky="w")

        # row btn
        button_frame = tk.Frame(self.scrollable_frame, bg="#A6C3FF")
        button_frame.grid(row=10, column=0, padx=10, pady=5, sticky="ew")
        button_frame.grid_columnconfigure((0, 1, 2), weight=1)

        tk.Button(button_frame, text="Comenzar", width=10).grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        tk.Button(button_frame, text="Guardar Sección", width=10).grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        tk.Button(button_frame, text="Guardar Prueba", width=10).grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        # cargar los btn
        tk.Button(self.scrollable_frame, text="Cargar Sección", width=25).grid(row=12, column=0, padx=10, pady=10,
                                                                               sticky="ew")

        # Botón volver below the sidebar
        btn_volver = tk.Button(self.menu, text="Volver a menu", command=self.volver)
        btn_volver.grid(row=2, column=0, pady=10)

    def add_slider(self, frame, text, row):
        slider_frame = tk.Frame(frame, bg="#A6C3FF")
        slider_frame.grid(row=row, column=0, padx=10, pady=5, sticky="ew")
        slider_frame.grid_columnconfigure(0, weight=1)

        tk.Label(slider_frame, text=text, bg="#A6C3FF").grid(row=0, column=0, sticky="w")
        tk.Scale(slider_frame, from_=0, to=1, orient=tk.HORIZONTAL, resolution=0.01, bg="#A6C3FF").grid(row=1, column=0,
                                                                                                        sticky="ew")

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def volver(self):
        self.menu.withdraw()
        self.ventana_principal.deiconify()