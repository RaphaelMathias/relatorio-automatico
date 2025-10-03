import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import smtplib
from email.message import EmailMessage
import ssl
from datetime import *
import calendar
import locale


# total de vendas
# faturamento total
# produto mais vendido
# grafico com relatorio

# Múltiplos relatórios por período
# Comparativo vs período anterior
# Mais gráficos
# Modo local vs modo envio
# Configuração via arquivo YAML ou JSON
# Tratamento de erros e logs

# 1. total de vendas no ano = soma geral da coluna de vendas
# 2. Produto mais vendido = Descobrir qual produto somou mais vendas no ano inteiro.
# 3. Top 5 produtos = Fazer um ranking do mais vendido até o 5º lugar.
# 4. Vendas por mês = Agrupar por mês e calcular o total de cada um.
# 5. Mês campeão de vendas = Encontrar qual mês teve o maior valor.
# 6. Comparação entre primeiro e último trimestre = Total de jan–mar vs out–dez e ver se houve crescimento ou queda.
# 7. Produto mais vendido em um mês específico = Exemplo: em julho, qual foi o campeão?
# 8. Dia com maior faturamento = Procurar a data que bateu recorde de vendas.
# 9. Média de vendas por produto = Calcular quanto, em média, cada produto vende por ocorrência.
# 10. Participação percentual de cada produto = Quanto % cada um representa do total anual.


def formatar_moeda(valor: float) -> str:
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


df = pd.read_csv("vendas_2024_com_preco.csv")
df["faturamento"] = df["vendas"] * df["preco_unitario"]
df["data"] = pd.to_datetime(df["data"], errors="coerce")


locale.setlocale(locale.LC_TIME, "pt_BR.UTF8")
hoje = date.today()
mes_num = hoje.month
mes = hoje.strftime("%B")
mes_anterior = mes_num - 1 if mes_num > 1 else 12
df_mes_anterior = df[df["data"].dt.month == mes_anterior]
df_mes = df[df["data"].dt.month == mes_num]


faturamento_ano = float(df["faturamento"].sum())
faturamento_ano_moeda = formatar_moeda(faturamento_ano)
faturamento_mes = df_mes["faturamento"].sum()
faturamento_mes_moeda = formatar_moeda(faturamento_mes)
faturamento_por_produto = df.groupby("produto")["faturamento"].sum()

produto_mais_vendido_ano = df.groupby("produto")["vendas"].sum().idxmax()
produto_mais_vendido_mes = df_mes.groupby("produto")["vendas"].sum().idxmax()

valor_mes_atual = df_mes["vendas"].sum()
valor_mes_anterior = df_mes_anterior["vendas"].sum()

total_vendas_ano = int(df["vendas"].sum())
total_vendas_mes = df[df["data"].dt.month == mes_num]["vendas"].sum()

variacao_mes_percentual = (valor_mes_atual / valor_mes_anterior) * 100  # ta errado
mais_vendido_grafico = df.groupby("produto")["vendas"].sum()


assinatura = "Raphael Mathias Ferreira"

# Grafico de mais vendidos
plt.figure(figsize=(10, 6))
mais_vendido_grafico.plot(kind="bar", color="skyblue")
plt.title("Grafico de vendas")
plt.xlabel("produto")
plt.ylabel("quantidade de vendas")
plt.xticks(rotation=45)
plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(integer=True))
plt.ylim(0, max(mais_vendido_grafico) + 5)
plt.tight_layout()
plt.savefig("Grafico_de_vendas.png")
# plt.show() # lembra de ativar de novo

# Grafico de faturamento
plt.figure(figsize=(10, 6))
faturamento_por_produto.plot(kind="bar", color="green")
plt.title("Grafico de Faturamento")
plt.xlabel("produto")
plt.ylabel("Faturamento")
plt.xticks(rotation=45)
plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(integer=True))
plt.ylim(0, max(faturamento_por_produto) + 5)
plt.tight_layout()
plt.savefig("Grafico_de_faturamento.png")
# plt.show()   # lembra de ativar de novo


# parte da criação e envio do E-mail
corpo = f"""

Prezados,

Segue abaixo o relatório completo de desempenho de vendas:

Resumo Anual

Total de vendas no ano: {total_vendas_ano}
Faturamento anual: {faturamento_ano_moeda}
Produto mais vendido no ano: {produto_mais_vendido_ano}

Resumo Mensal ({mes})

Total de vendas: {total_vendas_mes}
Faturamento: {faturamento_mes_moeda}
Produto mais vendido: {produto_mais_vendido_mes}
Variação em relação ao mês anterior: {variacao_mes_percentual:.2f}%



Atenciosamente,
{assinatura}

"""


email_destinatario = "raphael.mathias18@icloud.com"
email_remetento = "raphael.mathiasferreira18@gmail.com"
senha = "jjveuredelysmcqt"
assunto = "Relatorio de vendas"

mensagem = EmailMessage()
mensagem["From"] = email_remetento
mensagem["To"] = email_destinatario
mensagem["Subject"] = assunto
mensagem.set_content(corpo)

with open("Grafico_de_vendas.png", "rb") as arquivo:
    conteudo = arquivo.read()
    mensagem.add_attachment(
        conteudo, maintype="image", subtype="png", filename="Grafico_de_vendas.png"
    )

with open("Grafico_de_faturamento.png", "rb") as arquivo:
    conteudo = arquivo.read()
    mensagem.add_attachment(
        conteudo, maintype="image", subtype="png", filename="Grafico_de_faturamento.png"
    )

contexto = ssl.create_default_context()

with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=contexto) as servidor:
    servidor.login(email_remetento, senha)
    servidor.send_message(mensagem)
print("E-mail enviado com sucesso")
