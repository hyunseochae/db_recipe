from typing import Literal, Union
from typing_extensions import Literal
import flet as ft
from API_call import create_ingredient, read_ingredient, read_ingredients, delete_ingredient as api_delete_ingredient
class IngredientView(ft.Column):    

    def _get_ingredients(self):
        r = read_ingredients()
        # print(r)
        # return [ing["name"] for ing in r]
        return r
    
    def __init__(self):
        super().__init__()
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.cs = {}
        self.ingredients = self._get_ingredients()
        self.ingredient_input = ft.TextField(label="재료명", width=300)
        self.add_button = ft.ElevatedButton("추가", on_click=self.add_ingredient)
        # self.clear_button = ft.ElevatedButton("모두 삭제", on_click=clear_all_ingredients, color=ft.colors.RED)
        self.ingredients_list = ft.ListView(expand=1, spacing=2, padding=10)
    
    def update_ingredients_list(self):
        self.ingredients_list.controls = [
            ft.ListTile(
                title=ft.Text(ing['name']),
                trailing=ft.IconButton(
                    ft.icons.DELETE,
                    on_click=lambda _, x=ing: self.delete_ingredient(x)
                )
            ) for ing in self.ingredients
        ]
        self.update()

    def add_ingredient(self, e):
        if not self.ingredient_input.value:
            return
        # 이미 있으면 무시
        if self.ingredient_input.value in self.ingredients:
            return
        ing = create_ingredient(self.ingredient_input.value)
        self.ingredients.append(ing)
        self.ingredient_input.value = ""
        self.update_ingredients_list()

    def delete_ingredient(self, ingredient):
        api_delete_ingredient(ingredient['ingredient_id'])
        self.ingredients.remove(ingredient)
        self.update_ingredients_list()

    def clear_all_ingredients(self, e):
        self.ingredients.clear()
        self.update_ingredients_list()

    def build(self):
        self.controls = [
            ft.Text("레시피 재료 관리", size=20, weight=ft.FontWeight.BOLD),
            ft.Row([self.ingredient_input, self.add_button], alignment=ft.MainAxisAlignment.CENTER),
            ft.Container(
                content=self.ingredients_list,
                height=400,
                width=400,
                border=ft.border.all(1, ft.colors.OUTLINE),
                border_radius=10,
                padding=10
            )
            # clear_button
        ]
        # return super().build()
    
    def did_mount(self):
        self.update_ingredients_list()
        return super().did_mount()