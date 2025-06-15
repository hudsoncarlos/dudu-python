import json
import os
from datetime import datetime

# Caminhos dos arquivos
ARQ_CONTAS = "contas.json"
ARQ_HISTORICO = "historico_pagamentos.json"

def carregar_contas():
    if not os.path.exists(ARQ_CONTAS):
        return []
    with open(ARQ_CONTAS, "r", encoding="utf-8") as f:
        return json.load(f)

def salvar_contas(contas):
    with open(ARQ_CONTAS, "w", encoding="utf-8") as f:
        json.dump(contas, f, indent=2, ensure_ascii=False)

def registrar_pagamento(conta):
    historico = []
    if os.path.exists(ARQ_HISTORICO):
        with open(ARQ_HISTORICO, "r", encoding="utf-8") as f:
            historico = json.load(f)

    conta_pago = conta.copy()
    conta_pago["data_pagamento"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    historico.append(conta_pago)

    with open(ARQ_HISTORICO, "w", encoding="utf-8") as f:
        json.dump(historico, f, indent=2, ensure_ascii=False)

def carregar_historico():
    if not os.path.exists(ARQ_HISTORICO):
        return []
    with open(ARQ_HISTORICO, "r", encoding="utf-8") as f:
        return json.load(f)
