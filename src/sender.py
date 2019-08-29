import io
#import magic
import split_proteins
import zipfile
import find_entries_diso
from app import app
from flask import flash, request, redirect, render_template, send_file
from flask_mail import Mail, Message

ALLOWED_FASTA_EXTENSIONS = set([
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

    if (extension == ('multifasta') or
        extension == ('multi-fasta') or
        extension == ('fasta')):

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
        op = request.form['file_option']
        if op == 'op_fasta':
            final_words = extension(file.filename)
        else:
            final_words = 'diso'
        raw_name = file.filename.replace('.' + final_words, '')

        if file.filename == '':
            flash('Selecione um arquivo!')
            return redirect(request.url)
        if file and final_words in ALLOWED_FASTA_EXTENSIONS:
            mail_subject = ("Nova submissão - Arquivo fasta - " +
                            file.filename
                            )

            mail_body = (
                "Arquivo .fasta submetido por " +
                name +
                "\nEmail: " +
                email +
                "\nNúmero de núcleos solicitado: " +
                str(number)
            )

            msg = Message(
                subject=mail_subject,
                sender=app.config.get("MAIL_USERNAME"),
                recipients=[app.config.get("MAIL_USERNAME")],
                body=mail_body
                )

            wrapper = io.TextIOWrapper(file)

            splitted_files = split_proteins.names(raw_name, wrapper, number)

            for item in splitted_files:

                f = open(item.name, 'r')

                msg.attach(
                    item.name,
                    'application/octect-stream',
                    f.read()
                )

                f.close()

            try:
                mail.send(msg)
            except:
                zipped_files = zipfile.ZipFile('Arquivos Fasta.zip','w', zipfile.ZIP_DEFLATED)
                for item in splitted_files:
                    zipped_files.write(item.name)
                zipped_files.close()
                return send_file('Arquivos Fasta.zip',
                        mimetype = 'zip',
                        attachment_filename= 'Arquivos Fasta.zip',
                        as_attachment = True)

            flash('Arquivo enviado com sucesso!')
            return redirect('/')
        elif file and final_words == 'diso':
            wrapper = io.TextIOWrapper(file)
            txt_file = find_entries_diso.main(raw_name, wrapper)
            return send_file(raw_name + '.txt',
                    attachment_filename= 'Result-' + raw_name + '.txt',
                    as_attachment = True)

        else:
            flash("Você deve introduzir apenas arquivos 'faa', 'fasta', 'fna', 'ffn', 'frn', 'multifasta' ou 'multi-fasta'")
            return redirect(request.url)

if __name__ == "__main__":
    app.run()
