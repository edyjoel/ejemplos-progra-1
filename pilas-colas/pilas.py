# Importación módulo para obtener números aleatorios
import random

# Importación módulo para escoger una opción
from random import choice

# Importación de módulo para utilizar pilas
from collections import deque

# Definir la pila
records = deque()

# Obtener la selección del usuario y computador
def selectedItems( selector, computer ):
    print('\n-> Computadora: {}'.format( computer ))
    print('-> Humano: {}'.format( selector ))

# Agregar un elemento a la pila
def addRecord(selector, computer, result) :
    records.append({
        'selector': selector,
        'computer': computer,
        'result': result
    })

# Obtener el último registro de la pila
def getLastRecord():
    if( len( records ) > 0 ):
        last_record = records.pop()
        print('\n-> El resultado anterior es:')
        selectedItems( last_record[ 'selector' ], last_record[ 'computer' ] )
        print("-> Resultado: {} \n".format( last_record[ 'result' ] ))
    else:
        print('\n-> ¡El historial está vacío!\n')

# Función del juego
def play():

    scores = 0
    
    options = ['Piedra', 'Papel', 'Tijera'] 

    computer = (choice( ( options ) ) )

    print('*********************************************')
    print ('-> PIEDRA, PAPEL O TIJERAS')
    print('-> Elige tu respuesta:\n')

    for ( count, option ) in enumerate( options ):
        print('{}) {}'.format( ( count + 1 ), option ))

    selector = input()

    # Validar que el usuario ingrese numeros
    try:
        selector = int( selector )
        if( selector > 0 and selector <= len( options )  ):
            selector = options[ ( selector - 1 ) ]
            
    except ValueError:
        print("\n-> Por favor seleccione un número, no una letra.\n")

    # Validar la selección del usuario
    if selector not in options:
        print ("-> Seleccione una opción válida")
    
    # Obtener al ganar del juego
    if selector == computer:
        scores = 0
        selectedItems( selector, computer )
        addRecord( selector, computer, 'Empate |=' )
        print("-> Resultado: Empate |= \n")

    if ( selector == 'Piedra' ):
        if ( computer == 'Papel' ):
            scores = 2
            selectedItems( selector, computer )
            addRecord( selector, computer, 'Empate |=' )
            print("-> Resultado: Gana Computadora! )= \n")
        elif ( computer == 'Tijera' ):
            scores = 1
            selectedItems( selector, computer )
            addRecord( selector, computer, 'Gana Humano! (=' )
            print("-> Resultado: Gana Humano! (= \n")

    if ( selector == 'Papel' ):
        if ( computer == 'Tijera' ):
            scores = 2
            selectedItems( selector, computer )
            addRecord( selector, computer, 'Gana Computadora! )=' )
            print("-> Resultado: Gana Computadora! )= \n")
            
        elif ( computer == 'Piedra' ):
            scores = 1
            selectedItems( selector, computer )
            addRecord( selector, computer, 'Gana Humano! (=' )
            print("-> Resultado: Gana Humano! (= \n")

    if ( selector == 'Tijera' ):
        if ( computer == 'Piedra' ):
            scores = 2
            selectedItems( selector, computer )
            addRecord( selector, computer, 'Gana Computadora! )=' )
            print("-> Resultado: Gana Computadora! )= \n")
        elif ( computer == 'Papel' ):
            scores = 1
            selectedItems( selector, computer )
            addRecord( selector, computer, 'Gana Humano! (=' )
            print("-> Resultado: Gana Humano! (= \n")

    return scores

# Menú secundario
def menuResult():
    print('\n-> ¿Qué desea hacer?')
    print('1) Jugar otra vez')
    print('2) Ver resultado anterior')
    print('3) Salir')

# Juego
def main():
    score_player = 0
    score_computer = 0
    controller_menu = False
    
    # Ciclo del primer menú
    while controller_menu == False:

        controller_menu_result = False
        scores = play()
        if scores == 1:
            score_player += 1
        elif scores == 2:
            score_computer += 1
        print ("-> Puntuaciones: Ordenador ->", score_computer, "jugador ->", score_player)

        # Menú secundario 
        while controller_menu_result == False:

            menuResult()
            again = input()
        
            if ( again  == '1' ):
                print('-> A jugar de nuevo!')
                controller_menu_result = True

            elif ( again == '2' ):
                getLastRecord()

            elif ( again == '3' ):
                print("\n-> Juego finalizado! (=\n")
                controller_menu_result = True
                controller_menu = True

            else:
                print('A jugar de nuevo!')

# Inicializar el juego
main()