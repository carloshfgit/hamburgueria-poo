#INICIALIZADOR DA INTERFACE GRÁFICA
from database import init_db
from views.graficos.main_window import MainWindow

if __name__ == "__main__":
    init_db()
    
    app = MainWindow()
    app.mainloop()