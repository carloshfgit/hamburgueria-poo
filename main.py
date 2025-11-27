from database import init_db
from controllers.main_controller import MainController

def main():
    # 1. Garante que o banco existe
    init_db()
    
    # 2. Instancia o controlador principal e inicia o sistema
    controller = MainController()
    controller.iniciar()

if __name__ == "__main__":
    main()