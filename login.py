import flet as ft
from API_call import can_login

def main(page: ft.Page):
    page.title = "로그인"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    username = ft.TextField(label="사용자 이름", autofocus=True)
    password = ft.TextField(label="비밀번호", password=True)
    login_button = ft.ElevatedButton(text="로그인")

    def login_click(e):
        r = can_login(username.value, password.value)
        if r:
            page.clean()
            page.add(ft.Text(f"환영합니다, {username.value}님!", size=20))
        else:
            page.add(ft.Text("로그인 실패. 다시 시도해주세요.", color="red"))
        page.update()

    login_button.on_click = login_click

    page.add(
        ft.Column(
            [
                username,
                password,
                login_button
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
    )

ft.app(target=main, view=ft.WEB_BROWSER)