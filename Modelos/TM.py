import os
import yaml
from graphviz import Digraph

class TM:
    def __init__(self, estados, alfabeto, alfabetoEntrada, q0, aceptacion, rechazo, transiciones, cinta, posCabezal):
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

    @classmethod
    def from_yaml(cls, file_path):
        with open(file_path, 'r') as file:
            config = yaml.safe_load(file)
        
        estados = config['q_states']['states']
        alfabeto = config['alphabet']
        alfabeto_entrada = config['tape_alphabet']
        q0 = config['q_states']['initial_state']
        aceptacion = config['q_states']['final_states']
        rechazo = config['q_states']['reject_state']
        transiciones = {}

        for rule in config['delta']:
            estado_actual = rule['params']['initial_state']
            simbolo_leido = rule['params']['tape_input']
            estado_siguiente = rule['output']['final_state']
            simbolo_escrito = rule['output']['tape_output']
            movimiento = rule['output']['move']
            
            if estado_actual not in transiciones:
                transiciones[estado_actual] = {}
            transiciones[estado_actual][simbolo_leido] = [estado_siguiente, simbolo_escrito, movimiento]
        
        cinta = ['B'] * 100
        posCabezal = 0
        
        return cls(estados, alfabeto, alfabeto_entrada, q0, aceptacion, rechazo, transiciones, cinta, posCabezal)

    def imprimir_tabla_transiciones(self):
        print("Tabla de transiciones:")
        print(f"{'Estado':<10}{'Símbolo':<10}{'Siguiente Estado':<20}{'Símbolo Escrito':<20}{'Dirección'}")
        print("-" * 70)
        for estado in sorted(self.transiciones.keys()):
            for simbolo in sorted(self.transiciones[estado].keys()):
                siguiente_estado, simbolo_escrito, direccion = self.transiciones[estado][simbolo]
                print(f"{estado:<10}{simbolo:<10}{siguiente_estado:<20}{simbolo_escrito:<20}{direccion}")

    def simulate(self, cadena):
        self.historial = []
        estado_actual = self.q0
        self.cinta = list(cadena) + ['B'] * (100 - len(cadena))
        self.posCabezal = 0

        while True:
            simbolo_actual = self.cinta[self.posCabezal]

            # Formato del estado actual en el historial
            cinta_formateada = (
                ''.join(self.cinta[:self.posCabezal]) +
                f"[{estado_actual}, {simbolo_actual}]" +
                ''.join(self.cinta[self.posCabezal + 1:])
            )
            self.historial.append(f"|- {cinta_formateada}")

            # Verificar si el estado es de aceptación
            if estado_actual in self.aceptacion:
                self.historial.append(f"|- Máquina acepta la cadena.")
                break

            # Verificar si el estado es de rechazo
            if estado_actual == self.rechazo:
                self.historial.append(f"|- Máquina rechaza la cadena.")
                break

            # Buscar transición en la tabla
            if estado_actual in self.transiciones and simbolo_actual in self.transiciones[estado_actual]:
                siguiente_estado, simbolo_escrito, direccion = self.transiciones[estado_actual][simbolo_actual]
            else:
                # Si no se encuentra transición válida
                self.historial.append(f"|- [{estado_actual}] - No se encontró transición para el símbolo '{simbolo_actual}'.")
                estado_actual = self.rechazo
                break

            # Actualizar la cinta y el estado
            self.cinta[self.posCabezal] = simbolo_escrito
            estado_actual = siguiente_estado

            # Mover el cabezal
            if direccion == 'R':
                self.posCabezal += 1
            elif direccion == 'L':
                self.posCabezal -= 1

            # Verificar límites de la cinta
            if self.posCabezal < 0 or self.posCabezal >= len(self.cinta):
                self.historial.append(f"|- Error: Cabezal intentó salir de la cinta.")
                estado_actual = self.rechazo
                break

        return self.historial

    def writeInTXT(self):
        with open('historial.txt', 'w') as f:
            for paso in self.historial:
                f.write(paso + '\n')

    def graph(self):
        dot = Digraph(format='png', engine='dot')

        # Agregar nodos
        for estado in self.estados:
            if estado in self.aceptacion:
                dot.node(estado, shape='doublecircle', style='filled', color='lightgreen')
            elif estado == self.rechazo:
                dot.node(estado, shape='doublecircle', style='filled', color='red')
            else:
                dot.node(estado)

        # Agregar aristas
        for estado in self.transiciones:
            for simbolo in self.transiciones[estado]:
                siguiente_estado, simbolo_escrito, direccion = self.transiciones[estado][simbolo]
                label = f'{simbolo} / {simbolo_escrito}, {direccion}'
                dot.edge(estado, siguiente_estado, label=label)

        # Guardar y renderizar
        if not os.path.exists('graphs'):
            os.makedirs('graphs')
        file_path = 'graphs/maquina_turing'
        dot.render(file_path, view=True, cleanup=True)
        print(f"Grafo de la máquina de Turing generado y guardado en {file_path}.png")

def simulate_alteradora(cadenas_a_simular):
    file_path = "alternadora.yml"
    maquina = TM.from_yaml(file_path)

    maquina.imprimir_tabla_transiciones()
    print("\nSimulaciones de cadenas desde 'alternadora.yml':")

    for cadena in cadenas_a_simular:
        print(f"\nSimulación de la cadena '{cadena}':")

        # Simular la cadena directamente (sin invertirla)
        historial = maquina.simulate(cadena)
        for paso in historial:
            print(paso)

if __name__ == "__main__":
    # Ejecutar la máquina reconocedora
    print("Ejecutando máquina reconocedora:")
    file_path = "test.yml"
    maquina_reconocedora = TM.from_yaml(file_path)

    # Leer las cadenas desde el YAML de la reconocedora
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
        cadenas_a_simular = config.get('simulation_strings', [])

    maquina_reconocedora.imprimir_tabla_transiciones()

    print("\nSimulaciones de cadenas desde 'test.yml':")
    for cadena in cadenas_a_simular:
        print(f"\nSimulación de la cadena '{cadena}':")
        historial = maquina_reconocedora.simulate(cadena)
        for paso in historial:
            print(paso)
    maquina_reconocedora.graph()

    # Ejecutar la máquina alteradora con las cadenas de la reconocedora
    print("\nEjecutando máquina alteradora:")
    simulate_alteradora(cadenas_a_simular)
