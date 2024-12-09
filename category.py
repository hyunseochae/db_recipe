from typing import Literal, Union
from typing_extensions import Literal
import flet as ft
from API_call import create_category, read_category, read_categories, delete_category as api_delete_category
class CategoryView(ft.Column):    

    def _get_categories(self):
        r = read_categories()
        # print(r)
        # return [ing["name"] for ing in r]
        return r
    
    def __init__(self):
        super().__init__()
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.cs = {}
        self.categories = self._get_categories()
        self.category_input = ft.TextField(label="카테고리명", width=300)
        self.add_button = ft.ElevatedButton("추가", on_click=self.add_category)
        # self.clear_button = ft.ElevatedButton("모두 삭제", on_click=clear_all_categories, color=ft.colors.RED)
        self.categories_list = ft.ListView(expand=1, spacing=2, padding=10)
    
    def update_categories_list(self):
        self.categories_list.controls = [
            ft.ListTile(
                title=ft.Text(ing['name']),
                trailing=ft.IconButton(
                    ft.icons.DELETE,
                    on_click=lambda _, x=ing: self.delete_category(x)
                )
            ) for ing in self.categories
        ]
        self.update()

    def add_category(self, e):
        if not self.category_input.value:
            return
        # 이미 있으면 무시
        if self.category_input.value in self.categories:
            return
        ing = create_category(self.category_input.value)
        self.categories.append(ing)
        self.category_input.value = ""
        self.update_categories_list()

    def delete_category(self, category):
        api_delete_category(category['category_id'])
        self.categories.remove(category)
        self.update_categories_list()

    def clear_all_categories(self, e):
        self.categories.clear()
        self.update_categories_list()

    def build(self):
        self.controls = [
            ft.Text("레시피 카테고리 관리", size=20, weight=ft.FontWeight.BOLD),
            ft.Row([self.category_input, self.add_button], alignment=ft.MainAxisAlignment.CENTER),
            ft.Container(
                content=self.categories_list,
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
        self.update_categories_list()
        return super().did_mount()