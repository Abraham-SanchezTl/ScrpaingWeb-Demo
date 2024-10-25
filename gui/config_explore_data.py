import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QGroupBox, QHBoxLayout, QLabel, QLineEdit, QDateEdit, QFileDialog, QDialog, QMessageBox)
from PyQt6.QtCore import QDate, QProcess, QTimer
import os
import json
import time
from pathlib import Path


# Venta de opciones
class ConfigVentanaExplore(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Configuración
        self.setWindowTitle("Configuración")
        self.setGeometry(150, 150, 200, 200)
        layout = QVBoxLayout()

        # Campos de texto
        self.text_input = QLineEdit()
        self.text_input.setPlaceholderText("Ejemplo: 1, 3, 4, 5, 6")
        self.text_input.setText("1, 2, 3, 4")
        layout.addWidget(QLabel("Ingresa los números de página a explorar:"))
        layout.addWidget(self.text_input)

        # Botón Guardar
        self.save_button = QPushButton("Guardar")
        self.save_button.clicked.connect(self.save_config)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

        # Variable de estado
        self.config_saved = False
        # Variables de almacenamiento
        self.saved_text = ""

    def save_config(self):
        self.saved_text = self.text_input.text()
        # Procesar el texto para convertirlo en una lista de numeros
        try:
            split_text = self.saved_text.split(',')
            stripped_text = [x.strip() for x in split_text]
            filtered_text = [x for x in stripped_text if x.isdigit()]
            pages_list = [int(x) for x in filtered_text]

        except ValueError:
            # Indica error si no introduce numeros.
            QMessageBox.warning(self, "Error", "Por favor, ingresa solo números separados por comas.")
            return
        
        # Ruta de archivo config
        current_dir = Path(__file__).resolve().parent
        config_path = (current_dir / '..' / 'config' / 'config.json').resolve()

        # Leer el archivo config
        with open(config_path, 'r') as file:
            config = json.load(file)
        config['explore_settings']['pages'] = pages_list
        
        # Guardar los cambios de archivo config
        with open(config_path, 'w') as file:
            json.dump(config, file, indent=4)
        
        # Actualiza variable de estado y cierra ventana
        self.config_saved = True
        self.accept()

    # Verifica si configuracion fue guardada
    def was_config_saved(self):
        return self.config_saved