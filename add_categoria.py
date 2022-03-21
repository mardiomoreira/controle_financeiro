from tkinter import*
from tkinter.messagebox import showinfo
from tkinter.ttk import Combobox, Treeview
import sqlite3

class APP():
    def __init__(self):
        self.conectarBD()
        self.tela()
        self.componentes()
        self.COMBOBOX_tipo.delete(0,END)
        self.popularTREEVIEW()
        self.janela.mainloop()
    def tela(self):
        self.janela = Tk()
        self.janela.title('Cadastro de Categoria - Controle Financeiro')
        self.largura = 400
        self.altura = 300
        self.largura_screen = self.janela.winfo_screenwidth()
        self.altura_screen = self.janela.winfo_screenheight()
        self.posX = self.largura_screen/2 - self.largura/2
        self.posY = self.altura_screen/2 - self.altura/2
        self.janela.geometry("%dx%d+%d+%d" % (self.largura, self.altura, self.posX, self.posY))
        self.janela.configure(bg='#B0E0E6')
        # Não permitir Redimensionamento
        self.janela.resizable(width=0,height=0)
    def componentes(self):
        ### ROTULOS ###
        self.ROTULO_titulo = Label(self.janela,text='Cadastro de Categoria',font=('Ivy',18, 'bold'),bg='red')
        self.ROTULO_titulo.place(x=0,y=0, width=self.largura)
        self.ROTULO_tipo = Label(self.janela,text='Tipo: ',font=('Ivy',12,'italic'),bg='#B0E0E6')
        self.ROTULO_tipo.place(x=10,y=40)
        self.ROTULO_descricao = Label(self.janela,text='Descrição: ',font=('Ivy',12,'italic'),bg='#B0E0E6')
        self.ROTULO_descricao.place(x=10,y=80)
        ### ComboBox ###
        self.COMBOBOX_tipo = Combobox(self.janela, values=['RENDA','DESPESA'],justify='center')
        self.COMBOBOX_tipo.place(x=55,y=42)
        ### ENTRADAS ###
        self.ENTRADAS_descricao = Entry(self.janela, justify='center')
        self.ENTRADAS_descricao.place(x=92,y=82, width=(self.largura)-190)
        ### BOTAO ###
        self.BOTOES_cadastrar = Button(self.janela,text='Cadastrar', activebackground='red', activeforeground='white',font=('Ivy',11,'bold'),command=self.add_categoria)
        self.BOTOES_cadastrar.place(x=310,y=78)
        ### TREEVIEW ###
        self.columns = ('col01', 'col02', 'col03')
        self.tv = Treeview(self.janela, columns=self.columns, show='headings')
        # definindo Títulos
        self.tv.heading('col01', text='ID', anchor='center')
        self.tv.heading('col02', text='Tipo', anchor='center')
        self.tv.heading('col03', text='Descrição', anchor='center')
        # Configurando tamanho de Cada Coluna
        self.tv.column('col01',width=30,minwidth=30,anchor='center')
        self.tv.column('col02',width=30,minwidth=30,anchor='center')
        self.tv.column('col03',width=30,minwidth=30,anchor='center')
        # add a scrollbar
        self.TV_altura = 190
        self.scrollbar = Scrollbar(self.janela, orient=VERTICAL, command=self.tv.yview)
        self.tv.configure(yscroll=self.scrollbar.set)
        # Posicionando
        self.tv.place(x=1,y=120, width=(self.largura)-30,height=self.TV_altura)
        self.scrollbar.place(x=(self.largura)-30,y=120,height=self.TV_altura)
    def conectarBD(self):
        self.conn = sqlite3.connect("financeiro.db3")
        self.cursor = self.conn.cursor()
    def desconectar_bd(self):
        self.conn.close()
    def add_categoria(self):
        if (self.COMBOBOX_tipo.get() == '') or (self.ENTRADAS_descricao.get() == ''):
            showinfo('Campos Obrigatórios', 'Todos os campos são obrigatórios!!!')
        else:
            self.tipo = self.COMBOBOX_tipo.get()
            self.descricao = self.ENTRADAS_descricao.get()
            self.conectarBD()
            self.cursor.execute("""INSERT INTO tbl_categoria (tipo_cat, descri_cat) VALUES (?,?)""",(self.tipo,self.descricao))
            self.conn.commit()
            self.popularTREEVIEW()            
            showinfo('Cadastro','Cadastro Realizado com Sucesso!!!')
            

    def popularTREEVIEW(self):
        for i in self.tv.get_children():
            self.tv.delete(i)
        self.conectarBD
        self.cursor.execute('select id_cat,tipo_cat,descri_cat FROM tbl_categoria;')
        self.rows = self.cursor.fetchall()
        for (id,tipo,descricao) in self.rows:
            self.tv.insert('',END,values=(id,tipo,descricao))
        self.desconectar_bd()

APP()
