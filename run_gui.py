from database import init_db
from views.gui.main_window import MainWindow

if __name__ == "__main__":
    # 1. Garante o banco de dados
    init_db()
    
    # 2. Inicia a Interface Gráfica
    app = MainWindow()
    app.mainloop()