import random
from datetime import datetime
import pandas as pd
from matplotlib import pyplot as plt


class Jugador:
    def __init__(self, nombre, edad):
        self.__nombre = nombre
        self.__edad = edad

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, nombre):
        self.__nombre = nombre

    @property
    def edad(self):
        return self.__edad

    @edad.setter
    def edad(self, edad):
        self.__edad = edad

    def __str__(self):
        cadena = f"Jugador: {self.__nombre}, Edad {self.__edad}"
        return cadena


class JugadorEventos:
    def __init__(self):
        self.__posicion = 1
        self.__pierdeTurno = False
        self.__vivo = True

    @property
    def posicion(self):
        return self.__posicion

    @posicion.setter
    def posicion(self, posicion):
        if posicion < 1:
            self.__posicion = 1
        elif posicion > 30:
            self.__posicion = 30
        else:
            self.__posicion = posicion

    @property
    def pierdeTurno(self):
        return self.__pierdeTurno

    @pierdeTurno.setter
    def pierdeTurno(self, pierdeTurno):
        self.__pierdeTurno = bool(pierdeTurno)

    @property
    def vivo(self):
        return self.__vivo

    @vivo.setter
    def vivo(self, vivo):
        self.__vivo = bool(vivo)

    def mover(self, nuevaPosicion):
        self.posicion = nuevaPosicion

    def perderTurno(self):
        self.pierdeTurno = True

    def muere(self):
        self.vivo = False


class Instrucciones:
    def mostrarReglas(self):
        print(
            "\nInstrucciones del juego: \n"
            "Para jugar necesitaras lanzar un dado de 6 numeros aleatorios\n"
            "El tablero tiene 30 casillas y en algunas de ellas ocurren\n"
            "eventos que te haran retroceder 2 casillas, perder un turno, \n"
            "avanzar 4 casillas, perder al instante o retroceder al inicio\n"
            "Tu objetivo es llegar a la casilla 30 con vida\n"
        )


class RegistroPartida:
    archivoCSV = "registroPartidas.csv"

    def __init__(self, jugador):
        self.__jugador = jugador
        self.__listaPartidas = []
        self.__resultado = ""

    def finalizar(self, resultado):
        self.__resultado = resultado

        partida = {
            "jugador": self.__jugador.nombre,
            "edad": self.__jugador.edad,
            "resultado": self.__resultado,
            "fecha": datetime.now(),
        }

        self.__listaPartidas.append(partida)
        self.guardar()

    def guardar(self):
        df = pd.DataFrame(self.__listaPartidas)
        try:
            pd.read_csv(self.archivoCSV, sep=";")
            cabez = False
        except FileNotFoundError:
            cabez = True
        df.to_csv(
            self.archivoCSV,
            mode="a",
            index=False,
            header=cabez,
            sep=";",
        )


class Estadisticas:
    archivoCSV = "registroPartidas.csv"

    def __init__(self):
        self.__datos = None

    def cargar(self):
        self.__datos = pd.read_csv(self.archivoCSV, sep=";")
        return True

    def mostrarGraficos(self):
        if self.cargar() is False:
            return

        self.__datos["resultado"].value_counts().plot(
            kind="pie",
            autopct="%0.1f%%",
        )
        plt.title("Porcentaje de victorias, derrotas y abandonos")
        plt.show()

        self.__datos["edad"].value_counts().sort_index().plot(kind="bar")
        plt.title("Partidas jugadas por edad")
        plt.show()

        victorias = self.__datos[self.__datos["resultado"] == "Victoria"]
        if len(victorias) > 0:
            victorias["jugador"].value_counts().plot(kind="bar")
            plt.title("Ranking de victorias por jugador")
            plt.ylabel("Cantidad de victorias")
            plt.show()
        else:
            print("No existen victorias registradas")


class Evento:
    def __init__(self):
        self.__descripcion = ""

    @property
    def descripcion(self):
        return self.__descripcion

    @descripcion.setter
    def descripcion(self, descripcion):
        self.__descripcion = descripcion

    def aplicarEvento(self, jugador):
        posicion = jugador.posicion
        self.__descripcion = ""

        if posicion >= 5 and posicion <= 10:
            jugador.mover(jugador.posicion - 2)
            self.__descripcion = (
                f"Caiste en una trampa de arena: retrocedes 2 casillas\n"
                f"Ahora estas en la casilla {jugador.posicion}"
            )

        elif posicion >= 11 and posicion <= 18:
            jugador.perderTurno()
            self.__descripcion = (
                "Te cayo un cañonazo: pierdes un turno\n"
                f"Sigues en la casilla {jugador.posicion}"
            )

        elif posicion >= 19 and posicion <= 24:
            jugador.mover(jugador.posicion + 4)
            if jugador.posicion > 30:
                jugador.mover(30)
            self.__descripcion = (
                f"Encontraste un cofre de oro: avanzas 4 casillas\n"
                f"Ahora estas en la casilla {jugador.posicion}"
            )

        elif posicion >= 25 and posicion <= 29:
            tiro = random.randint(1, 6)
            print(f"El numero de dado para enfrentarte al Kraken es: {tiro}")
            if tiro % 2 == 1:
                jugador.muere()
                self.__descripcion = (
                    "Te enfrentas al Kraken y tu dado muestra impar. Muerto"
                )
            else:
                jugador.mover(1)
                self.__descripcion = (
                    "Te enfrentas al Kraken y tu dado muestra un par: "
                    "Retrocedes al inicio\n"
                    f"Ahora estas en la casilla {jugador.posicion}"
                )


class Tablero:
    def __init__(self):
        self.__tamaño = 30
        self.__evento = Evento()

    @property
    def tamaño(self):
        return self.__tamaño

    @tamaño.setter
    def tamaño(self, tamaño):
        self.__tamaño = tamaño

    @property
    def evento(self):
        return self.__evento

    @evento.setter
    def evento(self, evento):
        self.__evento = evento

    def aplicarEvento(self, jugador):
        self.__evento.aplicarEvento(jugador)
        if self.__evento.descripcion:
            print(self.__evento.descripcion)
        return self.__evento.descripcion

    def __str__(self):
        cadena = f"Tablero de {self.__tamaño} casillas"
        return cadena


class Juego:
    def __init__(self, jugador, estado):
        self.__tablero = Tablero()
        self.__jugador = jugador
        self.__estado = estado
        self.__enCurso = True
        self.__registro = RegistroPartida(jugador)
        self.__dado = 0

    @property
    def tablero(self):
        return self.__tablero

    @tablero.setter
    def tablero(self, tablero):
        self.__tablero = tablero

    @property
    def jugador(self):
        return self.__jugador

    @jugador.setter
    def jugador(self, jugador):
        self.__jugador = jugador

    @property
    def estado(self):
        return self.__estado

    @estado.setter
    def estado(self, estado):
        self.__estado = estado

    @property
    def enCurso(self):
        return self.__enCurso

    @enCurso.setter
    def enCurso(self, enCurso):
        self.__enCurso = bool(enCurso)

    @property
    def registro(self):
        return self.__registro

    @registro.setter
    def registro(self, registro):
        self.__registro = registro

    @property
    def dado(self):
        return self.__dado

    @dado.setter
    def dado(self, dado):
        self.__dado = dado

    def lanzarDado(self):
        self.__dado = random.randint(1, 6)
        dadoLanzado = self.__dado
        return dadoLanzado

    def turno(self):
        if self.__estado.vivo is False:
            print("El jugador ha sido derrotado por el Kraken")
            self.__enCurso = False
            self.__registro.finalizar("Derrota")
            return

        if self.__estado.pierdeTurno:
            print("Te salteas un turno por el cañonazo")
            self.__estado.pierdeTurno = False
            return

        input("Presiona enter para lanzar tu dado")
        dado = self.lanzarDado()
        print(f"El dado muestra el numero: {dado}")

        nuevaPosicion = self.__estado.posicion + dado
        self.__estado.mover(nuevaPosicion)

        print(f"Avanzas a la casilla {self.__estado.posicion}")
        self.__tablero.aplicarEvento(self.__estado)

        if self.__estado.vivo is False:
            print("Perdiste")
            self.__enCurso = False
            self.__registro.finalizar("Derrota")
            return

        if self.__estado.posicion >= 30:
            print("Llegaste al tesoro pirata, ganaste el juego")
            self.__enCurso = False
            self.__registro.finalizar("Victoria")
            return

        respuesta = input("Quieres abandonar el juego? s(Si), n(No) ").lower()
        if respuesta == "s":
            print("Abandonaste la partida")
            self.__enCurso = False
            self.__registro.finalizar("Abandono")
        else:
            print("Continuas en la partida")

    def jugar(self):
        print("Comienza el juego")
        while self.__enCurso:
            self.turno()


def menu():
    print("\nJuego del Tesoro Pirata:")
    print("1. Ver instrucciones")
    print("2. Jugar")
    print("3. Ver estadisticas")
    print("4. Salir")
    opcion = input("Elige una opcion: ")
    return opcion


while True:
    op = menu()

    if op == "1":
        Instrucciones().mostrarReglas()
    elif op == "2":
        nombre = input("Ingresa tu nombre: ")
        try:
            edad = int(input("Ingresa tu edad: "))
            jugador = Jugador(nombre, edad)
            estado = JugadorEventos()
            juego = Juego(jugador, estado)
            juego.jugar()
        except ValueError:
            print("Ingresa un numero valido")
    elif op == "3":
        estad = Estadisticas()
        estad.mostrarGraficos()
    elif op == "4":
        break
    else:
        print("Opcion invalida")
