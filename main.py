import flet as ft
from ingredient import IngredientView
from category import CategoryView
from API_call import can_login
from recipe import RecipeApp

def main(page: ft.Page):
    page.title = "Flet App with Login and Navigation"
    tf_user = ft.TextField(label="사용자 이름", autofocus=True)
    tf_pass = ft.TextField(label="비밀번호", password=True)

    def route_change(route):
        page.views.clear()
        if page.route == "/login":
            page.views.append(
                ft.View(
                    "/login",
                    [
                        ft.AppBar(title=ft.Text("로그인")),
                        ft.Column(
                            [
                                tf_user,
                                tf_pass,
                                ft.ElevatedButton("로그인", on_click=login_click)
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        )
                    ],
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            )
        elif page.route == "/" or page.route.startswith("/main"):
            page.views.append(
                ft.View(
                    "/main",
                    [
                        ft.AppBar(
                            leading=ft.Icon(ft.Icons.FOOD_BANK),
                            leading_width=40,
                            title=ft.Text("자취생을 위한 레시피 😋"), 
                            actions=[
                                ft.IconButton(ft.icons.LOGOUT, on_click=logout_click)
                            ]
                        ),
                        ft.Row(
                            [
                                ft.NavigationRail(
                                    selected_index=0,
                                    label_type=ft.NavigationRailLabelType.ALL,
                                    min_width=100,
                                    min_extended_width=400,
                                    destinations=[
                                        ft.NavigationRailDestination(
                                            icon=ft.icons.FOOD_BANK,
                                            selected_icon=ft.icons.FOOD_BANK_OUTLINED,
                                            label="레시피"
                                        ),
                                        ft.NavigationRailDestination(
                                            icon=ft.icons.CALENDAR_VIEW_DAY,
                                            selected_icon=ft.icons.CALENDAR_VIEW_DAY_OUTLINED,
                                            label="카테고리 관리"
                                        ),
                                        ft.NavigationRailDestination(
                                            icon=ft.icons.COOKIE,
                                            selected_icon=ft.icons.COOKIE_OUTLINED,
                                            label="재료 관리"
                                        )
                                    ],
                                    on_change=navigation_change
                                ),
                                ft.VerticalDivider(width=1),
                                ft.Column([ft.Text("메인 콘텐츠")], alignment=ft.MainAxisAlignment.START, expand=True)
                                # ft.Column([RecipeApp()], alignment=ft.MainAxisAlignment.START, expand=True)
                                # ft.Container(
                                #     content=ft.View(
                                #         "/recipe",
                                #         [RecipeApp()]
                                #     ),
                                #     expand=True
                                # )
                            ],
                            expand=True
                        )
                    ]
                )
            )
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    def login_click(e):
        r = can_login(tf_user.value, tf_pass.value)
        if r['result']:
            page.clean()
            page.session.set("user", r)
            # page.add(ft.Text(f"환영합니다, {username.value}님!", size=20))
            page.go("/main")
        else:
            page.session.set("user", None)
            page.add(ft.Text("로그인 실패. 다시 시도해주세요.", color="red"))
        # page.update()
        

    def logout_click(e):
        page.go("/login")

    def navigation_change(e):
        index = e.control.selected_index
        # container = page.views[-1].controls[-1].controls[-1]

        if index == 0:
            # page.views[-1].controls[-1].controls[-1].controls = [ft.Text("레시피")]
            page.views[-1].controls[-1].controls[-1].controls = [RecipeApp()]
        elif index == 1:
            page.views[-1].controls[-1].controls[-1].controls = [CategoryView()]
        elif index == 2:
            page.views[-1].controls[-1].controls[-1].controls = [IngredientView()]
        # if index == 0:
        #     container.content = ft.View("/recipe", [RecipeApp()])
        # elif index == 1:
        #     container.content = ft.View("/category", [CategoryView()])
        # elif index == 2:
        #     container.content = ft.View("/ingredient", [IngredientView()])

        page.update()

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go("/login")

ft.app(target=main, view=ft.WEB_BROWSER)