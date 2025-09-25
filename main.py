import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import smtplib
from email.message import EmailMessage
import ssl


# total de vendas
# faturamento total
# produto mais vendido
# grafico com relatorio



class Main:
    df = pd.read_csv('arquivo.csv')
    df['faturamento'] = df['vendas'] * df['preco_unitario']

    total_de_vendas = int(df['vendas'].sum())
    faturamento = float(df['faturamento'].sum())
    mais_vendido = df.groupby('produto')['vendas'].sum().idxmax()
     



    email_destinatario = 'raphael.mathias18@icloud.com'
    email_remetento = 'raphael.mathiasferreira18@gmail.com'
    senha = 'hirgvcyywsowceip'
    assunto = 'Relatorio de vendas'
    corpo = f"""

    Prezado Sr. Vagabundo

    total de vendas no mês foram: {total_de_vendas}
    o faturamento total foi de: {faturamento:,.2f}
    o produto mais vendido foi: {mais_vendido}


    segue em anexo o grafico do relatorio

    """


    mais_vendido_grafico = df.groupby('produto')['vendas'].sum()


    plt.figure(figsize=(10,6))
    mais_vendido_grafico.plot(kind='bar', color='skyblue')

    plt.title('Grafico de vendas')
    plt.xlabel('produto')
    plt.ylabel('quantidade de vendas')

    plt.xticks(rotation=45)


    plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(integer=True))
    plt.ylim(0, max(mais_vendido_grafico) + 5)



    plt.tight_layout()
    plt.savefig('Grafico.png')
    plt.show()


    mensagem = EmailMessage()
    mensagem['From'] = email_remetento
    mensagem['To'] = email_destinatario
    mensagem['Subject'] = assunto
    mensagem.set_content(corpo)

    with open('Grafico.png', 'rb') as arquivo:
        conteudo = arquivo.read()
        mensagem.add_attachment(
            conteudo,
            maintype='image',
            subtype='png',
            filename='Grafico.png'
        )

    contexto = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=contexto) as servidor:
        servidor.login(email_remetento, senha)
        servidor.send_message(mensagem)

    print('E-mail enviado com sucesso')