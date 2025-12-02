#INICIALIZADOR DO CONSOLE
from database import init_db
from controllers.main_controller import MainController

def main():
    init_db()
    controller = MainController()
    controller.iniciar()

if __name__ == "__main__":
    main()