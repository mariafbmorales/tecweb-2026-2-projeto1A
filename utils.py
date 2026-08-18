import json

def extract_route(requisicao):
    resp = requisicao.split(' ')
    if len(resp):
        resp = resp[1]
        return resp[1:]
    return

def read_file(argumento):
    arquivo = open(argumento, 'rb')
    conteudo = arquivo.read()
    arquivo.close()
    return conteudo

def load_data(nome):
    arquivo = open(f'data/{nome}', 'r')
    conteudo = json.load(arquivo)
    arquivo.close()
    return conteudo

def load_template(nome):
    arquivo = open(f'templates/{nome}', 'r')
    conteudo = arquivo.read()
    arquivo.close()
    return conteudo

def add_note(dicionario):
    conteudo = load_data('notes.json')
    conteudo.append(dicionario)
    arquivo = open(f'data/notes.json', 'w')
    json.dump(conteudo, arquivo)
    arquivo.close()

def build_response(body='', code=200, reason='OK', headers=''):
    response = f'HTTP/1.1 {code} {reason}\n'

    if headers:
        response += headers + '\n'

    response += '\n'
    response += body

    return response.encode()