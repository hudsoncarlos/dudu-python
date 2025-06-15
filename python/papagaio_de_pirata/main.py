import sys
import webbrowser
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QLabel, QListWidget, QListWidgetItem, QMessageBox, 
    QHBoxLayout, QDateEdit, QLineEdit
)
# from python.papagaio_de_pirata.banco_dados_json import carregar_contas, salvar_contas, registrar_pagamento
from datetime import datetime
from banco_sqlite import (
    inicializar_banco, listar_contas, marcar_como_paga, adicionar_conta
)

class AppContas(QWidget):
    def __init__(self):
        inicializar_banco()

        super().__init__()
        self.setWindowTitle("🔔 Lembrete de Contas a Pagar")
        self.setMinimumWidth(500)

        filtros = QHBoxLayout()
        self.filtro_status = "todas"
        
        self.layout = QVBoxLayout()
        self.lista_contas = QListWidget()
        self.atualizar_lista()

        self.layout.addWidget(QLabel("Contas próximas do vencimento:"))
        self.layout.addWidget(self.lista_contas)

        # Área de cadastro
        self.campo_nome = QLineEdit()
        self.campo_nome.setPlaceholderText("Nome da conta")

        self.campo_venc = QDateEdit()
        self.campo_venc.setCalendarPopup(True)
        self.campo_venc.setDisplayFormat("yyyy-MM-dd")

        self.campo_url = QLineEdit()
        self.campo_url.setPlaceholderText("Link do boleto ou site")

        btn_add = QPushButton("Adicionar conta")
        btn_add.clicked.connect(self.adicionar_conta)

        formulario = QVBoxLayout()
        formulario.addWidget(self.campo_nome)
        formulario.addWidget(self.campo_venc)
        formulario.addWidget(self.campo_url)
        formulario.addWidget(btn_add)

        self.layout.addLayout(formulario)

        btns = QHBoxLayout()
        btn_pagar = QPushButton("💰 Marcar como paga")
        btn_abrir = QPushButton("🌐 Abrir site")
        btn_atualizar = QPushButton("🔄 Atualizar lista")

        btn_pagar.clicked.connect(self.marcar_como_paga)
        btn_abrir.clicked.connect(self.abrir_site)
        btn_atualizar.clicked.connect(self.atualizar_lista)

        btn_todas = QPushButton("📋 Todas")
        btn_vencer = QPushButton("⏳ À Vencer")
        btn_vencidas = QPushButton("⚠️ Vencidas")

        btn_todas.clicked.connect(lambda: self.set_filtro("todas"))
        btn_vencer.clicked.connect(lambda: self.set_filtro("vencer"))
        btn_vencidas.clicked.connect(lambda: self.set_filtro("vencidas"))

        filtros.addWidget(btn_todas)
        filtros.addWidget(btn_vencer)
        filtros.addWidget(btn_vencidas)
        self.layout.addLayout(filtros)

        btns.addWidget(btn_pagar)
        btns.addWidget(btn_abrir)
        btns.addWidget(btn_atualizar)
        self.layout.addLayout(btns)

        self.setLayout(self.layout)

    def set_filtro(self, status):
        self.filtro_status = status
        self.atualizar_lista()

    from datetime import datetime

    def atualizar_lista(self):
        self.lista_contas.clear()
        hoje = datetime.today().date()

        # status pode ser: todas, vencer, vencidas
        contas_raw = listar_contas("pendente")
        for c in contas_raw:
            id_, nome, vencimento, url, status = c
            venc = datetime.strptime(vencimento, "%Y-%m-%d").date()
            dias = (venc - hoje).days

            if self.filtro_status == "vencer" and dias < 0:
                continue
            elif self.filtro_status == "vencidas" and dias >= 0:
                continue

            texto = f"{nome} - Vence em {dias} dia(s)"
            item = QListWidgetItem(texto)
            item.setData(1000, {"id": id_, "nome": nome, "url": url})
            self.lista_contas.addItem(item)


    def marcar_como_paga(self):
        item = self.lista_contas.currentItem()
        if not item:
            return QMessageBox.warning(self, "Atenção", "Selecione uma conta.")

        conta = item.data(1000)
        marcar_como_paga(conta["id"])
        self.atualizar_lista()
        QMessageBox.information(self, "Pagamento", f"Conta '{conta['nome']}' marcada como paga.")


    def abrir_site(self):
        item = self.lista_contas.currentItem()
        if not item:
            return QMessageBox.warning(self, "Atenção", "Selecione uma conta.")
        
        conta = item.data(1000)
        webbrowser.open(conta["url"])

    def adicionar_conta(self):
        nome = self.campo_nome.text().strip()
        venc = self.campo_venc.date().toString("yyyy-MM-dd")
        url = self.campo_url.text().strip()

        if not nome or not venc:
            QMessageBox.warning(self, "Erro", "Preencha todos os campos obrigatórios.")
            return

        adicionar_conta(nome, venc, url)
        QMessageBox.information(self, "Conta adicionada", f"{nome} adicionada com vencimento em {venc}.")
        
        # Limpar campos e atualizar lista
        self.campo_nome.clear()
        self.campo_url.clear()
        self.atualizar_lista()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = AppContas()
    janela.show()
    sys.exit(app.exec_())
