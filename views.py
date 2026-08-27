from urllib.parse import unquote_plus

from database import Database, Note
from utils import build_response, load_template


def _parse_form_body(request):
    request = request.replace('\r', '')
    partes = request.split('\n\n')
    corpo = partes[1]
    params = {}
    for chave_valor in corpo.split('&'):
        chave, valor = chave_valor.split('=')
        params[chave] = unquote_plus(valor)
    return params


def index(request):
    erro = None

    if request.startswith('POST'):
        params = _parse_form_body(request)
        titulo = params.get('titulo', '').strip()
        detalhes = params.get('detalhes', '').strip()

        if not titulo or not detalhes:
            erro = 'Título e conteúdo são obrigatórios para criar uma anotação.'
        else:
            database = Database('notes')
            database.add(Note(title=titulo, content=detalhes))

            return build_response(
                code=303,
                reason='See Other',
                headers='Location: /'
            )

    database = Database('notes')
    note_template = load_template('components/note.html')
    notes_li = [
        note_template.format(
            id=dados.id,
            title=dados.title,
            details=dados.content,
            favorite_label='★' if dados.favorite else '☆'
        )
        for dados in database.get_all()
    ]
    notes = '\n'.join(notes_li)

    erro_html = f'<p class="form-error">{erro}</p>' if erro else ''

    return build_response(
        body=load_template('index.html').format(notes=notes, erro=erro_html)
    )


def edit(request, note_id):
    database = Database('notes')

    if request.startswith('POST'):
        params = _parse_form_body(request)
        titulo = params.get('titulo', '').strip()
        detalhes = params.get('detalhes', '').strip()

        if not titulo or not detalhes:
            note = database.get_by_id(note_id)
            erro_html = '<p class="form-error">Título e conteúdo são obrigatórios.</p>'
            return build_response(
                body=load_template('edit.html').format(
                    id=note.id,
                    title=titulo or note.title,
                    content=detalhes or note.content,
                    erro=erro_html
                )
            )

        database.update(Note(id=note_id, title=titulo, content=detalhes))

        return build_response(
            code=303,
            reason='See Other',
            headers='Location: /'
        )

    note = database.get_by_id(note_id)

    if note is None:
        return not_found()

    return build_response(
        body=load_template('edit.html').format(
            id=note.id,
            title=note.title,
            content=note.content,
            erro=''
        )
    )


def confirm_delete(request, note_id):
    database = Database('notes')
    note = database.get_by_id(note_id)

    if note is None:
        return not_found()

    return build_response(
        body=load_template('confirmar-exclusao.html').format(
            id=note.id,
            title=note.title,
            details=note.content
        )
    )


def delete(request, note_id):
    database = Database('notes')
    database.delete(note_id)

    return build_response(
        code=303,
        reason='See Other',
        headers='Location: /'
    )


def favorite(request, note_id):
    database = Database('notes')
    database.toggle_favorite(note_id)

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