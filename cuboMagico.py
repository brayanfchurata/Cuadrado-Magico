import tkinter as tk
import time

class VisualizadorCuadradoMagico:
    def __init__(self, n, fila_inicio=0, columna_inicio=0):
        self.n = n
        self.suma_magica = n * (n * n + 1) // 2
        self.cuadrado = [[0 for _ in range(n)] for _ in range(n)]
        self.numeros_usados = [False] * (n * n + 1)

        # Inicializar el contador de iteraciones
        self.iteraciones = 0

        # Establecer la fila y columna de inicio
        self.fila_inicio = fila_inicio
        self.columna_inicio = columna_inicio

        # Configuración de la ventana gráfica
        self.root = tk.Tk()
        self.root.title("Generación del Cuadrado Mágico Corregido")
        self.canvas = tk.Canvas(self.root, width=400, height=400)
        self.canvas.pack()
        self.cell_size = 400 // n
        self.text_widgets = [[None for _ in range(n)] for _ in range(n)]

        # Crear la cuadrícula visual
        self.dibujar_cuadricula()

    def dibujar_cuadricula(self):
        for i in range(self.n):
            for j in range(self.n):
                x0 = j * self.cell_size
                y0 = i * self.cell_size
                x1 = x0 + self.cell_size
                y1 = y0 + self.cell_size
                self.canvas.create_rectangle(x0, y0, x1, y1, outline="black")
                self.text_widgets[i][j] = self.canvas.create_text(
                    (x0 + x1) // 2, (y0 + y1) // 2, text="", font=("Arial", 24)
                )

    def actualizar_celda(self, fila, columna, valor, color="black"):
        self.canvas.itemconfig(self.text_widgets[fila][columna], text=str(valor), fill=color)
        self.root.update()

    def borrar_celda(self, fila, columna):
        self.actualizar_celda(fila, columna, "", "red")

    def validar_completitud(self):
        # Verificar todas las filas
        for fila in self.cuadrado:
            if sum(fila) != self.suma_magica:
                return False

        # Verificar todas las columnas
        for col in range(self.n):
            if sum(self.cuadrado[fila][col] for fila in range(self.n)) != self.suma_magica:
                return False

        # Verificar diagonal principal
        diag_principal = sum(self.cuadrado[i][i] for i in range(self.n))
        if diag_principal != self.suma_magica:
            return False

        # Verificar diagonal secundaria
        diag_secundaria = sum(self.cuadrado[i][self.n - i - 1] for i in range(self.n))
        if diag_secundaria != self.suma_magica:
            return False

        return True

    def poda_rapida(self, fila, columna, num):
        # Verificar suma parcial de fila
        if sum(self.cuadrado[fila]) + num > self.suma_magica:
            return False

        # Verificar suma parcial de columna
        suma_columna = sum(self.cuadrado[i][columna] for i in range(self.n))
        if suma_columna + num > self.suma_magica:
            return False

        # Verificar diagonal principal si corresponde
        if fila == columna:
            diag_principal = sum(self.cuadrado[i][i] for i in range(self.n))
            if diag_principal + num > self.suma_magica:
                return False

        # Verificar diagonal secundaria si corresponde
        if fila + columna == self.n - 1:
            diag_secundaria = sum(self.cuadrado[i][self.n - i - 1] for i in range(self.n))
            if diag_secundaria + num > self.suma_magica:
                return False

        return True

    def resolver(self, fila, columna):
        # Caso base: si llegamos al final del tablero
        if fila == self.n:
            return self.validar_completitud()

        # Siguiente celda
        siguiente_fila = fila + (columna + 1) // self.n
        siguiente_columna = (columna + 1) % self.n

        # Intentar colocar cada número en la celda actual
        for num in range(1, self.n * self.n + 1):
            if not self.numeros_usados[num]:
                # Verificar poda rápida antes de colocar
                if not self.poda_rapida(fila, columna, num):
                    continue

                # Colocar el número y marcarlo como usado
                self.cuadrado[fila][columna] = num
                self.numeros_usados[num] = True
                self.actualizar_celda(fila, columna, num, "blue")
                self.iteraciones += 1  # Contar iteraciones

                # Continuar con el siguiente estado
                if self.resolver(siguiente_fila, siguiente_columna):
                    return True

                # Retroceso
                self.cuadrado[fila][columna] = 0
                self.numeros_usados[num] = False
                self.borrar_celda(fila, columna)

        return False

    def generar_cuadrado_magico(self):
        if self.resolver(self.fila_inicio, self.columna_inicio):
            print("¡Cuadrado mágico completado!")
            print(f"Número de iteraciones: {self.iteraciones}")
        else:
            print("No se pudo generar un cuadrado mágico.")

    def iniciar(self):
        self.generar_cuadrado_magico()
        self.root.mainloop()

n = 3
visualizador = VisualizadorCuadradoMagico(n)
visualizador.iniciar()
