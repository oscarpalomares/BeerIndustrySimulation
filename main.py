import tkinter as tk
from tkinter import ttk
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import pygame
import sys
import webbrowser
import re

class Cerveceria:
    costo_energia_segundos = 0.099
    litros_producidos = 0

    class Fermentacion:
        def __init__(self):
            # Estos datos no pueden ser modificables
            self.temperatura = 25
            self.litros_maximos = 300000
            self.numero_tanques = 3
            self.randomize_proceso_fermentacion()  # Llama al método para inicializar las demás variables

        def randomize_proceso_fermentacion(self):
            # Datos aleatorios que se pueden modificar con un botón
            self.tiempo_fermentado = random.randint(210000, 345600)
            Cerveceria.litros_producidos = random.randint(8000, 15000)
            self.costo_materia_prima_fermentacion = random.randint(5000, 7000)
            self.numero_empleados_fermentacion = random.randint(5, 8)
            self.pago_empleados_fermentacion = random.randint(4000, 8000)

            # Cálculo de costos basados en variables aleatorias
            self.costo_energia_total_fermentacion = Cerveceria.costo_energia_segundos * self.tiempo_fermentado
            self.pago_total_empleados_fermentacion = self.numero_empleados_fermentacion * self.pago_empleados_fermentacion

    class Embotellado:
        def __init__(self):
            self.embotealladoras = 3
            self.cont_botella = 600
            self.costo_botella_prima = 2
            self.randomize_proceso_embotellado()

        def randomize_proceso_embotellado(self):
            self.tiempo_embotellado = random.randint(210000, 345600)
            self.numero_empleados_embotellado = random.randint(5, 8)
            self.pago_empleados_embotellado = random.randint(4000, 8000)
            self.costo_energia_total_embotellado = Cerveceria.costo_energia_segundos * self.tiempo_embotellado
            self.pago_total_empleados_embotellado = self.numero_empleados_embotellado * self.pago_empleados_embotellado
            self.botellas_total_producidas = Cerveceria.litros_producidos / self.cont_botella
            self.costo_total_botellas = self.botellas_total_producidas * self.costo_botella_prima

    class Empaquetado:
        def __init__(self):
            self.empaquetadoras = 3  # Se utilizará en pygame
            self.capacidad_six = 6
            self.costo_por_caja = 2

        def proceso(self, botellas_total_producidas):
            tiempo_empaquetado = random.randint(210000, 345600)
            numero_empleados_empaquetado = random.randint(5, 8)
            pago_empleados_empaquetado = random.randint(4000, 8000)

            costo_energia_total_empaquetado = Cerveceria.costo_energia_segundos * tiempo_empaquetado
            pago_total_empleados_empaquetado = numero_empleados_empaquetado * pago_empleados_empaquetado
            cajas_total_producidas = botellas_total_producidas / self.capacidad_six
            costo_total_por_caja = cajas_total_producidas * self.costo_por_caja

            return cajas_total_producidas, costo_energia_total_empaquetado, pago_total_empleados_empaquetado

    class Distribucion:
        def __init__(self):
            self.capacidad_maxima_camion = 20
            self.numero_empleados_distribucion = 2

        def proceso(self, cajas_total_producidas):
            tiempo_distribucion = random.randint(210000, 345600)
            pago_empleados_distribucion = random.randint(4000, 8000)
            costo_gas_por_camion = random.randint(800, 1000)

            numero_de_camiones = round(cajas_total_producidas / self.capacidad_maxima_camion)
            costo_gas_total_distribucion = costo_gas_por_camion * numero_de_camiones
            pago_total_empleados_distribucion = self.numero_empleados_distribucion * pago_empleados_distribucion

            return tiempo_distribucion, costo_gas_total_distribucion, pago_total_empleados_distribucion








class Aplicacion:
    def __init__(self, root):
        self.root = root
        self.cerveceria = Cerveceria()
        self.current_stage = 'fermentacion'  # Inicializar la etapa actual
        
        # Crear el control de pestañas
        self.tabControl = ttk.Notebook(root)
        
        # Crear las pestañas
        self.fermentacion_tab = ttk.Frame(self.tabControl)
        self.embotellado_tab = ttk.Frame(self.tabControl)
        self.empaquetado_tab = ttk.Frame(self.tabControl)
        self.distribucion_tab = ttk.Frame(self.tabControl)
        
        # Configuración inicial de las pestañas
        self.fermentacion_tab = ttk.Frame(self.tabControl)
        self.embotellado_tab = ttk.Frame(self.tabControl)
        self.empaquetado_tab = ttk.Frame(self.tabControl)
        self.distribucion_tab = ttk.Frame(self.tabControl)
        self.tabControl.add(self.fermentacion_tab, text='Fermentación')
        self.tabControl.add(self.embotellado_tab, text='Embotellado')
        self.tabControl.add(self.empaquetado_tab, text='Empaquetado')
        self.tabControl.add(self.distribucion_tab, text='Distribución')
        self.tabControl.pack(side=tk.LEFT, fill="both", expand=True)

        # Añadir widget de texto para los resultados
        self.result_text = tk.Text(root, height=10, width=50)
        self.result_text.pack(side=tk.RIGHT, fill="both", expand=True)

        # Inicializar contenido de cada pestaña
        self.init_fermentacion_tab()
        self.init_embotellado_tab()
        self.init_empaquetado_tab()
        self.init_distribucion_tab()

        # Configuración inicial de pestañas
        self.tabControl.tab(1, state='disabled')  # Embotellado
        self.tabControl.tab(2, state='disabled')  # Empaquetado
        self.tabControl.tab(3, state='disabled')  # Distribución
        
        #Simulation button
        self.run_button = tk.Button(root, text="Simulación", command=self.next_stage)
        self.run_button.pack()

    def next_stage(self):
        self.run_simulation(self.current_stage)
        # Actualizar el estado para la próxima etapa
        if self.current_stage == 'fermentacion':
            self.current_stage = 'embotellado'
        elif self.current_stage == 'embotellado':
            self.current_stage = 'empaquetado'
        elif self.current_stage == 'empaquetado':
            self.current_stage = 'distribucion'

    def init_fermentacion_tab(self):
        #We must create an instance of itself
        fermentacion = self.cerveceria.Fermentacion()

        #Static Variables
        ttk.Label(self.fermentacion_tab, text="-VARIABLES FIJAS:").pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        ttk.Label(self.fermentacion_tab, text="Temperatura (°C):").pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
        ttk.Label(self.fermentacion_tab, text=str(fermentacion.temperatura)).pack(side=tk.TOP, fill=tk.X, padx=20)

        ttk.Label(self.fermentacion_tab, text="Litros máximos:").pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
        ttk.Label(self.fermentacion_tab, text=str(fermentacion.litros_maximos)).pack(side=tk.TOP, fill=tk.X, padx=20)

        ttk.Label(self.fermentacion_tab, text="Número de tanques:").pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
        ttk.Label(self.fermentacion_tab, text=str(fermentacion.numero_tanques)).pack(side=tk.TOP, fill=tk.X, padx=20)

        ttk.Label(self.fermentacion_tab, text="").pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        ttk.Label(self.fermentacion_tab, text="-VARIABLES ALEATORIAS:").pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)


        #Random variables
        randomizable_vars_fermentacion = [
            ("Tiempo fermentado (210000 - 345600 seg)", "tiempo_fermentado"),
            ("Litros producidos (8000 - 15000)", "litros_producidos"),
            ("Costo materia prima (5000 - 7000 MXN)", "costo_materia_prima_fermentacion"),
            ("Número de empleados (5 - 8)", "numero_empleados_fermentacion"),
            ("Pago a empleados (4000 - 8000 MXN)", "pago_empleados_fermentacion")
        ]

        #Ranges dictionary for randomize and correct input
        ranges_fermentacion = {
            "tiempo_fermentado": (210000, 345600),
            "litros_producidos": (8000, 15000),
            "costo_materia_prima_fermentacion": (5000, 7000),
            "numero_empleados_fermentacion": (5, 8),
            "pago_empleados_fermentacion": (4000, 8000)
        }

        #Validates if input is inside the range (ranges dictionary).
        def validate_input(P, attr_name):
            if re.match("^[0-9]*$", P):  #This pretty much means ONLY NUMBERS.
                if P == "":  #This allows 'empty' entries, like inputing nothing.
                    return True
                value = int(P)
                min_val, max_val = ranges_fermentacion[attr_name]
                return min_val <= value <= max_val
            return False

        for label_text, attr_name in randomizable_vars_fermentacion:
            frame = ttk.Frame(self.fermentacion_tab)
            frame.pack(fill=tk.X, pady=5)
            ttk.Label(frame, text=label_text).pack(side=tk.LEFT, padx=10)

            if attr_name == "litros_producidos":
                var = tk.StringVar(value=str(self.cerveceria.litros_producidos))
            else:
                var = tk.StringVar(value=getattr(fermentacion, attr_name))

            vcmd = (self.root.register(lambda P, attr_name=attr_name: validate_input(P, attr_name)), '%P')
            entry = ttk.Entry(frame, textvariable=var, validate='key', validatecommand=vcmd)
            entry.pack(side=tk.LEFT, padx=10)

            def randomize(var, attr_name):
                # Obtener el rango adecuado desde el diccionario
                range_min, range_max = ranges_fermentacion[attr_name]
                # Generar nuevo valor aleatorio dentro del rango específico
                new_value = random.randint(range_min, range_max)
                if attr_name == "litros_producidos":
                    setattr(self.cerveceria, attr_name, new_value)
                else:
                    setattr(fermentacion, attr_name, new_value)
                var.set(new_value)

            # Botón que vincula el método randomize con los argumentos específicos
            ttk.Button(frame, text="Randomize", command=lambda var=var, attr_name=attr_name: randomize(var, attr_name)).pack(side=tk.LEFT, padx=10)


    def init_embotellado_tab(self):
        embotellado = self.cerveceria.Embotellado()

        #Static Variables
        ttk.Label(self.embotellado_tab, text="-VARIABLES FIJAS:").pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        ttk.Label(self.embotellado_tab, text="Número de Embotelladoras:").pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
        ttk.Label(self.embotellado_tab, text=str(embotellado.embotealladoras)).pack(side=tk.TOP, fill=tk.X, padx=20)

        ttk.Label(self.embotellado_tab, text="Mililitros máximos por botella:").pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
        ttk.Label(self.embotellado_tab, text=str(embotellado.cont_botella)).pack(side=tk.TOP, fill=tk.X, padx=20)

        ttk.Label(self.embotellado_tab, text="Costo de cada botella vacía:").pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
        ttk.Label(self.embotellado_tab, text=str(embotellado.costo_botella_prima)).pack(side=tk.TOP, fill=tk.X, padx=20)

        ttk.Label(self.embotellado_tab, text="").pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        #Random Variables

        ttk.Label(self.embotellado_tab, text="-VARIABLES ALEATORIAS:").pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        randomizable_vars_embotellado = [
            ("Tiempo embotellado (210000 - 345600 seg)", "tiempo_embotellado"),
            ("Número de empleados (5 - 8)", "numero_empleados_embotellado"),
            ("Pago a empleados (4000 - 8000 MXN)", "pago_empleados_embotellado")
        ]

        #Ranges dictionary
        ranges_embotellado = {
            "tiempo_embotellado": (210000, 345600),
            "numero_empleados_embotellado": (5, 8),
            "pago_empleados_embotellado": (4000, 8000)
        }

        #Validates if input is inside the range (ranges dictionary).
        def validate_input(P, attr_name):
            if re.match("^[0-9]*$", P):  #This pretty much means ONLY NUMBERS.
                if P == "":  #This allows 'empty' entries, like inputing nothing.
                    return True
                value = int(P)
                min_val, max_val = ranges_embotellado[attr_name]
                return min_val <= value <= max_val
            return False

        for label_text, attr_name in randomizable_vars_embotellado:
            frame = ttk.Frame(self.embotellado_tab)
            frame.pack(fill=tk.X, pady=5)
            ttk.Label(frame, text=label_text).pack(side=tk.LEFT, padx=10)

            var = tk.StringVar(value=getattr(embotellado, attr_name))
            vcmd = (self.root.register(lambda P, attr_name=attr_name: validate_input(P, attr_name)), '%P')
            entry = ttk.Entry(frame, textvariable=var, validate='key', validatecommand=vcmd)
            entry.pack(side=tk.LEFT, padx=10)

            def randomize(var, attr_name):
                # Obtener el rango adecuado desde el diccionario
                range_min, range_max = ranges_embotellado[attr_name]
                # Generar nuevo valor aleatorio dentro del rango específico
                new_value = random.randint(range_min, range_max)
                setattr(embotellado, attr_name, new_value)
                var.set(new_value)

            # Botón que vincula el método randomize con los argumentos específicos
            ttk.Button(frame, text="Randomize", command=lambda var=var, attr_name=attr_name: randomize(var, attr_name)).pack(side=tk.LEFT, padx=10)

    def init_empaquetado_tab(self):
        # Adaptado a empaquetado
        pass

    def init_distribucion_tab(self):
        # Adaptado a distribución
        pass

    def run_simulation(self, completed_stage):
        if completed_stage == 'fermentacion':
            fermentacion = self.cerveceria.Fermentacion()
            costo_energia = fermentacion.costo_energia_total_fermentacion
            pago_empleados = fermentacion.pago_total_empleados_fermentacion
            self.result_text.delete('1.0', tk.END)
            result_message = f"Resultados de Fermentación:\nCosto Energía: {costo_energia:.2f}\nPago Empleados: {pago_empleados:.2f}"
            self.result_text.insert(tk.END, result_message)
            self.tabControl.tab(1, state='normal')
        elif completed_stage == 'embotellado':
            embotellado = self.cerveceria.Embotellado()
            # No se necesita pasar argumentos aquí
            embotellado.randomize_proceso_embotellado()
            botellas_producidas = embotellado.botellas_total_producidas
            costo_energia = embotellado.costo_energia_total_embotellado
            pago_empleados = embotellado.pago_total_empleados_embotellado
            self.result_text.delete('1.0', tk.END)
            result_message = f"Resultados de Embotellado:\nBotellas Producidas: {botellas_producidas:.0f}\nCosto Energía: {costo_energia:.2f}\nPago Empleados: {pago_empleados:.2f}"
            self.result_text.insert(tk.END, result_message)
            self.tabControl.tab(2, state='normal')  # Habilitar Empaquetado



# Configuración inicial de la ventana
root = tk.Tk()
root.title("Cerveza2")
app = Aplicacion(root)
root.mainloop()