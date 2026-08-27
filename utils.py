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
    arquivo = open(f'templates/{nome}', 'r', encoding="utf-8")
    conteudo = arquivo.read()
    arquivo.close()
    return conteudo

def add_note(dicionario):
    database = Database("notes")
    note = Note(title=dicionario["titulo"], content=dicionario["detalhes"])
    database.add(note)

def get_note(note_id):
    database = Database("notes")
    return database.get_by_id(note_id)

def update_note(note_id, dicionario):
    database = Database("notes")
    note = Note(
        id=note_id,
        title=dicionario["titulo"],
        content=dicionario["detalhes"]
    )
    database.update(note)

def build_response(body='', code=200, reason='OK', headers=''):
    response = f'HTTP/1.1 {code} {reason}\n'

    if headers:
        response += headers + '\n'

    response += '\n'
    response += body

    return response.encode()

def delete_note(id):
    database = Database("notes")
    database.delete(id)
    return build_response(
        code=303,
        reason='See Other',
        headers='Location: /'
    )

def not_found():
    return build_response(
        body=load_template('404.html'),
        code=404,
        reason='Not Found'
    )