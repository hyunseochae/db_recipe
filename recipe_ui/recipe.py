import flet as ft
from API_call import read_categories, read_ingredients, create_recipe, read_recipes, delete_recipe as api_delete_recipe
from API_call import read_recipe_category, read_recipe_ingredients
class Recipe:
    
    def __init__(self, title, category, ingredients, description, time, difficulty, servings):
        self.title = title
        self.category = category
        self.ingredients = ingredients
        self.description = description
        self.time = time
        self.difficulty = difficulty
        self.servings = servings
        self.ingredient_ids = None

class RecipeApp(ft.Column):
    def __init__(self):
        super().__init__()
        self.route = "/recipe"
        self.categories = self._get_categories()
        self.ingredients = self._get_ingredients()
        self.recipes = self._get_recipes()
        self.selected_category = self.categories[0] if self.categories else None
        self.categories_list = ft.ListView(expand=1, spacing=2, padding=10)
        
        self.category_dropdown = ft.Dropdown(
            options=[ft.dropdown.Option(category['name']) for category in self.categories],
            value=self.selected_category['name'] if self.selected_category else None,
            on_change=self.change_category
        )
        
        self.recipe_list = ft.ListView(expand=1, spacing=10, padding=20)
        self.add_recipe_button = ft.IconButton(ft.icons.ADD, on_click=self.show_add_recipe_dialog)
        self.controls = [self.build()]

    def _get_cateory_id(self):
        for cat in self.categories:
            if self.category_dropdown.value == cat['name']:
                return cat['category_id']
    
    # def _get_ingredient_ids(self):
    #     ids = []
    #     for ing in ingredient_chips.controls:

    def _get_recipes(self):
        rs = read_recipes()
        for r in rs:
            rc = read_recipe_category(r['recipe_id'])
            ri = read_recipe_ingredients(r['recipe_id'])
            if rc:
                r['category_id'] = rc['category_id']
            if ri:
                r['ingredients_ids'] = ','.join([str(x['ingredient_id']) for x in ri])
        return rs
    
    def _get_categories(self):
        r = read_categories()
        return r
    
    def _get_ingredients(self):
        return read_ingredients()
    
    def build(self):
        self.controls = [
            ft.Row([
                self.category_dropdown,
                self.add_recipe_button
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            self.recipe_list
        ]

    def _get_category_from_name(self, name):
        for cat in self.categories:
            if cat['name'] == name:
                return cat
            
    def get_category_name(self, category_id):
        for category in self.categories:
            if category['category_id'] == category_id:
                return category['name']
        return None
    
    def get_ingredient_names(self, ingredient_ids):
        ingredient_names = []
        for ingredient_id in ingredient_ids:
            for ingredient in self.ingredients:
                if ingredient['ingredient_id'] == int(ingredient_id):
                    ingredient_names.append(ingredient['name'])
                    break
        return ingredient_names
            
    def change_category(self, e):
        self.selected_category = self._get_category_from_name(e.control.value)
        self.update_recipe_list()

    def update_recipe_list(self):
        self.recipe_list.controls = []
        for recipe in self.recipes:
            if 'category_id' not in recipe or 'category_id' not in self.selected_category:
                continue
            if (recipe['category_id'] != self.selected_category['category_id']):
                continue
            lt = ft.ListTile(
                title=ft.Text(recipe.title if isinstance(recipe, Recipe) else recipe['title']),
                on_click=lambda _, r=recipe: self.show_recipe_details(r)
            ) 
            self.recipe_list.controls.append(lt)
        self.update()

    def show_recipe_details(self, recipe):
        def close_dlg(e):
            self.page.dialog.open = False
            self.page.update()
        
        # ---------------------------------------------------------------------수정필요/삭제, 수정
        # 삭제 됨. 근데 바로 안없어짐
        def delete_dlg(e):
            api_delete_recipe(recipe['recipe_id'])
            self.page.dialog.open = False
            self.page.update()

        def update_dlg(e):
            self.page.dialog.open = False
            self.page.update()


        # ---------------------------------------------------------------------수정필요/재료명 출력
        # 카테고리명과 재료명 출력 되는데, 카테고리명을 추가창에서 선택할 수 없음.
        # 추가했을 땐 재료명 출력 되는데, 저장되어 있는건 출력 안됨.
        # 밖에 창에서 카테고리를 지정한 후 저장을 누르면 그 카테고리에 들어감.

        # categories = '' if 'category_id' not in recipe or not recipe['category_id'] else f"카테고리: {recipe['category_id']}"
        # ings = '' if 'ingredient_ids' not in recipe or not recipe['ingredient_ids'] else f"재료: {', '.join(recipe['ingredient_ids'])}"
        category_name = self.get_category_name(recipe['category_id']) if 'category_id' in recipe else ''
        ingredient_names = self.get_ingredient_names(recipe['ingredient_ids'].split(',') if 'ingredient_ids' in recipe and recipe['ingredient_ids'] else [])

        self.page.dialog = ft.AlertDialog(
            title=ft.Text(recipe['title']),
            content=ft.Column([
                # ft.Text(f"카테고리: {categories}"),
                # ft.Text(f"재료: {ings}"),
                ft.Text(f"카테고리: {category_name}"),
                ft.Text(f"재료: {', '.join(ingredient_names)}"),
                ft.Text(f"조리 방법:\n{recipe['description']}"),
                ft.Text(f"소요 시간: {recipe['cooking_time']}분"),
                ft.Text(f"난이도: {recipe['difficulty_level']}/10"),
                ft.Text(f"몇 인분: {recipe['servings']}인분")
            ], tight=True),
            actions=[
                ft.TextButton("수정", on_click=update_dlg),
                ft.TextButton("삭제", on_click=delete_dlg),
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

        # 재료 목록 (예시)
        # ingredient_input = ft.TextField(label="재료 입력", expand=True)
        selected_ingredients = []
        ingredients_chips = ft.Row(wrap=True, spacing=5)

        ingredients = [ing['name'] for ing in self.ingredients]
        
        ingredients_dropdown = ft.Dropdown(
            options=[ft.dropdown.Option(ingredient) for ingredient in ingredients],
            label="재료 선택",
            width=150,
        )
        selected_ingredients = []
        # ingredients_list = ft.Column()

        def add_ingredient(e):
            if ingredients_dropdown.value and ingredients_dropdown.value not in selected_ingredients:
                selected_ingredients.append(ingredients_dropdown.value)
                update_ingredients_chips()
                ingredients_dropdown.value = ""  # 입력 필드 초기화
                self.page.update()

        def remove_ingredient(ingredient):
            selected_ingredients.remove(ingredient)
            update_ingredients_chips()

        def _get_ingredient_id_from_name(name):
            for ing in self.ingredients:
                if ing['name'] == name:
                    return ing['ingredient_id']
                
        def update_ingredients_chips():
            ingredients_chips.controls = [
                ft.Chip(
                    label=ft.Text(ingredient),
                    delete_icon=ft.Icon(ft.icons.DELETE),
                    on_delete=lambda _, i=ingredient: remove_ingredient(i)
                ) for ingredient in selected_ingredients
            ]
            self.ingredient_ids = [_get_ingredient_id_from_name(ingname) for ingname in selected_ingredients]
            
            self.page.update()
        add_ingredient_button = ft.ElevatedButton("재료 추가", on_click=add_ingredient)

        description_input = ft.TextField(label="조리 방법", multiline=True, height=300)
        time_input = ft.TextField(label="소요 시간 (분)")
        difficulty_input = ft.Slider(min=1, max=10, divisions=9, label="{value}")
        servings_input = ft.TextField(label="몇 인분")

        def delete_recipe(self, recipe):
            api_delete_recipe(recipe['recipe_id'])
            self.recipes.remove(recipe)
            self.update_recipes_list()

        def clear_all_recipes(self, e):
            self.recipes.clear()
            self.update_recipes_list()

        def save_recipe(e):
            user = self.page.session.get("user")
            new_recipe = create_recipe(
                title = title_input.value,
                category_id = self._get_cateory_id(),
                ingredient_ids = ','.join([str(x) for x in self.ingredient_ids]),
                description = description_input.value,
                cooking_time = int(time_input.value),
                difficulty_level = int(difficulty_input.value),
                servings = int(servings_input.value),
                user_id=user['user_id']
            )
            self.recipes.append(new_recipe)
            self.update_recipe_list()
            self.page.dialog.open = False
            self.page.update()

        def close_dlg(e):
            self.page.dialog.open = False
            self.page.update()
        
        def delete_dlg(e):
            self.page.dialog.open = False
            self.page.update()

        self.page.dialog = ft.AlertDialog(
            title=ft.Text("새 레시피 추가"),
            content=ft.Column(
                [
                    title_input,
                    category_dropdown,
                    ft.Row([ingredients_dropdown, add_ingredient_button, ingredients_chips]),
                    description_input,
                    time_input,
                    ft.Text("난이도"),
                    difficulty_input,
                    servings_input
                ], 
                tight=True, scroll=ft.ScrollMode.AUTO,
                width=self.page.width - 200
            ),
            actions=[
                ft.TextButton("저장", on_click=save_recipe),
                ft.TextButton("취소", on_click=close_dlg)
            ],
        )
        self.page.dialog.open = True
        self.page.update()

    def get_category_id(self, category_name):
        for category in self.categories:
            if category['name'] == category_name:
                return category['category_id']
        return None
    
    def get_ingredient_ids(self, selected_ingredients):
        ingredient_ids = []
        for ingredient in selected_ingredients:
            for ing in self.ingredients:
                if ing['name'] == ingredient:
                    ingredient_ids.append(ing['ingredient_id'])
                    break
        return ingredient_ids

def main(page: ft.Page):
    page.title = "자취생을 위한 레시피 앱"
    recipe_app = RecipeApp()
    page.add(recipe_app)

if __name__ == "__main__":
    ft.app(target=main, view=ft.WEB_BROWSER)
