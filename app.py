from flask import Flask, render_template, request, flash, redirect, session
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.secret_key = 'senha'
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
#  classes 
class Contato:
    def __init__(self, nome, email, mensagem):
        self.nome = nome
        self.email = email
        self.mensagem = mensagem

class Projeto(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(150), nullable=False)
    imagem = db.Column(db.String(500), nullable=False)
    descricao = db.Column(db.String(500), nullable=False)
    link = db.Column(db.String(300), nullable=False)

    def __init__(self, nome, imagem, descricao, link):
        self.nome = nome
        self.imagem = imagem
        self.descricao = descricao
        self.link = link

# rota principal
@app.route('/')
def index():
    session['usuario_logado'] = None
    projeto = Projeto.query.all()
    return render_template('index.html' , projeto=projeto)

# Rota para enviar o email
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

# Rotas de login
@app.route('/login')
def login():
    session['usuario_logado'] = None
    return render_template('login.html')

@app.route('/auth' , methods=['GET', 'POST'])
def auth():
    if request.form['senha'] == 'admin':
        session['usuario_logado'] = 'admin' # Adiciona um usuario na sessão
        flash('Login feito com sucesso!') # Envia mensagem de sucesso
        return redirect('/adm') # Redireciona para a rota adm
    else:
        flash('Erro no login, tente novamente!')  # Envia mensagem de erro
        return redirect('/login')
    

@app.route('/adm')
def adm():
   if 'usuario_logado' not in session or session['usuario_logado'] == None:
      flash('Faça o login antes de entrar nessa rota!') # Mensagem de erro
      return redirect('/login') # Redireciona para o login
   projetos = Projeto.query.all() # Busca todos os projetos no banco e coloca na veriável projetos, que se transforma em uma lista.
   return render_template('adm.html', projetos=projetos)


@app.route('/new', methods=['GET','POST'])
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

@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
   projeto = Projeto.query.get(id) 
   projetos = Projeto.query.all()
   if request.method == "POST": # 
      projeto.nome = request.form['nome']
      projeto.descricao = request.form['descricao']
      projeto.imagem = request.form['imagem']
      projeto.link = request.form['link']
      db.session.commit()
      return redirect('/adm') 
   return render_template('adm.html', projeto=projeto, projetos=projetos) 

  #crud delete
@app.route('/delete/<id>')
def delete(id):
    projeto = Projeto.query.get(id)
    db.session.delete(projeto)
    db.session.commit()
    return redirect('/adm')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

        
