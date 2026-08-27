from urllib.parse import unquote_plus

from utils import add_note, build_response, load_data, load_template, delete_note, get_note, update_note

def index(request):
    if request.startswith('POST'):
        request = request.replace('\r', '')
        partes = request.split('\n\n')
        corpo = partes[1]
        params = {}
        for chave_valor in corpo.split('&'):
            chave, valor = chave_valor.split('=')
            params[chave] = unquote_plus(valor)

        add_note(params)

        return build_response(
            code=303,
            reason='See Other',
            headers='Location: /'
        )

    note_template = load_template('components/note.html')
    notes_li = [
        note_template.format(id=dados.id, title=dados.title, details=dados.content)
        for dados in load_data()
    ]
    notes = '\n'.join(notes_li)

    return build_response(
            body=load_template('index.html').format(notes=notes)
        )

def edit(request, note_id):
    if request.startswith('POST'):
        request = request.replace('\r', '')
        partes = request.split('\n\n')
        corpo = partes[1]
        params = {}
        for chave_valor in corpo.split('&'):
            chave, valor = chave_valor.split('=')
            params[chave] = unquote_plus(valor)

        update_note(note_id, params)

        return build_response(
            code=303,
            reason='See Other',
            headers='Location: /'
        )

    note = get_note(note_id)

    return build_response(
        body=load_template('edit.html').format(
            id=note.id,
            title=note.title,
            content=note.content
        )
    )

def confirm_delete(note_id):
    note = get_note(note_id)

    if note is None:
        return build_response(
            body=load_template('404.html'),
            code=404,
            reason='Not Found'
        )

    return build_response(
        body=load_template('confirmar-exclusao.html').format(
            id=note.id,
            title=note.title,
            details=note.content
        )
    )

    # O RESTO DO CÓDIGO DA FUNÇÃO index CONTINUA DAQUI PARA BAIXO...
    # Cria uma lista de <li>'s para cada anotação
    # Se tiver curiosidade: https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions
    note_template = load_template('components/note.html')
    notes_li = [
        note_template.format(id=dados.id, title=dados.title, details=dados.content)
        for dados in load_data()
    ]
    notes = '\n'.join(notes_li)

    return build_response(
            body=load_template('index.html').format(notes=notes)
        )