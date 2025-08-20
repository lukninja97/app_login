import flet as ft
import requests
from flet import AppBar, Text, View
from flet.core.colors import Colors
from flet.core.icons import Icons
from flet.core.types import FontWeight, CrossAxisAlignment
from api.routes import *


def main(page: ft.Page):
    # Configurações
    page.title = "Exemplo de Login"
    page.theme_mode = ft.ThemeMode.LIGHT  # ou ft.ThemeMode.DARK
    page.window.width = 375
    page.window.height = 667

    # Funções

    def click_salvar(e):
        token = page.client_storage.get("auth_token")
        if token is None:
            page.go("/login")

        nome = input_nome.value
        email = input_email.value
        senha = input_senha.value
        papel = input_papel.value

        #Verifica se foi preenchido
        if nome and email and senha and papel:

            # Feedback de carregamento
            btn_salvar.disabled = True
            btn_salvar.text = "Salvando..."
            loading_indicator.visible = True

            btn_salvar.opacity = 0.5
            input_nome.opacity = 0.5
            input_email.opacity = 0.5
            input_senha.opacity = 0.5
            input_papel.opacity = 0.5

            page.update()

            #chama a API
            resposta = post_usuarios(nome, email, senha, papel, token)
            if resposta == 201:
                snack_sucesso("Usuário cadastrado com sucesso.")

                input_nome.value = ""
                input_email.value = ""
                input_senha.value = ""
                input_papel.value = ""
            else:
                print(resposta)
                snack_error("Erro ao cadastrar usuário")

            # Restaurar Componentes
            btn_salvar.disabled = False
            btn_salvar.text = "Salvar"
            loading_indicator.visible = False
            btn_salvar.opacity = 1
            input_nome.opacity = 1
            input_email.opacity = 1
            input_senha.opacity = 1
            input_papel.opacity = 1

            page.update()

    def click_login(e):
        # Limpa erros anteriores
        input_email.error_text = None
        input_senha.error_text = None

        # Validação de campos
        is_valid = True
        if not input_email.value:
            input_email.error_text = "O campo e-mail é obrigatório."
            is_valid = False

        if not input_senha.value:
            input_senha.error_text = "O campo senha é obrigatório."
            is_valid = False

        if not is_valid:
            page.update()
            return

        # Feedback de carregamento
        btn_login.disabled = True
        btn_login.text = "Entrando..."
        loading_indicator.visible = True
        spacing.visible = True

        btn_login.opacity = 0.5
        input_email.opacity = 0.5
        input_senha.opacity = 0.5

        page.update()

        # Chamar a rota da API
        dados = post_login(input_email.value, input_senha.value)

        # Lógica de "autenticação"
        if "access_token" in dados:

            page.client_storage.set("auth_token", dados["access_token"])
            page.client_storage.set("papel", dados["papel"])

            # Feedback de sucesso
            snack_sucesso("Login realizado com sucesso!")

            input_email.value = ""
            input_senha.value = ""

            page.go("/usuarios")

        else:
            # Feedback de erro
            snack_error("Credenciais inválidas")

        # Restaura o estado dos componentes
        btn_login.disabled = False
        btn_login.text = "Login"
        loading_indicator.visible = False
        spacing.visible = False
        btn_login.opacity = 1
        input_email.opacity = 1
        input_senha.opacity = 1

        page.update()

    def click_logout(e):
        page.client_storage.remove("auth_token")
        page.snack_bar = ft.SnackBar(content=ft.Text("Você foi desconectado."))
        page.snack_bar.open = True
        page.go("/login")
        page.update()

    def snack_sucesso(texto: str):
        page.snack_bar = ft.SnackBar(
            content=ft.Text(texto),
            bgcolor=Colors.GREEN_700
        )
        page.snack_bar.open = True
        page.overlay.append(page.snack_bar)

    def snack_error(texto: str):
        page.snack_bar = ft.SnackBar(
            content=ft.Text(texto),
            bgcolor=Colors.RED_700
        )
        page.snack_bar.open = True
        page.overlay.append(page.snack_bar)

    def atualizar_lista():
        token = page.client_storage.get("auth_token")
        if token is None:
            page.go("/login")

        lv_usuarios.controls.clear()
        usuarios = get_usuarios(token)
        print(usuarios)
        for usuario in usuarios:
            lv_usuarios.controls.append(
                ft.ListTile(
                    title=ft.Text(usuario["nome"]),
                    subtitle=ft.Text(usuario["email"]),
                    leading=ft.Icon(Icons.API) if usuario["papel"] == "admin" else ft.Icon(Icons.PERSON),
                )
            )
        page.update()

    def gerencia_rotas(e):

        # input_email.value = "lucas@"
        # input_senha.value = "123"

        page.views.clear()
        page.views.append(
            View(
                "/login",
                [
                    ft.Column(
                        [
                            ft.Text("Bem-vindo à Biblioteca", size=24, weight=ft.FontWeight.BOLD),
                            ft.Container(height=10),  # Espaçamento
                            input_email,
                            input_senha,
                            ft.Container(height=10),  # Espaçamento
                            loading_indicator,
                            spacing,
                            btn_login,
                        ],
                        # Alinha a coluna de login no centro horizontal da página
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        height=page.window.height,
                        alignment=ft.MainAxisAlignment.CENTER,
                    )
                ]
            )
        )

        if page.route == "/usuarios":
            # Somente o admin pode adicionar novos usuarios
            fab_add_usuario.visible = page.client_storage.get("papel") == "admin"
            atualizar_lista()

            page.views.append(
                View(
                    "/",
                    [
                        AppBar(title=Text("Usuarios"), center_title=True, bgcolor=Colors.PRIMARY_CONTAINER,
                               leading=ft.Icon(), actions=[btn_logout]),
                        lv_usuarios
                    ],
                    floating_action_button=fab_add_usuario,
                    horizontal_alignment=ft.CrossAxisAlignment.END,
                    scroll=ft.ScrollMode.HIDDEN,
                )
            )

        if page.route == "/add_usuario":
            page.views.append(
                View(
                    "/add_usuario",
                    [
                        AppBar(title=Text("Novo Usuario"), center_title=True, bgcolor=Colors.PRIMARY_CONTAINER,
                               leading=ft.Icon(), actions=[btn_logout]),
                        input_nome,
                        input_email,
                        input_senha,
                        input_papel,
                        btn_salvar,
                        btn_cancelar,
                        loading_indicator
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            )

        # verifica_usuario_conectado()
        page.update()

    # Componentes

    fab_add_usuario = ft.FloatingActionButton(
        icon=Icons.ADD,
        on_click= lambda _: page.go("/add_usuario")
    )

    lv_usuarios = ft.ListView(expand=True)

    input_email = ft.TextField(
        label="E-mail",
        width=300,
        prefix_icon=Icons.EMAIL_OUTLINED,
        keyboard_type=ft.KeyboardType.EMAIL,
        autofocus=True,
    )

    # Campo de Senha
    input_senha = ft.TextField(
        label="Senha",
        width=300,
        password=True,
        can_reveal_password=True,  # Ícone para mostrar/ocultar senha
        prefix_icon=Icons.LOCK_OUTLINE,
    )

    input_nome = ft.TextField(
        label="Nome",
        width=300,
        prefix_icon=Icons.PERSON,
    )

    input_papel = ft.TextField(
        label="Papel",
        width=300,
        prefix_icon=Icons.SECURITY,
    )

    # Indicador de carregamento
    loading_indicator = ft.ProgressRing(visible=False, width=20, height=20, stroke_width=2)

    spacing = ft.Container(visible=False, height=10)

    # Botão de Login
    btn_login = ft.ElevatedButton(
        text="Login",
        icon=Icons.LOGIN,
        width=300,
        height=45,
        on_click=click_login,
    )

    btn_logout = ft.TextButton(
        icon=Icons.LOGOUT,
        on_click=click_logout,
        scale=1.5,
        icon_color=Colors.RED_700
    )

    btn_salvar = ft.FilledButton(
        text="Salvar",
        style=ft.ButtonStyle(text_style=ft.TextStyle(size=16)),
        on_click=click_salvar,
        width=page.window.width,
        height=45,
    )

    btn_cancelar = ft.OutlinedButton(
        text="Cancelar",
        style=ft.ButtonStyle(text_style=ft.TextStyle(size=16)),
        width=page.window.width,
        on_click= lambda _: page.go("/usuarios"),
        height=45,
    )

    # Eventos
    page.on_route_change = gerencia_rotas
    page.on_close = page.client_storage.remove("auth_token")
    page.go(page.route)


# Comando que executa o aplicativo
# Deve estar sempre colado na linha
ft.app(main)
