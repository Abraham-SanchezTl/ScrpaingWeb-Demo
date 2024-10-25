import sys
import time
from PyQt6.QtCore import pyqtSignal, QThread, Qt
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QLabel, QGroupBox, QWidget, QStatusBar, QApplication, QDialog,  QMessageBox
from PyQt6.QtGui import QAction
from .config_explore_data import ConfigVentanaExplore
from .config_update_data import ConfigUpdateData
from .config_upload_xlsx import ConfigUploadXlsx
from .config_update_xlsx import ConfigUpdateXlsx
from src import main_explore_data, main_update_data, main_upload_xlsx, main_update_xlsx
from src.upload_xlsx import revertir_xlsx
from src.utilities import conectar_bd, cerrar_bd


class HiloDeTrabajo(QThread):
    progress = pyqtSignal(str)

    def __init__(self, script_function):
        super().__init__()
        self.script_function = script_function

    def run(self):
        sys.stdout = self  # Redirigir stdout al hilo actual
        sys.stderr = self  # Redirigir stderr al hilo actual
        try:
            self.script_function()  # Ejecutar
        finally:
            sys.stdout = sys.__stdout__  # Restaurar stdout
            sys.stderr = sys.__stderr__  # Restaurar stderr

    def write(self, text):
        #Escribir la salida
        self.progress.emit(str(text))

    def flush(self):
        pass


class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("WebScraper")
        # Obtener la resolución de la pantalla
        screen = QApplication.primaryScreen()
        screen_geometry = screen.geometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()

        # Posicion y tamaño de ventana
        self.setGeometry(0, 0, screen_width// 2 , screen_height)


       # Barra de menu
        menubar = self.menuBar()
        barra_menu = menubar.addMenu("Deshacer")
        ejecutar_revertir_upload_xlsx = QAction("Carga de xlsx", self)
        ejecutar_revertir_upload_xlsx.triggered.connect(self.confirmar_revertir_upload_xlsx)
        # Añadir la acción al menú Deshacer
        barra_menu.addAction(ejecutar_revertir_upload_xlsx)

        # Crear un widget central para contener el layout principal
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Crear layout principal con margen y espaciado
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)  # Espaciado entre widgets
        main_layout.setContentsMargins(10, 10, 10, 10)  # Márgenes alrededor del layout

        # Crear layout de botones alieneados horizontalmente
        button_layout = QHBoxLayout()

        # Botones
        explore_data_box = self.seccion_btn("Exploración datos", "Iniciar Exploración", self.run_explore_data)
        update_data_box = self.seccion_btn("Actualización de datos Seleccionados", "Iniciar Actualización de datos", self.run_update_data)
        upload_xlsx_box = self.seccion_btn("Subir xlsx", "Cargar Datos", self.run_upload_xlsx)
        update_xlsx_box = self.seccion_btn("Actualizar xlsx", "Cargar Datos", self.run_update_xlsx)

        # Añadir las secciones al layout horizontal
        button_layout.addWidget(explore_data_box)
        button_layout.addWidget(update_data_box)
        button_layout.addWidget(upload_xlsx_box)
        button_layout.addWidget(update_xlsx_box)

        # Añadir el layout horizontal al layout principal
        main_layout.addLayout(button_layout)

        # Consola de salida
        self.output_console = QTextEdit()
        self.output_console.setReadOnly(True)
        self.output_console.setStyleSheet("background-color: #1e1e1e; color: #d4d4d4; font-family: Consolas; font-size: 12px;")
        main_layout.addWidget(QLabel("Consola de salida:"))
        main_layout.addWidget(self.output_console)

        central_widget.setLayout(main_layout)
        # Variables para almacenar la salida progresiva
        self.console_output = ""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)


    # Confirmacion para revertir UploadXlsx
    def confirmar_revertir_upload_xlsx(self):
        reply = QMessageBox.question(
            self,
            "Confirmación",
            "¿Estás seguro de que quieres revertir la ultima carga de xlsx?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.ejecutar_revertir_upload_xlsx()

    
    # Ejecucion revertir UploadXlsx
    def ejecutar_revertir_upload_xlsx(self):
        try:
            cnx = conectar_bd()
            revertir_xlsx(cnx)  # Llamada a la primera función
            cerrar_bd(cnx)
            QMessageBox.information(self, "Éxito", "Ultima carga de xlsx fue revertida.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Se produjo un error al ejecutar  al revertir la carga de xlsx: {str(e)}")

    


    def seccion_btn(self, title, button_text, run_function):
        group_box = QGroupBox(title)
        group_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
        group_box.setStyleSheet("QGroupBox { font-weight: bold; font-size: 16px; }")
        layout = QVBoxLayout()

        # Botón para ejecutar
        run_button = QPushButton(button_text)
        run_button.clicked.connect(run_function)
        layout.addWidget(run_button)

        group_box.setLayout(layout)
        return group_box

    def update_console(self, text):
        #Actualizar la consola con el texto recibido desde el hilo y elimina saltos de linea 
        cleaned_text = text.rstrip()
        self.output_console.append(cleaned_text)


        # Ejecutar una función de script en un hilo separado.
    def run_script(self, script_function):
        self.thread = HiloDeTrabajo(script_function)
        self.thread.progress.connect(self.update_console)
        self.thread.start()


    # Funciones para ejecutar
    # Abre configuracion, si configuracion fue guardad ejecuta el script
    def run_explore_data(self):
        config_window = ConfigVentanaExplore(self)        
        if config_window.exec() == QDialog.DialogCode.Accepted:
            if config_window.was_config_saved():
                self.run_script(main_explore_data)


    def run_update_data(self):
        config_window = ConfigUpdateData(self)
        if config_window.exec() == QDialog.DialogCode.Accepted:
            if config_window.was_config_saved():
                self.run_script(main_update_data)


    def run_upload_xlsx(self):
        config_window = ConfigUploadXlsx(self)
        if config_window.exec() == QDialog.DialogCode.Accepted:
            if config_window.was_config_saved():
                self.run_script(main_upload_xlsx)


    def run_update_xlsx(self):
        config_window = ConfigUpdateXlsx(self)        
        if config_window.exec() == QDialog.DialogCode.Accepted:
            if config_window.was_config_saved():
                self.run_script(main_update_xlsx)


    # Funciones para abrir ventanas de configuracion.
    def config_explore_data(self):
        config_window = ConfigVentanaExplore(self)
        config_window.exec()

    def config_update_data(self):
        config_window = ConfigUpdateData(self)
        config_window.exec()

    def config_upload_xlsx(self):
        config_window = ConfigUploadXlsx(self)
        config_window.exec()

    def config_update_xlsx(self):
        config_window = ConfigUpdateXlsx(self)
        config_window.exec()


