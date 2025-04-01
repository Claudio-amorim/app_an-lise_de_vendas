import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
                             QComboBox, QMessageBox, QFrame, QHeaderView)
from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import pandas as pd
from datetime import datetime

class DrinkSalesApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TechDrink Analytics")
        self.setGeometry(100, 100, 1000, 700)
        
        # Configuração de estilo
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2c3e50;
            }
            QLabel {
                color: #ecf0f1;
                font-size: 14px;
            }
            QLineEdit, QComboBox {
                background-color: #34495e;
                color: #ecf0f1;
                border: 1px solid #7f8c8d;
                padding: 5px;
                border-radius: 4px;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QTableWidget {
                background-color: #34495e;
                color: #ecf0f1;
                border: 1px solid #7f8c8d;
                gridline-color: #7f8c8d;
            }
            QHeaderView::section {
                background-color: #2c3e50;
                color: #ecf0f1;
                padding: 5px;
                border: none;
            }
        """)
        
        # Dados iniciais
        self.drinks = ["Caipirinha", "Mojito", "Margarita", "Martini", "Cosmopolitan", "Negroni"]
        self.sales_data = []
        
        self.initUI()
        
    def initUI(self):
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Painel esquerdo (entrada de dados)
        left_panel = QFrame()
        left_panel.setFrameShape(QFrame.StyledPanel)
        left_layout = QVBoxLayout()
        left_panel.setLayout(left_layout)
        
        # Título
        title = QLabel("TechDrink Analytics")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setStyleSheet("color: #3498db;")
        left_layout.addWidget(title)
        
        # Formulário de entrada
        form_layout = QVBoxLayout()
        
        # Drink
        drink_label = QLabel("Selecione o Drink:")
        self.drink_combo = QComboBox()
        self.drink_combo.addItems(self.drinks)
        form_layout.addWidget(drink_label)
        form_layout.addWidget(self.drink_combo)
        
        # Quantidade
        qty_label = QLabel("Quantidade Vendida:")
        self.qty_input = QLineEdit()
        self.qty_input.setPlaceholderText("Digite a quantidade")
        form_layout.addWidget(qty_label)
        form_layout.addWidget(self.qty_input)
        
        # Valor
        value_label = QLabel("Valor Total (R$):")
        self.value_input = QLineEdit()
        self.value_input.setPlaceholderText("Digite o valor total")
        form_layout.addWidget(value_label)
        form_layout.addWidget(self.value_input)
        
        # Botão de adicionar
        add_button = QPushButton("Adicionar Venda")
        add_button.clicked.connect(self.add_sale)
        form_layout.addWidget(add_button)
        
        left_layout.addLayout(form_layout)
        
        # Tabela de vendas
        self.sales_table = QTableWidget()
        self.sales_table.setColumnCount(4)
        self.sales_table.setHorizontalHeaderLabels(["Data", "Drink", "Quantidade", "Valor (R$)"])
        self.sales_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        left_layout.addWidget(self.sales_table)
        
        # Painel direito (análise e gráficos)
        right_panel = QFrame()
        right_panel.setFrameShape(QFrame.StyledPanel)
        right_layout = QVBoxLayout()
        right_panel.setLayout(right_layout)
        
        # Título de análise
        analysis_title = QLabel("Análise de Vendas")
        analysis_title.setFont(QFont("Arial", 16, QFont.Bold))
        analysis_title.setStyleSheet("color: #3498db;")
        right_layout.addWidget(analysis_title)
        
        # Resultados da análise
        self.analysis_results = QLabel()
        self.analysis_results.setWordWrap(True)
        self.analysis_results.setStyleSheet("color: #ecf0f1; font-size: 14px;")
        right_layout.addWidget(self.analysis_results)
        
        # Gráfico
        self.figure = plt.figure(facecolor='#34495e')
        self.canvas = FigureCanvas(self.figure)
        right_layout.addWidget(self.canvas)
        
        # Botão de análise
        analyze_button = QPushButton("Gerar Análise")
        analyze_button.clicked.connect(self.analyze_sales)
        right_layout.addWidget(analyze_button)
        
        # Adicionando painéis ao layout principal
        main_layout.addWidget(left_panel, 1)
        main_layout.addWidget(right_panel, 1)
        
    def add_sale(self):
        drink = self.drink_combo.currentText()
        qty = self.qty_input.text()
        value = self.value_input.text()
        
        if not qty or not value:
            QMessageBox.warning(self, "Atenção", "Preencha todos os campos!")
            return
            
        try:
            qty = int(qty)
            value = float(value)
        except ValueError:
            QMessageBox.warning(self, "Erro", "Quantidade deve ser inteiro e valor deve ser numérico!")
            return
            
        # Adiciona venda aos dados
        sale = {
            "date": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "drink": drink,
            "quantity": qty,
            "value": value
        }
        self.sales_data.append(sale)
        
        # Atualiza tabela
        self.update_sales_table()
        
        # Limpa campos
        self.qty_input.clear()
        self.value_input.clear()
        
    def update_sales_table(self):
        self.sales_table.setRowCount(len(self.sales_data))
        
        for row, sale in enumerate(self.sales_data):
            self.sales_table.setItem(row, 0, QTableWidgetItem(sale["date"]))
            self.sales_table.setItem(row, 1, QTableWidgetItem(sale["drink"]))
            self.sales_table.setItem(row, 2, QTableWidgetItem(str(sale["quantity"])))
            self.sales_table.setItem(row, 3, QTableWidgetItem(f"R$ {sale['value']:.2f}"))
            
    def analyze_sales(self):
        if not self.sales_data:
            QMessageBox.warning(self, "Atenção", "Nenhum dado de venda disponível para análise!")
            return
            
        # Cria DataFrame para análise
        df = pd.DataFrame(self.sales_data)
        
        # Análise por quantidade
        qty_by_drink = df.groupby('drink')['quantity'].sum().sort_values(ascending=False)
        total_qty = qty_by_drink.sum()
        
        # Análise por valor
        value_by_drink = df.groupby('drink')['value'].sum().sort_values(ascending=False)
        total_value = value_by_drink.sum()
        
        # Drink mais vendido
        top_drink_qty = qty_by_drink.idxmax()
        top_drink_value = value_by_drink.idxmax()
        
        # Drink menos vendido
        worst_drink_qty = qty_by_drink.idxmin()
        worst_drink_value = value_by_drink.idxmin()
        
        # Texto de análise
        analysis_text = f"""
        <b>Análise Completa:</b><br><br>
        <b>Total de Drinks Vendidos:</b> {total_qty}<br>
        <b>Faturamento Total:</b> R$ {total_value:.2f}<br><br>
        
        <b>Drink mais vendido (quantidade):</b> {top_drink_qty} ({qty_by_drink[top_drink_qty]} unidades)<br>
        <b>Drink mais lucrativo:</b> {top_drink_value} (R$ {value_by_drink[top_drink_value]:.2f})<br><br>
        
        <b>Drink que precisa vender mais (quantidade):</b> {worst_drink_qty} ({qty_by_drink[worst_drink_qty]} unidades)<br>
        <b>Drink menos lucrativo:</b> {worst_drink_value} (R$ {value_by_drink[worst_drink_value]:.2f})<br>
        """
        
        self.analysis_results.setText(analysis_text)
        
        # Atualiza gráfico
        self.update_chart(qty_by_drink, value_by_drink)
        
    def update_chart(self, qty_data, value_data):
        self.figure.clear()
        
        # Gráfico de barras para quantidade
        ax1 = self.figure.add_subplot(211)
        qty_data.plot(kind='bar', ax=ax1, color='#3498db')
        ax1.set_title('Vendas por Quantidade', color='white')
        ax1.set_facecolor('#34495e')
        ax1.tick_params(axis='x', colors='white')
        ax1.tick_params(axis='y', colors='white')
        ax1.spines['bottom'].set_color('white')
        ax1.spines['left'].set_color('white')
        ax1.spines['top'].set_visible(False)
        ax1.spines['right'].set_visible(False)
        
        # Gráfico de barras para valor
        ax2 = self.figure.add_subplot(212)
        value_data.plot(kind='bar', ax=ax2, color='#2ecc71')
        ax2.set_title('Vendas por Valor (R$)', color='white')
        ax2.set_facecolor('#34495e')
        ax2.tick_params(axis='x', colors='white')
        ax2.tick_params(axis='y', colors='white')
        ax2.spines['bottom'].set_color('white')
        ax2.spines['left'].set_color('white')
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)
        
        self.figure.tight_layout()
        self.canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Configuração de estilo adicional
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(44, 62, 80))
    palette.setColor(QPalette.WindowText, QColor(236, 240, 241))
    app.setPalette(palette)
    
    window = DrinkSalesApp()
    window.show()
    sys.exit(app.exec_())