import json
from database import Database,  Note

def extract_route(requisicao):
    resp = requisicao.split(' ')
    if len(resp) > 0:
        resp = resp[1]
        return resp[1:]
    return

def read_file(argumento):
    arquivo = open(argumento, 'rb')
    conteudo = arquivo.read()
    arquivo.close()
    return conteudo

def load_data():
    database = Database("notes")
    return database.get_all()

def load_template(nome):
    arquivo = open(f'templates/{nome}', 'r')
    conteudo = arquivo.read()
    arquivo.close()
    return conteudo

def add_note(dicionario):
    database = Database("notes")
    note = Note(title=dicionario["titulo"], content=dicionario["detalhes"])
    database.add(note)

def build_response(body='', code=200, reason='OK', headers=''):
    response = f'HTTP/1.1 {code} {reason}\n'

    if headers:
        response += headers + '\n'

    response += '\n'
    response += body

    return response.encode()

def delete_note(note):
    database = Database("notes")
    database.delete(note)