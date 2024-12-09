import requests

BASE_URL = "http://127.0.0.1:8000"

def can_login(user: str, password: str):
    response = requests.get(f"{BASE_URL}/can_login/", params={
        "user": user,
        "password": password
    })
    return response.json()

# ---------------user----------------
def create_user(username: str, email: str, password: str):
    response = requests.post(f"{BASE_URL}/users/", params={
        "username": username,
        "email": email,
        "password": password
    })
    return response.json()

def read_user(user_id: int):
    response = requests.get(f"{BASE_URL}/users/{user_id}")
    return response.json()

def read_users(skip: int = 0, limit: int = 100):
    response = requests.get(f"{BASE_URL}/users/", params={
        "skip": skip,
        "limit": limit
    })
    return response.json()

def update_user(user_id: int, username: str = None, email: str = None, password: str = None):
    params = {}
    if username:
        params["username"] = username
    if email:
        params["email"] = email
    if password:
        params["password"] = password
    
    response = requests.put(f"{BASE_URL}/users/{user_id}", params=params)
    return response.json()

def delete_user(user_id: int):
    response = requests.delete(f"{BASE_URL}/users/{user_id}")
    return response.json()


# ---------------ingredient----------------
def create_ingredient(name: str, unit: str="ea"):
    response = requests.post(f"{BASE_URL}/ingredients/", params={
        "name": name,
        "unit": unit
    })
    return response.json()

def read_ingredient(ingredient_id: int):
    response = requests.get(f"{BASE_URL}/ingredients/{ingredient_id}")
    return response.json()

def read_ingredients(skip: int = 0, limit: int = 100):
    response = requests.get(f"{BASE_URL}/ingredients/", params={
        "skip": skip,
        "limit": limit
    })
    return response.json()

def delete_ingredient(ingredient_id: int):
    response = requests.delete(f"{BASE_URL}/ingredients/{ingredient_id}")
    return response.json()

# ---------------category----------------
def create_category(name: str):
    response = requests.post(f"{BASE_URL}/categories/", params={
        "name": name
    })
    return response.json()

def read_category(category_id: int):
    response = requests.get(f"{BASE_URL}/categories/{category_id}")
    return response.json()

def read_categories(skip: int = 0, limit: int = 100):
    response = requests.get(f"{BASE_URL}/categories/", params={
        "skip": skip,
        "limit": limit
    })
    return response.json()

def delete_category(category_id: int):
    response = requests.delete(f"{BASE_URL}/categories/{category_id}")
    return response.json()

# ---------------recipe----------------
def create_recipe(title, category_id, ingredient_ids, description, cooking_time, difficulty_level, servings, user_id):
    response = requests.post(f"{BASE_URL}/recipes/", params={
        "title": title,
        "category_id": category_id,
        "ingredient_ids": ingredient_ids,
        "description": description,
        "cooking_time": cooking_time,
        "difficulty_level": difficulty_level,
        "servings": servings,
        "user_id": user_id
    })
    r = response.json()
    return r

def read_recipe(recipe_id: int):
    response = requests.get(f"{BASE_URL}/recipes/{recipe_id}")
    return response.json()

def read_recipes(skip: int = 0, limit: int = 100):
    response = requests.get(f"{BASE_URL}/recipes/", params={
        "skip": skip,
        "limit": limit
    })
    return response.json()

def delete_recipe(recipe_id: int):
    response = requests.delete(f"{BASE_URL}/recipes/{recipe_id}")
    return response.json()

# -----------------read_recipe_category-------------
def read_recipe_category(recipe_id: int):
    response = requests.get(f"{BASE_URL}/recipecategories/{recipe_id}")
    return response.json()

def read_recipe_ingredients(recipe_id: int):
    response = requests.get(f"{BASE_URL}/recipeingredients/{recipe_id}")
    return response.json()

# 사용 예시
if __name__ == "__main__":
    # r = can_login ("aaa", "1234")
    # print(r)
    # r = can_login ("aaa", "aaa")
    # print(r)
    
    # # 사용자 생성
    # new_user = create_user("newuser5", "newuser5@example.com", "password123")
    # print("Created user:", new_user)

    # # 사용자 정보 읽기
    # user_info = read_user(new_user["user_id"])
    # print("User info:", user_info)

    # # 모든 사용자 목록 가져오기
    # all_users = read_users()
    # print("All users:", all_users)

    # # 사용자 정보 업데이트
    # updated_user = update_user(new_user["user_id"], username="updateduser")
    # print("Updated user:", updated_user)

    # # 사용자 삭제
    # delete_result = delete_user(new_user["user_id"])
    # print("Delete result:", delete_result)

    
    # # 재료 생성
    # new_ingredient = create_ingredient("콩나물")
    # print("Created ingredient:", new_ingredient)

    # # 재료 정보 읽기
    # ingredient_info = read_ingredient(new_ingredient["ingredient_id"])
    # print("ingredient info:", ingredient_info)

    # # 모든 재료 목록 가져오기
    # all_ingredients = read_ingredients()
    # print("All ingredients:", all_ingredients)

    # # 재료 삭제
    # delete_result = delete_ingredient(new_ingredient["ingredient_id"])
    # print("Delete result:", delete_result)

    # # 레시피 생성
    # new_recipe = create_recipe("국밥", 10, [5, 7, 9], "국밥을 만들는 방법", 30, 3, 4)
    # print("Created recipe:", new_recipe)

    # # 레시피 정보 읽기
    # recipe_info = read_recipe(new_recipe["recipe_id"])
    # print("recipe info:", recipe_info)

    # # 모든 레시피 목록 가져오기
    # all_recipes = read_recipes()
    # print("All recipes:", all_recipes)

    # # 레시피 삭제
    # delete_result = delete_recipe(new_recipe["recipe_id"])
    # print("Delete result:", delete_result)

    # r = read_recipe_category(10)
    # print("recipe category info:", r)

    r = read_recipe_ingredients(15)
    print("recipe ingredients info:", r)