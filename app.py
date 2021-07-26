from flask import Flask, render_template, request
from flask_mail import Mail, Message

app = Flask(__name__)

mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": 'kwaibotelho@gmail.com',
    "MAIL_PASSWORD": 'senhanova123'
}
app.config.update(mail_settings)
mail = Mail(app)
class Contato:
    def __init__(self, nome, email, mensagem):
        self.nome = nome
        self.email = email
        self.mensagem = mensagem
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/send', methods=['GET', 'POST'])
def send():
    if request.method == 'POST':
        contactForm = Contato(
            request.form['nome'],
            request.form['email'],
            request.form['mensagem']
        )
        msg = Message(
            subject='Contato portfólio',
            sender=app.config.get("MAIL_USERNAME"),
            recipients=[app.config.get("MAIL_USERNAME")],
            body=f'''
            O {contactForm.nome} com o e-mail {contactForm.email}, enviou a seguinte mensagem:
            
            {contactForm.mensagem}'''         
        )
        mail.send(msg) 
    return render_template('send.html', contact=contactForm)
if __name__ == '__main__':
    app.run(debug=True)

        
