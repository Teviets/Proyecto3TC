import os
from graphviz import Digraph

class TM:

    """
        Constructor de la clase TM determinista
        @param estados: lista de estados --> list
        @param alfabeto: lista de simbolos del alfabeto  --> list
        @param alfabetoEntrada: lista de simbolos del alfabeto de entrada --> list
        @param q0: estado inicial --> str
        @param aceptacion: estado de aceptacion  --> str
        @param rechazo: estado de rechazo --> str
        @param transiciones: lista de transiciones --> list
        @param cinta: cinta de la maquina --> list
        @param posCabezal: posicion del cabezal en la cinta --> int

        parametros esperados:
        estados = ['q0', 'q1', 'q2', 'q3', 'q4']
        alfabeto = ['0', '1']
        alfabetoEntrada = ['0', '1']
        q0 = 'q0'
        aceptacion = 'q4'
        rechazo = 'q3'
        transiciones = {
            'q0': {
                '0': ['q1', '0', 'R'], 
                '1': ['q3', '1', 'R']
                },
            'q1': {
                '0': ['q1', '0', 'R'], 
                '1': ['q2', '1', 'R']
            }, 
            'q2': {
                '0': ['q2', '0', 'R'], 
                '1': ['q2', '1', 'R'], 
                'B': ['q4', 'B', 'R']
            }
        cinta = ['0', '1', '0', '1', 'B', 'B', 'B', 'B']
        posCabezal = 0
    """
    def __init__ (self, estados, alfabeto, alfabetoEntrada, q0, aceptacion, rechazo, transiciones, cinta, posCabezal):
        self.estados = estados
        self.alfabeto = alfabeto
        self.alfabetoEntrada = alfabetoEntrada
        self.q0 = q0
        self.aceptacion = aceptacion
        self.rechazo = rechazo
        self.transiciones = transiciones
        self.cinta = cinta
        self.posCabezal = posCabezal

        self.historial = []

    def imprimir_tabla_transiciones(self):
            print(f"{'Estado':<10}{'Símbolo':<10}{'Siguiente Estado':<20}{'Símbolo Escrito':<20}{'Dirección'}")
            print("-" * 70)
            
            for estado in self.transiciones:
                for simbolo in self.transiciones[estado]:
                    siguiente_estado, simbolo_escrito, direccion = self.transiciones[estado][simbolo]
                    print(f"{estado:<10}{simbolo:<10}{siguiente_estado:<20}{simbolo_escrito:<20}{direccion}")

    def simulate(self, cadena):
        estado_actual = self.q0
        self.cinta = list(cadena) + ['B'] * (len(self.cinta) - len(cadena))
        self.posCabezal = 0

        while estado_actual != self.aceptacion and estado_actual != self.rechazo:
            simbolo_actual = self.cinta[self.posCabezal]
            
            # Mostrar cinta completa con el estado y el símbolo en la posición del cabezal
            cinta_formateada = (
                ''.join(self.cinta[:self.posCabezal]) +
                f"[{estado_actual}, {simbolo_actual}]" +
                ''.join(self.cinta[self.posCabezal + 1:])
            )
            self.historial.append(f"|- {cinta_formateada}")
            
            # Si no hay transición, asumir estado de rechazo
            if simbolo_actual not in self.transiciones.get(estado_actual, {}):
                estado_actual = self.rechazo
                self.historial.append(f"|- [{estado_actual}] - Sin transición")
                break

            siguiente_estado, simbolo_escrito, direccion = self.transiciones[estado_actual][simbolo_actual]
            
            # Actualizar la cinta, el estado y el cabezal
            self.cinta[self.posCabezal] = simbolo_escrito
            estado_actual = siguiente_estado
            self.posCabezal += 1 if direccion == 'R' else -1

            # Asegurar que el cabezal no se salga de la cinta
            if self.posCabezal < 0:
                self.posCabezal = 0
            elif self.posCabezal >= len(self.cinta):
                self.cinta.append('B')

        # Agregar la configuración final al historial
        simbolo_actual = self.cinta[self.posCabezal]
        cinta_formateada = (
            ''.join(self.cinta[:self.posCabezal]) +
            f"[{estado_actual}, {simbolo_actual}]" +
            ''.join(self.cinta[self.posCabezal + 1:])
        )
        self.historial.append(f"|- {cinta_formateada}")
        
        return self.historial
    
    def writeInTXT(self):
        with open('historial.txt', 'w') as f:
            for paso in self.historial:
                f.write(paso + '\n')


    def graph(self):
        dot = Digraph(format='png', engine='dot')

        for estado in self.estados:
            if estado == self.aceptacion:
                dot.node(estado, shape='doublecircle', style='filled', color='lightgreen') 
            elif estado == self.rechazo:
                dot.node(estado, shape='doublecircle', style='filled', color='red') 
            else:
                dot.node(estado) 

        for estado in self.transiciones:
            for simbolo in self.transiciones[estado]:
                siguiente_estado, simbolo_escrito, direccion = self.transiciones[estado][simbolo]
                label = f'{simbolo} / {simbolo_escrito}, {direccion}'
                dot.edge(estado, siguiente_estado, label=label)

        if not os.path.exists('graphs'):
            os.makedirs('graphs')

        file_path = 'graphs/maquina_turing.png'
        dot.render(file_path, view=True)
        print(f"Grafo de la máquina de Turing generado y guardado en {file_path}.")


    
"""

EJEMPLO DE USO

# Definición de los parámetros
estados = ['q0', 'q1', 'q2', 'q3', 'q4']
alfabeto = ['0', '1']
alfabetoEntrada = ['0', '1']
q0 = 'q0'
aceptacion = 'q4'
rechazo = 'q3'
transiciones = {
    'q0': {
        '0': ['q1', '0', 'R'], 
        '1': ['q3', '1', 'R']
    },
    'q1': {
        '0': ['q1', '0', 'R'], 
        '1': ['q2', '1', 'R']
    },
    'q2': {
        '0': ['q2', '0', 'R'], 
        '1': ['q2', '1', 'R'], 
        'B': ['q4', 'B', 'R']
    }
}
cinta = ['0', '1', '0', '1', 'B', 'B', 'B', 'B']
posCabezal = 0

# Crear instancia de la clase TM
maquina = TM(estados, alfabeto, alfabetoEntrada, q0, aceptacion, rechazo, transiciones, cinta, posCabezal)

# Llamar al método para imprimir la tabla de transiciones
maquina.imprimir_tabla_transiciones()

# Llamar al método para generar el grafo
maquina.graph()

# Ejecutar la simulación y obtener el historial de pasos
historial = maquina.simulate("0101")

# Imprimir el historial de pasos
for paso in historial:
    print(paso)

maquina.writeInTXT()
"""