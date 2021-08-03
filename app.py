from flask import Flask, render_template, request, flash
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy

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

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ydkfcsxx:N1pAH-ujCc1W45VA3ldvkk-RkrYMyNjk@kesavan.db.elephantsql.com/ydkfcsxx'
db = SQLAlchemy(app)

class Contato:
    def __init__(self, nome, email, mensagem):
        self.nome = nome
        self.email = email
        self.mensagem = mensagem
class Projeto(db.model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(150), nullable=False)
    imagem = db.Column(db.string(500), nullable=False)
    descricao = db.Column(db.String(500), nullable=False)
    link = db.Column(db.String(300), nullable=False)

    def __init__(self, nome, imagem, descricao, link):
        self.nome = nome
        self.imagem = imagem
        self.descricao = descricao
        self.link = link


@app.route('/')
def index():
    projetos = Projeto.query.all()

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

@app.route('/new',methods=['GET','POST'])
def new():
    if request.method == 'POST':
        projeto = Projeto(
            request.form['nome'],
            request.form['imagem'],
            request.form['descricao'],
            request.form['link']
        )
        db.session.add(projeto)
        db.session.commit()
        flash('Projeto criado com sucesso!')
        return redirect('/adm')
        
if __name__ == '__main__':
    app.run(debug=True)

        
