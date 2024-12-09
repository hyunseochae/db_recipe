import flet as ft

def main(page: ft.Page):
    
    page.title = "레시피 재료 관리"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    ingredients = []
    
    def update_ingredients_list():
        ingredients_list.controls = [
            ft.ListTile(
                title=ft.Text(ing),
                trailing=ft.IconButton(
                    ft.icons.DELETE,
                    on_click=lambda _, x=ing: delete_ingredient(x)
                )
            ) for ing in ingredients
        ]
        page.update()

    def add_ingredient(e):
        if not ingredient_input.value:
            return
        ingredients.append(ingredient_input.value)
        ingredient_input.value = ""
        update_ingredients_list()

    def delete_ingredient(ingredient):
        ingredients.remove(ingredient)
        update_ingredients_list()

    def clear_all_ingredients(e):
        ingredients.clear()
        update_ingredients_list()

    ingredient_input = ft.TextField(label="재료명", width=300)
    add_button = ft.ElevatedButton("추가", on_click=add_ingredient)
    # clear_button = ft.ElevatedButton("모두 삭제", on_click=clear_all_ingredients, color=ft.colors.RED)

    ingredients_list = ft.ListView(expand=1, spacing=2, padding=10)

    page.add(
        ft.Text("레시피 재료 관리", size=20, weight=ft.FontWeight.BOLD),
        ft.Row([ingredient_input, add_button], alignment=ft.MainAxisAlignment.CENTER),
        ft.Container(
            content=ingredients_list,
            height=400,
            width=400,
            border=ft.border.all(1, ft.colors.OUTLINE),
            border_radius=10,
            padding=10
        ),
        # clear_button
    )

# ft.app(target=main, view=ft.WEB_BROWSER)