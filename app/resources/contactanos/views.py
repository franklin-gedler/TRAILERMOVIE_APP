
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.modules.form import Contactanos
from app.modules.sendmail import SendEmail

contactanos = Blueprint("contactanos", __name__)
####

@contactanos.route("/contactanos", methods=['GET', 'POST'])
def main():
    form = Contactanos()
    if request.method == 'POST' and form.validate():
        try:
            resp = SendEmail().send_email({
                'nombre': form.clientname.data,
                'email_user': form.email.data,
                'mensaje': form.comment.data,
            })
            
            flash(*resp)

            form.process() # Limpia el form

            return redirect(url_for('contactanos.main'))

        except Exception as err:
            flash(err, 'error')

    return render_template('contactanos.html', title='Contactanos', form=form)