import flet as ft
from flet import AppBar, Text, View
from flet.core.colors import Colors
from flet.core.icons import Icons
from api.routes import *


def main(page: ft.Page):
    # Configurações
    page.title = "Exemplo de Login"
    page.theme_mode = ft.ThemeMode.LIGHT  # ou ft.ThemeMode.DARK
    page.window.width = 375
    page.window.height = 667

    # Funções
    def click_login(e):
        loading_indicator.visible = True
        page.update()

        dados = post_login(input_email.value, input_senha.value)

        if "access_token" in dados:
            snack_sucesso("Login realizado com sucesso!")

            page.client_storage.set("access_token", dados["access_token"])
            page.client_storage.set("papel", dados["papel"])

            input_email.value = ""
            input_senha.value = ""

            loading_indicator.visible = False
            page.go("/usuarios")

        else:
            snack_error("Email ou senha incorretos.")

    def click_logout(e):
        page.client_storage.remove("access_token")
        snack_sucesso("Logout realizado com sucesso!")
        page.go("/login")

    def click_salvar_usuario(e):
        nome = input_nome.value
        email = input_email.value
        senha = input_senha.value
        papel = input_papel.value

        if nome and email and senha and papel:
            loading_indicator.visible = True
            page.update()

            token = page.client_storage.get("access_token")

            response = post_usuario(nome, email, senha, papel, token)

            if response == 201:
                snack_sucesso("Usuario cadastrado com sucesso!")
                input_nome.value = ""
                input_email.value = ""
                input_senha.value = ""
                input_papel.value = ""
                page.update()
            else:
                snack_error("Erro ao cadastrar usuario")

            loading_indicator.visible = False
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
        #Pegar o token
        token = page.client_storage.get("access_token")
        lv_usuarios.controls.clear()

        #Chamar a API
        dados = get_usuarios(token)
        usuarios = dados["usuarios"]

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
                            ft.Container(height=page.window.height),  # Espaçamento
                            loading_indicator,
                            spacing,
                            btn_login,
                        ],
                        # Alinha a coluna de login no centro horizontal da página
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        height=page.window.height,
                        alignment=ft.MainAxisAlignment.CENTER,
                    )
                ],
            )
        )

        if page.route == "/usuarios":

            fab_add_usuario.visible = page.client_storage.get("papel") == "admin"

            atualizar_lista()

            page.views.append(
                View(
                    "/usuarios",
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

        page.update()

    # Componentes

    fab_add_usuario = ft.FloatingActionButton(
        icon=Icons.ADD,
        on_click= lambda _: page.go("/add_usuario")
    )

    lv_usuarios = ft.ListView(expand=True)

    # Campos
    input_email = ft.TextField(
        label="E-mail",
        width=300,
        prefix_icon=Icons.EMAIL_OUTLINED,
        keyboard_type=ft.KeyboardType.EMAIL,
        autofocus=True,
    )

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

    # Botões
    btn_login = ft.ElevatedButton(
        text="Login",
        icon=Icons.LOGIN,
        width=300,
        height=45,
        on_click=click_login
    )

    btn_logout = ft.TextButton(
        icon=Icons.LOGOUT,
        scale=1.5,
        icon_color=Colors.RED_700,
        on_click=click_logout
    )

    btn_salvar = ft.FilledButton(
        text="Salvar",
        style=ft.ButtonStyle(text_style=ft.TextStyle(size=16)),
        width=page.window.width,
        height=45,
        on_click=click_salvar_usuario
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
