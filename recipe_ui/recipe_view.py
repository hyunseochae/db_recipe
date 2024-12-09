import flet as ft
from API_call import read_categories, read_ingredients

class Recipe:
    def __init__(self, title, category, ingredients, description, time, difficulty, servings):
        self.title = title
        self.category = category
        self.ingredients = ingredients
        self.description = description
        self.time = time
        self.difficulty = difficulty
        self.servings = servings

class RecipeView(ft.View):
    def __init__(self):
        super().__init__(route="/recipe")
        self.categories = self._get_categories()
        self.ingredients = self._get_ingredients()
        self.recipes = []
        self.selected_category = self.categories[0] if self.categories else None
        
        self.category_dropdown = ft.Dropdown(
            options=[ft.dropdown.Option(category['name']) for category in self.categories],
            value=self.selected_category['name'] if self.selected_category else None,
            on_change=self.change_category
        )
        
        self.recipe_list = ft.ListView(expand=1, spacing=10, padding=20)
        self.add_recipe_button = ft.IconButton(ft.icons.ADD, on_click=self.show_add_recipe_dialog)
        
        self.controls = [
            ft.Column([
                ft.Row([
                    self.category_dropdown,
                    self.add_recipe_button
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                self.recipe_list
            ])
        ]

    def _get_categories(self):
        return read_categories()

    def _get_ingredients(self):
        return read_ingredients()

    def change_category(self, e):
        self.selected_category = e.control.value
        self.update_recipe_list()

    def update_recipe_list(self):
        self.recipe_list.controls = [
            ft.ListTile(
                title=ft.Text(recipe.title),
                on_click=lambda _, r=recipe: self.show_recipe_details(r)
            ) for recipe in self.recipes if recipe.category == self.selected_category
        ]
        self.update()

    def show_recipe_details(self, recipe):
        def close_dlg(e):
            self.page.dialog.open = False
            self.page.update()

        self.page.dialog = ft.AlertDialog(
            title=ft.Text(recipe.title),
            content=ft.Column([
                ft.Text(f"카테고리: {recipe.category}"),
                ft.Text(f"재료: {', '.join(recipe.ingredients)}"),
                ft.Text(f"조리 방법:\n{recipe.description}"),
                ft.Text(f"소요 시간: {recipe.time}분"),
                ft.Text(f"난이도: {recipe.difficulty}/10"),
                ft.Text(f"몇 인분: {recipe.servings}인분")
            ], tight=True),
            actions=[
                ft.TextButton("닫기", on_click=close_dlg)
            ]
        )
        self.page.dialog.open = True
        self.page.update()

    def show_add_recipe_dialog(self, e):
        title_input = ft.TextField(label="레시피 제목")
        category_dropdown = ft.Dropdown(
            options=[ft.dropdown.Option(category['name']) for category in self.categories],
            label="카테고리"
        )

        selected_ingredients = []
        ingredients_chips = ft.Row(wrap=True, spacing=5)
        ingredients = [ing['name'] for ing in self.ingredients]
        ingredients_dropdown = ft.Dropdown(
            options=[ft.dropdown.Option(ingredient) for ingredient in ingredients],
            label="재료 선택",
            width=150
        )

        def add_ingredient(e):
            if ingredients_dropdown.value and ingredients_dropdown.value not in selected_ingredients:
                selected_ingredients.append(ingredients_dropdown.value)
                update_ingredients_chips()
                ingredients_dropdown.value = ""
                self.page.update()

        def remove_ingredient(ingredient):
            selected_ingredients.remove(ingredient)
            update_ingredients_chips()

        def update_ingredients_chips():
            ingredients_chips.controls = [
                ft.Chip(
                    label=ft.Text(ingredient),
                    delete_icon=ft.Icon(ft.icons.DELETE),
                    on_delete=lambda _, i=ingredient: remove_ingredient(i)
                ) for ingredient in selected_ingredients
            ]
            self.page.update()

        add_ingredient_button = ft.ElevatedButton("재료 추가", on_click=add_ingredient)
        description_input = ft.TextField(label="조리 방법", multiline=True, height=300)
        time_input = ft.TextField(label="소요 시간 (분)")
        difficulty_input = ft.Slider(min=1, max=10, divisions=9, label="{value}")
        servings_input = ft.TextField(label="몇 인분")

        def save_recipe(e):
            new_recipe = Recipe(
                title_input.value,
                category_dropdown.value,
                selected_ingredients,
                description_input.value,
                int(time_input.value),
                int(difficulty_input.value),
                int(servings_input.value)
            )
            self.recipes.append(new_recipe)
            self.update_recipe_list()
            self.page.dialog.open = False
            self.page.update()

        def close_dlg(e):
            self.page.dialog.open = False
            self.page.update()

        self.page.dialog = ft.AlertDialog(
            title=ft.Text("새 레시피 추가"),
            content=ft.Column([
                title_input,
                category_dropdown,
                ft.Row([ingredients_dropdown, add_ingredient_button, ingredients_chips]),
                description_input,
                time_input,
                ft.Text("난이도"),
                difficulty_input,
                servings_input
            ], tight=True, scroll=ft.ScrollMode.AUTO),
            actions=[
                ft.TextButton("저장", on_click=save_recipe),
                ft.TextButton("취소", on_click=close_dlg)
            ]
        )
        self.page.dialog.open = True
        self.page.update()

def main(page: ft.Page):
    page.title = "자취생을 위한 레시피 앱"
    recipe_view = RecipeView()
    page.add(recipe_view)

ft.app(target=main, view=ft.WEB_BROWSER)