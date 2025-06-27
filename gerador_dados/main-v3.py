from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QTextEdit, QFileDialog, QMessageBox, QHBoxLayout
)
from PyQt5.QtGui import QClipboard
import sys
import json
from gerador_dados import gerar_lista_dados
from exportador import salvar_em_csv, salvar_em_json


class GeradorDadosWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gerador de Dados • Tolkien + Pessoais")
        self.setMinimumSize(700, 500)

        self.layout_principal = QVBoxLayout()
        self.setLayout(self.layout_principal)

        # Botões
        btn_layout = QHBoxLayout()
        self.btn_gerar = QPushButton("🔁 Gerar Dados")
        self.btn_copiar = QPushButton("📋 Copiar Tudo")
        self.btn_exportar_csv = QPushButton("💾 Exportar CSV")
        self.btn_exportar_json = QPushButton("💾 Exportar JSON")

        btn_layout.addWidget(self.btn_gerar)
        btn_layout.addWidget(self.btn_copiar)
        btn_layout.addWidget(self.btn_exportar_csv)
        btn_layout.addWidget(self.btn_exportar_json)
        self.layout_principal.addLayout(btn_layout)

        # Área de exibição
        self.text_area = QTextEdit()
        self.layout_principal.addWidget(self.text_area)

        # Conexões
        self.btn_gerar.clicked.connect(self.gerar_dados)
        self.btn_copiar.clicked.connect(self.copiar_dados)
        self.btn_exportar_csv.clicked.connect(self.exportar_csv)
        self.btn_exportar_json.clicked.connect(self.exportar_json)

        self.dados_atuais = []

    def gerar_dados(self):
        self.dados_atuais = gerar_lista_dados(quantidade=5)
        texto = json.dumps(self.dados_atuais, ensure_ascii=False, indent=4)
        self.text_area.setPlainText(texto)

    def copiar_dados(self):
        texto = self.text_area.toPlainText()
        if texto:
            QApplication.clipboard().setText(texto)
            QMessageBox.information(self, "Copiado", "Dados copiados para a área de transferência!")
        else:
            QMessageBox.warning(self, "Aviso", "Nada para copiar.")

    def exportar_csv(self):
        if not self.dados_atuais:
            QMessageBox.warning(self, "Aviso", "Gere os dados primeiro.")
            return
        caminho, _ = QFileDialog.getSaveFileName(self, "Salvar como CSV", "saida/dados.csv", "CSV Files (*.csv)")
        if caminho:
            salvar_em_csv(self.dados_atuais, caminho)
            QMessageBox.information(self, "Salvo", f"Dados salvos em:\n{caminho}")

    def exportar_json(self):
        if not self.dados_atuais:
            QMessageBox.warning(self, "Aviso", "Gere os dados primeiro.")
            return
        caminho, _ = QFileDialog.getSaveFileName(self, "Salvar como JSON", "saida/dados.json", "JSON Files (*.json)")
        if caminho:
            salvar_em_json(self.dados_atuais, caminho)
            QMessageBox.information(self, "Salvo", f"Dados salvos em:\n{caminho}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GeradorDadosWindow()
    window.show()
    sys.exit(app.exec_())
