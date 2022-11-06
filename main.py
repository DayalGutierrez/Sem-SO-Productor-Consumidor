from pynput import keyboard as kb
from rich import print
from rich.layout import Layout
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from random import randint as ran
from time import sleep
from random import randint as ran

estado_productor = "Esperando"
estado_consumidor = "Esperando"
indice_productor = 0
indice_consumidor = 0
buffer = list()

for i in range(25):
    buffer.append("-")

escape = 0
def pulsa(tecla):
    global escape
    if tecla == kb.Key.esc:
        escape = 1
        

escuchador = kb.Listener(pulsa)
escuchador.start()

def make_layout() -> Layout:
    """Define el layout."""
    layout = Layout(name="root")

    layout.split(
        Layout(name="arriba", size=6),
        Layout(name="abajo", size=6)
    )

    return layout

def tabla_productos() -> Table:
    table = Table(title="Productos")
    for i in range(1,26):
        table.add_column(str(i), justify="left", style="bold blue")

    table.add_row(buffer[0],buffer[1],buffer[2],buffer[3],buffer[4],buffer[5],buffer[6],buffer[7],buffer[8],buffer[9],buffer[10],buffer[11],
    buffer[12],buffer[13],buffer[14],buffer[15],buffer[16],buffer[17],buffer[18],buffer[19],buffer[20],buffer[21],buffer[22],
    buffer[23],buffer[24])
    
    return table

def tabla_estados() -> Table:
    table = Table(title="Estados")
    table.add_column("Productor", justify="left", style="bold blue")
    table.add_column("Consumidor", justify="left", style="bold blue")

    table.add_row(estado_productor, estado_consumidor)
    
    return table
    
layout = make_layout()
layout["arriba"].update(tabla_productos())
layout["abajo"].update(tabla_estados())

with Live(layout, refresh_per_second=30) as live:
    while escape == 0:
        sorteo = ran(1,2)
        n_productos = ran(2,5)

        if sorteo == 1: #Sección del productor
            if buffer[indice_productor] == "🍔":
                estado_productor = "N/A producir"
            else:
                estado_productor = "Produciendo"
            layout["abajo"].update(tabla_estados())
            for i in range(n_productos):
                if buffer[indice_productor] != "🍔":
                    buffer[indice_productor] = "🍔"
                else:
                    break
                layout["arriba"].update(tabla_productos())
                sleep(0.5)
                indice_productor += 1
                if indice_productor > 24:
                    indice_productor = 0
            sleep(1)
            estado_productor = "Esperando"
            layout["abajo"].update(tabla_estados())

        else: #Seccion del consumidor
            if buffer[indice_consumidor] == "-":
                estado_consumidor = "N/A consumo"
            else:
                estado_consumidor = "Consumiendo"
            layout["abajo"].update(tabla_estados())
            for i in range(n_productos):
                if buffer[indice_consumidor] == "🍔":
                    buffer[indice_consumidor] = "-"
                else:
                    break
                layout["arriba"].update(tabla_productos())
                sleep(0.5)
                indice_consumidor += 1
                if indice_consumidor > 24:
                    indice_consumidor = 0
            sleep(1)

            estado_consumidor = "Esperando"
            layout["abajo"].update(tabla_estados())
            