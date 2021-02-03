from requests_html import HTMLSession
from time import sleep as slp
from time import localtime as lt
from time import asctime as at
from os import system as sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

session = HTMLSession()

#titulos = ['Resultado Preliminar da VD', 'Retificação de Edital - 012', 'Chamada IS da OREL SSPM (Retificada)', 'Retificação da IS da OREL SSPM', 'Convocação de Candidato Sub judice', 'Chamada para AP', 'Chamada para VD da OREL SSPM', 'Relação dos candidatos por OREL', 'Eliminados e Ausentes', 'Chamada para EVC - TAF-i', 'Resultado da Prova Escrita', 'Comunicado aos Candidatos - 007', 'Retificação de Edital - 011', 'Retificação de Edital - 010', 'Gabarito Final', 'Gabarito Preliminar', 'Comunicado aos Candidatos - 006', 'Retificação de Edital - 009', 'Retificação de Edital - 008', 'Comunicado aos Candidatos - 005', 'Retificação de Edital - 007', 'Retificação de Edital - 006', 'Retificação de Edital - 005', 'Retificação de Edital - 004', 'Comunicado aos Candidatos - 004', 'Retificação de Edital - 003', 'Retificação de Edital - 002', 'Comunicado aos Candidatos - 003', 'Comunicado aos Candidatos - 002', 'comunicado aos candidatos 001', 'Retificação de Edital - 001', 'Edital de abertura (retificado)']
titulos = ['Retificação de Edital - 001', 'Edital de abertura (retificado)']
teste = [
    ['Retificação de Edital - 001', 'Edital de abertura (retificado)'],
    ['comunicado aos candidatos 001', 'Retificação de Edital - 001', 'Edital de abertura (retificado)'],
    ['Comunicado aos Candidatos - 002', 'comunicado aos candidatos 001', 'Retificação de Edital - 001', 'Edital de abertura (retificado)'],
    ['Retificação de Edital - 001', 'Edital de abertura (retificado)'],
    ['Resultado Preliminar da VD', 'Retificação de Edital - 012', 'Chamada IS da OREL SSPM (Retificada)', 'Retificação da IS da OREL SSPM', 'Convocação de Candidato Sub judice', 'Chamada para AP', 'Chamada para VD da OREL SSPM', 'Relação dos candidatos por OREL', 'Eliminados e Ausentes', 'Chamada para EVC - TAF-i', 'Resultado da Prova Escrita', 'Comunicado aos Candidatos - 007', 'Retificação de Edital - 011', 'Retificação de Edital - 010', 'Gabarito Final', 'Gabarito Preliminar', 'Comunicado aos Candidatos - 006', 'Retificação de Edital - 009', 'Retificação de Edital - 008', 'Comunicado aos Candidatos - 005', 'Retificação de Edital - 007', 'Retificação de Edital - 006', 'Retificação de Edital - 005', 'Retificação de Edital - 004', 'Comunicado aos Candidatos - 004', 'Retificação de Edital - 003', 'Retificação de Edital - 002', 'Comunicado aos Candidatos - 003', 'Comunicado aos Candidatos - 002', 'comunicado aos candidatos 001', 'Edital de abertura (retificado)']
]
with open('secret.txt') as f:
    reader = f.readlines()
    email = reader[0].strip()
    senha = reader[1].strip()

smtp = 'smtp.gmail.com'

#while True:
for vezes in range(5):
    try:
        qwertyuiop = 1+1
        #r = session.get('https://www.inscricao.marinha.mil.br/marinha/index_concursos.jsp?id_concurso=384')
    except Exception as e:
        print('Conexão Rejeitada/Demorada')
    else:
        n_titulos = 0
        n_titulos_novos = 0
        #titulos_encontrados = [c.text for c in r.html.find('u')]
        titulos_encontrados = teste[vezes].copy()
        novos = []
        inalterados = []
        excluidos = []
        hora_consulta = at(lt())
        
        for c in range(len(titulos)):
            for b in range(len(titulos_encontrados)):
                if titulos[c] == titulos_encontrados[b]:
                    inalterados.append(c)
            if not c in inalterados:
                excluidos.append(c)

        for c in range(len(titulos_encontrados)):
            for b in range(len(titulos)):
                if titulos[b] == titulos_encontrados[c]:
                    pass
            if not c in inalterados and not c in excluidos:
                novos.append(c)

        if len(novos) != 0 or len(excluidos) != 0:
            ###########################################
            #               SEND MAIL
            ###########################################
            with open('email_cadastrados.txt') as f:
                reader = f.readlines()
                destino = [c.strip() for c in reader]

            subj = 'Alteração no Site da Concurso Público de Admissão às Escolas de Aprendizes de Marinheiro/2020'

            msg = MIMEMultipart()
            msg['From'] = email
            msg['Subject'] = subj

            txt = f'Olá, Candidato\n\nVenho lhe informar que existem informações mais recentes sobre seu concurso e da carreira que pretendes seguir.\n\n{len(novos)+len(excluidos)} Atualizações:\n\n'
            if len(novos) != 0 and len(excluidos) == 0:
                txt = txt + f'Novos: {", ".join([titulos_encontrados[c] for c in novos])}.'
            if len(novos) != 0 and len(excluidos) != 0:
                txt = txt + f'Novos: {", ".join([titulos_encontrados[c] for c in novos])}.\nExcluídos: {", ".join([titulos[c] for c in excluidos])}.'
            if len(novos) == 0 and len(excluidos) != 0:
                txt = txt + f'Excluídos: {", ".join([titulos[c] for c in excluidos])}.'
            txt = txt + f'\n\nAtualizado em: {hora_consulta}\nLink: <a href="https://www.inscricao.marinha.mil.br/marinha/index_concursos.jsp?id_concurso=384">Site do Concurso</a>'
            txt = txt.replace('\n', '<br>')
            msg_txt = MIMEText(txt, 'html')
            msg.attach(msg_txt)
            #print(msg.as_string())

            try:
                server = smtplib.SMTP(smtp, 587)
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(email, senha)
                server.sendmail(email, ','.join(destino), msg.as_string())
                server.quit()
            except Exception as err:
                print(f'Falha ao enviar email: {err}')
            else:
                print('Emais enviados com sucesso!')
        else:
            print('Sem  Atualizações, Sem e-mail')
        titulos = titulos_encontrados.copy()
    finally:
        print(f'--------------------------------\nRodada {vezes+1}\nNovos: {novos}\nInalterados: {inalterados}\nExcluidos: {excluidos}\n\n')
    slp(1)
