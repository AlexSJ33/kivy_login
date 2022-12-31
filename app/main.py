#!/usr/bin/env python3
#---------------------------------------------------------#
# Sistema MiniGestão - C.R.U.D
# Ferramentas: Python, Kivy, SQLite
# Versão: 1.0.0
#---------------------------------------------------------#
# Desenvolvedor..: Alex S Jesus <alevildark@gmail.com>
# Data...........: 04.12.2022 <dd/mm/yyy> 
#---------------------------------------------------------#

from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen,ScreenManager
from kivymd.uix.card import MDCard
from kivymd.uix.list import OneLineListItem
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from database import ConectaBanco
from kivy.core.window import Window
Window.size = (350, 580)

global tela
global autenticado
tela = ScreenManager()
autenticado = []


class Inicio(Screen):
    pass

class Menu(Screen):

    def on_enter(self):
        name = autenticado[0]
        self.ids.label_menu.text = 'Olá ' + str(name)

class GestaoUsuario(Screen):
    def cad_usuario(self):
        self.add_widget(CadastrarUsuario())
    
    def exibir_dados(self):
        self.add_widget(ListarUsuarios())           
    

class GestaoCliente(Screen):
    def cad_cliente(self):
        self.add_widget(CadastrarCliente())


class Login(Screen):

    def login(self):
        campo_user = self.ids.username.text
        campo_password = self.ids.password.text

        self.username = "".join(campo_user.split())
        self.password = "".join(campo_password.split())

        if self.username == '' or self.password.strip() == '':
            self.dialog = MDDialog(
                text="[color=#f9f9f9]Preencha todos os campos ![/color]",
                md_bg_color='3c3c3c',
                )
            self.dialog.open()
            
        else:
            return self.username,self.password

    def valida_login(self):
        lista = c.listar_dados()
        for users in lista:

            if self.username == '' or self.password == '':
                self.ids.label_login.text = ' '

            elif self.username == users[1] and self.password == users[3]:
                print(self.username)
                self.ids.label_login.text = 'Login Accept !!'
                self.ids.label_login.text_color= 'green'
                MDApp.get_running_app().root.current = 'menu'
                autenticado.append(self.username)
                break
                
            else:
                self.ids.label_login.text = 'Login Incorrect !!'
                self.ids.label_login.text_color = 'red'
    
class CadastrarCliente(MDCard):

    def fechar(self):
        self.parent.remove_widget(self)   

class CadastrarUsuario(MDCard):
    dialog = None    
    def pega_valor(self):
        usuario = self.ids.usuario.text
        usuario = "".join(usuario.split())
        email = self.ids.email.text
        email = "".join(email.split())
        senha = self.ids.senha.text
        senha = "".join(senha.split())
        re_senha = self.ids.re_senha.text
        re_senha = "".join(re_senha.split())
        data = (usuario,email,senha)
        
        if usuario == '' or email.strip() == '' or senha.strip() == '' or re_senha.strip() == '':
            self.dialog = MDDialog(
                text="[color=#f9f9f9]Preencha todos os campos ![/color]",
                md_bg_color='3c3c3c',
                )
            self.dialog.open()
            
        else:
            self.dialog = MDDialog(
                text="[color=#f9f9f9]Dados gravados com sucesso![/color]",
                md_bg_color='3c3c3c',
                )
        
            self.dialog.open()
            
            
            return c.inserir_dados(data)

    def fechar(self):
        self.parent.remove_widget(self)   

    def limpar_text(self):
        self.ids.usuario.text = ''
        self.ids.email.text = ''
        self.ids.senha.text = ''
        self.ids.re_senha.text = ''

class ListarUsuarios(MDCard):
    def on_enter(self):
        lista = c.listar_dados()
        for users in lista:
                    self.ids['box'].add_widget(
                        OneLineListItem(
                            text=f"{users[0]:>4} {users[1]}",
                        )
                    )
    
    def fechar(self):
        self.parent.remove_widget(self)     

class ListUser(MDCard):

    def exibir_dados(self):
        lista = c.listar_dados()
        for users in lista:
                    self.ids['box'].add_widget(
                        MDLabel(
                            text=f"{users[1]}",
                            halign="left",
                            
                            adaptive_height=True,
                        )
                    )

    
    def fechar(self):
        self.parent.remove_widget(self)   

# class Account(Screen,ConectaBanco):
    dialog = None    
    def pega_valor(self):
        username = self.ids.username.text
        username = "".join(username.split())
        email = self.ids.email.text
        email = "".join(email.split())
        password = self.ids.password.text
        password = "".join(password.split())
        password_2 = self.ids.password_2.text
        password_2 = "".join(password_2.split())
        data = (username,email,password)
        
        if username == '' or email.strip() == '' or password.strip() == '' or password_2.strip() == '':
            self.dialog = MDDialog(
                text="[color=#f9f9f9]Preencha todos os campos ![/color]",
                md_bg_color='3c3c3c',
                )
            self.dialog.open()
            
        else:
            self.dialog = MDDialog(
                text="[color=#f9f9f9]Dados gravados com sucesso![/color]",
                md_bg_color='3c3c3c',
                )
        
            self.dialog.open()

            
            return c.inserir_dados(data)



    def abrir_card(self):
        self.add_widget(ListUser())

tela.add_widget(Inicio(name='inicio'))
tela.add_widget(Login(name='login'))
tela.add_widget(Menu(name='menu'))
#tela.add_widget(Account(name='account'))


c=ConectaBanco()
c.connect()
c.create_table()
c.listar_dados()

class MyApp(MDApp):

    def build(self):
        kv = Builder.load_file('app.kv')
        tela = kv
        #self.theme_cls.primary_palette = 'Purple'
        #self.theme_cls.theme_style = 'Dark'
        return tela


if __name__=='__main__':
    MyApp().run()
