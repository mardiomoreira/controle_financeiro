import locale
from tkinter import*
from tkinter.messagebox import showinfo
from tkinter.ttk import Combobox, Treeview, Scrollbar
from tkcalendar import DateEntry
import sqlite3

class FUNCOES():
    def conectarBD(self):
        self.conn = sqlite3.connect("financeiro.db3")
        self.cursor = self.conn.cursor()
    def desconectar_bd(self):
        self.conn.close()
    def criarTabelas(self):
        self.conectarBD(); print("Conectando ao Banco de Dados!!!")
        ### Criar tabela
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS tbl_categoria (
                                id_cat           INTEGER      PRIMARY KEY AUTOINCREMENT NOT NULL,
                                tipo_cat         VARCHAR (7)  NOT NULL,
                                descri_cat       VARCHAR (50) NOT NULL,
                                datacadastro_cat DATE         DEFAULT (CURRENT_DATE) 
                                    );
                        """)
        self.conn.commit();print("Banco de dados criado!!!")
        self.desconectar_bd();print("Banco de Dados desconectado")
    def criar_tbl_movimentacao(self):
        self.conectarBD()
        ## Criar a tabela
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS tbl_movimentacao (
                                id_mov          INTEGER      PRIMARY KEY AUTOINCREMENT
                                                            NOT NULL,
                                fk_categoria_id              REFERENCES tbl_categoria (id_cat) ON DELETE RESTRICT
                                                            NOT NULL,
                                mov_descricao   VARCHAR (40),
                                mov_data        DATE,
                                mov_valor       DECIMAL
                                    );
                        """)
        self.conn.commit();print("tabela Movimentacao Criada com Sucesso")
        self.desconectar_bd();print("Banco de Dados desconectado")
    def criar_view_movimentacao(self):
        self.conectarBD()
        self.cursor.execute(""" CREATE VIEW IF NOT EXISTS vw_movimentacao 
                            AS SELECT * FROM tbl_movimentacao INNER JOIN 
                            tbl_categoria ON tbl_categoria.id_cat = tbl_movimentacao.fk_categoria_id; """)
        self.conn.commit();print("View Movimentação criado com sucesso!!!")
    def combo_categoria(self):
        self.dictCOMBO = {}
        self.listaCOMBO = []
        ### COMBO ###
        self.COMBOBOX_categoria = Combobox(self.janela)
        self.COMBOBOX_categoria.place(x=75,y=70)
        self.conectarBD()
        self.cur = self.conn.cursor()
        self.cur.execute('SELECT id_cat,descri_cat FROM tbl_categoria;')
        self.rows = self.cur.fetchall()
        for i in self.rows:
            self.dictCOMBO[i[1]]= i[0]
            self.listaCOMBO.append(i[1])
        self.COMBOBOX_categoria['values'] = self.listaCOMBO
        


class APP(FUNCOES):
    def __init__(self):
        self.conectarBD()
        self.criarTabelas()
        self.criar_tbl_movimentacao()
        self.criar_view_movimentacao()
        self.desconectar_bd()
        self.tela()
        self.componentes()
        self.combo_categoria()
        self.janela.mainloop()
    def tela(self):
        self.janela = Tk()
        self.janela.title('Controle Financeiro')
        self.largura = 700
        self.altura = 500
        self.largura_screen = self.janela.winfo_screenwidth()
        self.altura_screen = self.janela.winfo_screenheight()
        self.posX = self.largura_screen/2 - self.largura/2
        self.posY = self.altura_screen/2 - self.altura/2
        self.janela.geometry("%dx%d+%d+%d" % (self.largura, self.altura, self.posX, self.posY))
        self.janela.title("Controle Financeiro")
        self.janela.configure(bg='#B0E0E6')
        # Não permitir Redimensionamento
        self.janela.resizable(width=0,height=0)
    def componentes(self):
        ### RÓTULOS ###
        self.ROTULO_titulo = Label(self.janela,text='Cadastro de Movimentação',font=('Ivy',18, 'bold'),bg='red')
        self.ROTULO_titulo.place(x=0,y=0, width=self.largura)
        self.ROTULO_data = Label(self.janela, text='Data: ', font=('Ivy',10, 'bold'))
        self.ROTULO_data.place(x=1,y=40)
        self.ROTULO_data.configure(bg='#B0E0E6')
        self.ROTULO_descricao = Label(self.janela, text='Descrição: ', font=('Ivy',10, 'bold'),bg='#B0E0E6')
        self.ROTULO_descricao.place(x=180,y=40)
        self.ROTULO_categoria = Label(self.janela, text='Categoria: ', font=('Ivy',10, 'bold'),bg='#B0E0E6')
        self.ROTULO_categoria.place(x=1,y=70)
        self.ROTULO_valor = Label(self.janela, text='Valor: ', font=('Ivy',10, 'bold'),bg='#B0E0E6')
        self.ROTULO_valor.place(x=230,y=70)
        ### ENTRADA ###
        self.ENTRADA_data = DateEntry(self.janela,font=('Ivy',11),bg="darkblue",locale='pt_br')
        self.ENTRADA_data.configure(background='red', foreground='yellow')
        self.ENTRADA_data.place(x=45,y=40)
        self.ENTRADA_descricao = Entry(self.janela, justify='center')
        self.ENTRADA_descricao.place(x=255,y=40, width=430)
        self.ENTRADA_valor = Entry(self.janela, justify='center')
        self.ENTRADA_valor.place(x=275,y=70)
        ### BOTÕES ###
        self.BOTAO_cadastrar = Button(self.janela,text='Cadastrar',font=('Ivy',11,'bold'),command=self.cadastrar)
        self.BOTAO_cadastrar.place(x=410,y=66)
        self.BOTAO_limpar = Button(self.janela,text='Limpar',font=('Ivy',11,'bold','italic'),command=self.limpaCAMPOS)
        self.BOTAO_limpar.place(x=505,y=66)
        ### TREEVIEW
        self.columns = ('col01', 'col02', 'col03', 'col04', 'col05')
        self.tree = Treeview(self.janela, columns=self.columns, show='headings')
        # definindo Títulos
        self.tree.heading('col01', text='ID')
        self.tree.heading('col02', text='Descrição')
        self.tree.heading('col03', text='Categoria')
        self.tree.heading('col04', text='Data')
        self.tree.heading('col05', text='Valor')
        # add a scrollbar
        self.scrollbar = Scrollbar(self.janela, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)
        # Posicionando
        self.tree.place(x=1,y=120, width=self.largura-20, height=350)
        self.scrollbar.place(x=680,y=120,height=350)
    def limpaCAMPOS(self):
        self.ENTRADA_data.delete(0,END)
        self.ENTRADA_descricao.delete(0,END)
        self.ENTRADA_valor.delete(0,END)
        self.COMBOBOX_categoria.delete(0,END)
        self.ENTRADA_descricao.focus()
    def numeroREAL(self, valor):
        self.a = "{:,.2f}".format(float(valor))
        self.b = self.a.replace(',','v')
        self.c = self.b.replace('.',',')
        return self.c.replace('v','.')
    def cadastrar(self):
        if (self.ENTRADA_descricao.get() =='') or (self.ENTRADA_valor.get() =='') or (self.COMBOBOX_categoria.get() ==''):
            showinfo('Campos Obrigatórios','Todos os campos São Obrigatórios')
        else:
            self.CHAVE = self.COMBOBOX_categoria.get()
            self.DADOS_categoria = self.dictCOMBO[self.CHAVE]
            self.DADOS_data = self.ENTRADA_data.get_date()
            self.DADOS_descricao = self.ENTRADA_descricao.get()
            self.DADOS_valor = self.numeroREAL(self.ENTRADA_valor.get())
            self.conectarBD()
            self.cursor.execute(""" INSERT INTO tbl_movimentacao (
                                    fk_categoria_id, 
                                    mov_descricao, 
                                    mov_data, 
                                    mov_valor)  
                                    VALUES (?,?,?,?)""",(self.DADOS_categoria,self.DADOS_descricao,self.DADOS_data,self.DADOS_valor))
            self.conn.commit()
            self.desconectar_bd()
            self.limpaCAMPOS()
            showinfo('Cadastro','Cadastro Realizado com Sucesso!!!')



APP()