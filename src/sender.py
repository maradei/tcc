import io
#import magic
import split_proteins
from app import app
from flask import Flask, flash, request, redirect, render_template
from flask_mail import Mail, Message

ALLOWED_EXTENSIONS = set([
    'faa',
    'fasta',
    'fna',
    'ffn',
    'frn',
    'multifasta',
    'multi-fasta'])

mail = Mail(app)

def extension(filename):

    extension = filename.rsplit('.')
    extension = extension[-1].lower()

    if extension == ('multifasta') or extension == ('multi-fasta') or extension == ('fasta'):
        extension = 'faa'

    return extension

@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('Arquivo não reconhecido')
            return redirect(request.url)
        file = request.files['file']
        name = request.form['name']
        email = request.form['email']
        number = int(request.form['number'])
        final_words = extension(file.filename)
        raw_name = file.filename.replace('.' + final_words, '')

        if file.filename == '':
            flash('Selecione um arquivo!')
            return redirect(request.url)
        if file and final_words in ALLOWED_EXTENSIONS:
            mail_subject = ("Nova submissão - Arquivo fasta - " +
                file.filename
                )

            mail_body = (
                "Arquivo .fasta submetido por " +
                name +
                "\nEmail: " +
                email +
                "\nNúmero de clusters solicitado: " +
                str(number)
            )

            msg = Message(
                subject=mail_subject,
                sender=app.config.get("MAIL_USERNAME"),
                recipients=[app.config.get("MAIL_USERNAME")],
                body=mail_body
                )

            # print ('\n\nFILE = \n\n', file)
            # print ('\n\nTYPE = \n\n', type(file))
            # print ('\n\nSTREAM = \n\n', file.stream)

            wrapper = io.TextIOWrapper(file)

            # print ('\n\nTYPE = \n\n', type(wrapper))

            splitted_files = split_proteins.names(raw_name, wrapper, number)

            # print ('\n\nFILE = \n\n', splitted_files)
            # print ('\n\nTYPE = \n\n', type(splitted_files))

            for item in splitted_files:

                f = open(item.name, 'r')

                msg.attach(
                    item.name,
                    'application/octect-stream',
                    f.read()
                )

                f.close()

            mail.send(msg)

            flash('Arquivo enviado com sucesso!')
            return redirect('/')
        else:
            flash("Você deve introduzir apenas arquivos 'faa', 'fasta', 'fna', 'ffn', 'frn', 'multifasta' ou 'multi-fasta'")
            return redirect(request.url)

if __name__ == "__main__":
    app.run()
