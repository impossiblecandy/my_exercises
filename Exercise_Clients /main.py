clients = {}
op = ''


def add_client():
    # Funcion para añadir un cliente
    print('1 - Añadir cliente')
    print("Introduzca los siguientes datos")
    nif = input("NIF: ")
    # Verificar el nif del cliente
    if len(nif) != 9:
        print("El nif debe contener 9 caracteres")
        return
    if not nif[0:8].isdigit():
        print("Los primeros ocho caracteres deben ser numeros")
        return
    if not 'A' <= nif[8] <= 'Z':
        print("El último caracter debe de ser una letra mayúscula")
        return True
    nombre = input("Nombre: ")
    apellidos = input("Apellidos: ")
    direccion = input("Dirección: ")
    telefono = input("Teléfono: ")
    # Funcion para verificar el telefono del cliente
    if len(telefono) != 9:
        print("El telefono debe contener 9 caracteres")
        return
    else:
        if not telefono.isdigit():
            print("El telefono debe contener solo digitos")
            return
    correo = input("Correo: ")
    # Funcion para verificar el correo del cliente
    if '@' not in correo:
        print("La dirección de correo no tiene arroba")
        return
    habitual = bool(input("Habitual (True/False): "))
    from datetime import datetime
    fecha = input("Introduzca la fecha de la operación 'dd/mm/aaaa': ").strip()
    # Verificar la fecha
    try:
        fecha = datetime.strptime(fecha, '%d/%m/%Y')
    except ValueError:
        print("No ha ingresado una fecha válida")
    client = {'Nombre': nombre, 'Apellidos': apellidos, 'Direccion': direccion, 'Telefono': telefono, 'Correo': correo, 'Habitual': habitual == True, 'Fecha': fecha}
    clients[nif] = client



def delete_client():
    # Funcion para borrar un cliente
    print('2 - Eliminar cliente')
    nif = input("\n Introduzca el NIF del usuario que desea eliminar :\n").strip()
    if nif in clients:
        del clients[nif]
        print('El usuario ha sido eliminado')
    else:
        print('No existe el cliente con el nif', nif)


def show_client():
    # Funcion para mostrar un cliente
    print('3 - Mostrar cliente')
    nif = input("Introduzca el NIF del cliente que desea ver: ")
    if nif in clients:
        print(clients[nif])
    else:
        print('No existe el cliente con el nif: ', nif)

def list_of_clients():
    # Funcion para mostrar la lista de clientes
    print('4 - Listar todos los clientes')
    print("---------------------------------------------- Listado de clientes -----------------------------------------------")
    for clave, valor in clients.items():
        print("\nEl usuario con nif: ", clave)
        for claveValor, data in valor.items():
            print(claveValor, ": ", data)

    print('\n------------------------------------------------------------------------------------------------------------------')


def list_of_frequent_clients():
    # Funcion para mostrar la lista de clientes habituales
    print('5 - Listar clientes habituales')
    print("---------------------------------------------- Listado de clientes habituales -----------------------------------------------")
    for clave, valor in clients.items():
        if valor['Habitual']:
            print("\nEl usuario habitual con nif: ", clave)
        for claveValor, data in valor.items():
            print(claveValor, ": ", data)
    print('\n------------------------------------------------------------------------------------------------------------------')

def exit_program():
    # Funcion para salir del programa
    print('Saliendo del menú')
    return True


def menu():
    # Funcion del menu
    salir = False
    while not salir:
        print('______ MENU ______')
        print()
        print("1. Añadir cliente \n"
              "2. Eliminar cliente \n"
              "3. Mostrar cliente \n"
              "4. Listar todos los clientes \n"
              "5. Listar clientes habituales \n"
              "6. Salir \n     ")

        op = int(input('Seleccione una opción: '))

        if op == 1:
            add_client()
        elif op == 2:
            delete_client()
        elif op == 3:
            show_client()
        elif op == 4:
            list_of_clients()
        elif op == 5:
            list_of_frequent_clients()
        elif op == 6:
            salir = exit_program()
        else:
            print()
            print('Debe seleccionar una opción de 1 a 6')
            print()


menu()
