# crud.py
from sqlalchemy.orm import Session
from models import User, Categories, Recipes, Ingredients, RecipeIngredients, Ratings, UserPreferences, RecipeCategories, Instructions
from typing import Optional
from datetime import datetime

# User CRUD
def create_user(db: Session, user: User):
    try:
        db_user = User(
            username=user.username,
            email=user.email,
            password=user.password,
            created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        print(e)
        return e

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.user_id == user_id).first()

def can_login(db: Session, user: str, password: str):
    db_user = db.query(User).filter(User.username == user, User.password == password).first()
    if db_user:
        return {"result": True, "user_id": db_user.user_id, "username": db_user.username, "email": db_user.email}
    return {"result": False}

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

def update_user(db: Session, user_id: int, username: Optional[str] = None, 
                email: Optional[str] = None, password: Optional[str] = None):
    db_user = db.query(User).filter(User.user_id == user_id).first()
    if db_user:
        if username:
            db_user.username = username
        if email:
            db_user.email = email
        if password:
            db_user.password = password
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = db.query(User).filter(User.user_id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False

# Categories CRUD
def create_category(db: Session, category: str):
    try:
        db_category = Categories(
            name=category.name
        )
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        return db_category
    except Exception as e:
        print(e)
        return e
    
def get_category(db: Session, category_id: int):
    return db.query(Categories).filter(Categories.category_id == category_id).first()

def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Categories).offset(skip).limit(limit).all()

def update_category(db: Session, category_id: int, name: Optional[str] = None):
    db_category = db.query(Categories).filter(Categories.category_id == category_id).first()
    if db_category:
        if name:
            db_category.name = name
        db.commit()
        db.refresh(db_category)
    return db_category

def delete_category(db: Session, category_id: int):
    db_category = db.query(Categories).filter(Categories.category_id == category_id).first()
    if db_category:
        db.delete(db_category)
        db.commit()
        return True
    return False

# Recipe CRUD
def create_recipe(db: Session, recipe: Recipes, user: User):
    try :
        db_recipe = Recipes(
            title=recipe.title,
            description=recipe.description,
            cooking_time=recipe.cooking_time,
            difficulty_level=recipe.difficulty_level,
            servings=recipe.servings,
            user_id=user.user_id,
            created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        db.add(db_recipe)
        db.commit()
        db.refresh(db_recipe)
        return db_recipe
    except Exception as e:
        print(e)
        return e

def get_recipes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Recipes).offset(skip).limit(limit).all()

def get_recipe(db: Session, recipe_id: int):
    return db.query(Recipes).filter(Recipes.recipe_id == recipe_id).first()

def update_recipe(db: Session, recipe_id: int, title: Optional[str] = None, 
                  description: Optional[str] = None, cooking_time: Optional[int] = None,
                  difficulty_level: Optional[int] = None, servings: Optional[str] = None):
    db_recipe = db.query(Recipes).filter(Recipes.recipe_id == recipe_id).first()
    if db_recipe:
        if title:
            db_recipe.title = title
        if description:
            db_recipe.description = description
        if cooking_time:
            db_recipe.cooking_time = cooking_time
        if difficulty_level:
            db_recipe.difficulty_level = difficulty_level
        if servings:
            db_recipe.servings = servings
        db.commit()
        db.refresh(db_recipe)
    return db_recipe

def delete_recipe(db: Session, recipe_id: int):
    db_recipe = db.query(Recipes).filter(Recipes.recipe_id == recipe_id).first()
    if db_recipe:
        db.delete(db_recipe)
        db.commit()
        return True
    return False

# Ingredients CRUD
def create_ingredient(db: Session, ingredient: Ingredients):
    try:
        db_ingredient = Ingredients(
            name=ingredient.name,
            unit=ingredient.unit,
        )
        db.add(db_ingredient)
        db.commit()
        db.refresh(db_ingredient)
        return db_ingredient
    except Exception as e:
        print(e)
        return e
    
def get_ingredient(db: Session, ingredient_id: int):
    return db.query(Ingredients).filter(Ingredients.ingredient_id == ingredient_id).first()

def get_ingredients(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Ingredients).offset(skip).limit(limit).all()

def update_ingredient(db: Session, ingredient_id: int, name: Optional[str] = None, unit: Optional[str] = None):
    db_ingredient = db.query(Ingredients).filter(Ingredients.ingredient_id == ingredient_id).first()
    if db_ingredient:
        if name:
            db_ingredient.name = name
        if unit:
            db_ingredient.unit = unit
        db.commit()
        db.refresh(db_ingredient)
    return db_ingredient

def delete_ingredient(db: Session, ingredient_id: int):
    db_ingredient = db.query(Ingredients).filter(Ingredients.ingredient_id == ingredient_id).first()
    if db_ingredient:
        db.delete(db_ingredient)
        db.commit()
        return True
    return False

# Recipe Ingredients CRUD
def create_recipe_ingredient(db: Session, recipe_id: int, ingredient_id: int, quantity: str = '1'):
    try:
        db_recipe_ingredient = RecipeIngredients(
            quantity='1',
            recipe_id=recipe_id,
            ingredient_id=ingredient_id,
        )
        db.add(db_recipe_ingredient)
        db.commit()
        db.refresh(db_recipe_ingredient)
        return db_recipe_ingredient
    except Exception as e:
        print(e)
        return e
    
def get_recipe_ingredient(db: Session, recipe_id: int):
    return db.query(RecipeIngredients).filter(RecipeIngredients.recipe_id == recipe_id).all()

def get_recipe_ingredients(db: Session, skip: int = 0, limit: int = 100):
    return db.query(RecipeIngredients).offset(skip).limit(limit).all()

def update_recipe_ingredient(db: Session, recipe_id: int, quantity: Optional[str] = None):
    db_recipe_ingredient = db.query(RecipeIngredients).filter(RecipeIngredients.recipe_id == recipe_id).first()
    if db_recipe_ingredient:
        if quantity:
            db_recipe_ingredient.quantity = quantity
        db.commit()
        db.refresh(db_recipe_ingredient)
    return db_recipe_ingredient 

def delete_recipe_ingredient(db: Session, recipe_id: int):
    db_recipe_ingredients = db.query(RecipeIngredients).filter(RecipeIngredients.recipe_id == recipe_id).all()
    if not db_recipe_ingredients:
        return False
    for db_recipe_ingredient in db_recipe_ingredients:
        db.delete(db_recipe_ingredient)
    db.commit()
    return True

# Ratings CRUD
def create_rating(db: Session, score: int, comment: str, user_id: int, recipe_id: int):
    try:
        db_rating = Ratings(
            score=score,
            comment=comment,
            created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            user_id=user_id,
            recipe_id=recipe_id
        )
        db.add(db_rating)
        db.commit()
        db.refresh(db_rating)
        return db_rating
    except Exception as e:
        print(e)
        return e
    
def get_rating(db: Session, rating_id: int):
    return db.query(Ratings).filter(Ratings.rating_id == rating_id).first()

def get_ratings(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Ratings).offset(skip).limit(limit).all()

def update_rating(db: Session, rating_id: int, score: Optional[int] = None, comment: Optional[str] = None):
    db_rating = db.query(Ratings).filter(Ratings.rating_id == rating_id).first()
    if db_rating:
        if score:
            db_rating.score = score
        if comment:
            db_rating.comment = comment
        db.commit()
        db.refresh(db_rating)
    return db_rating

def delete_rating(db: Session, rating_id: int):
    db_rating = db.query(Ratings).filter(Ratings.rating_id == rating_id).first()
    if db_rating:
        db.delete(db_rating)
        db.commit()
        return True
    return False


# # Saved Recipes CRUD
# def create_saved_recipe(db: Session, saved_recipe: SavedRecipes, user: User, recipe: Recipes):
#     try:
#         db_saved_recipe = SavedRecipes(
#             user_id=user.user_id,
#             recipe_id=recipe.recipe_id,
#             created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         )
#         db.add(saved_recipe)
#         db.commit()
#         db.refresh(saved_recipe)
#         return db_saved_recipe
#     except Exception as e:
#         print(e)
#         return e

# def get_saved_recipe(db: Session, user_id: int, recipe_id: int):
#     return db.query(SavedRecipes).filter(SavedRecipes.user_id == user_id, SavedRecipes.recipe_id == recipe_id).first()

# def get_saved_recipes(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(SavedRecipes).offset(skip).limit(limit).all()

# def delete_saved_recipe(db: Session, user_id: int, recipe_id: int):
#     db_saved_recipe = db.query(SavedRecipes).filter(SavedRecipes.user_id == user_id, SavedRecipes.recipe_id == recipe_id).first()
#     if db_saved_recipe:
#         db.delete(db_saved_recipe)
#         db.commit()
#         return True
#     return False

# def get_saved_recipes_by_user(db: Session, user_id: int):
#     return db.query(SavedRecipes).filter(SavedRecipes.user_id == user_id).all()

# def get_saved_recipes_by_recipe(db: Session, recipe_id: int):
#     return db.query(SavedRecipes).filter(SavedRecipes.recipe_id == recipe_id).all()


# User Preferences CRUD
def create_user_preference(db: Session, user_id: int, category_id: int):
    try:
        db_user_preference = UserPreferences(
            user_id=user_id,
            category_id=category_id,
            created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        db.add(db_user_preference)
        db.commit()
        db.refresh(db_user_preference)
        return db_user_preference
    except Exception as e:
        print(e)
        return e

def get_user_preference(db: Session, user_id: int, category_id: int):
    return db.query(UserPreferences).filter(UserPreferences.user_id == user_id, UserPreferences.category_id == category_id).first()

def get_user_preferences(db: Session, skip: int = 0, limit: int = 100):
    return db.query(UserPreferences).offset(skip).limit(limit).all()

def delete_user_preference(db: Session, user_id: int, category_id: int):
    db_user_preference = db.query(UserPreferences).filter(UserPreferences.user_id == user_id, UserPreferences.category_id == category_id).first()
    if db_user_preference:
        db.delete(db_user_preference)
        db.commit()
        return True
    return False

def get_user_preferences_by_user(db: Session, user_id: int):
    return db.query(UserPreferences).filter(UserPreferences.user_id == user_id).all()

def get_user_preferences_by_category(db: Session, category_id: int):
    return db.query(UserPreferences).filter(UserPreferences.category_id == category_id).all()

# Recipe Categories CRUD
def create_recipe_category(db: Session, recipe_id: int, category_id: int):
    try:
        db_recipe_category = RecipeCategories(
            recipe_id=recipe_id,
            category_id=category_id,
            # created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        db.add(db_recipe_category)
        db.commit()
        db.refresh(db_recipe_category)
        return db_recipe_category
    except Exception as e:
        print(e)
        return e

def get_recipe_category(db: Session, recipe_id: int):
    return db.query(RecipeCategories).filter(RecipeCategories.recipe_id == recipe_id).first()

def get_recipe_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(RecipeCategories).offset(skip).limit(limit).all()

def delete_recipe_category(db: Session, recipe_id: int):    
    db_recipe_category = db.query(RecipeCategories).filter(RecipeCategories.recipe_id == recipe_id).first()
    if db_recipe_category:
        db.delete(db_recipe_category)
        db.commit()
        return True
    return False

def get_recipe_categories_by_recipe(db: Session, recipe_id: int):
    return db.query(RecipeCategories).filter(RecipeCategories.recipe_id == recipe_id).all()

def get_recipe_categories_by_category(db: Session, category_id: int):
    return db.query(RecipeCategories).filter(RecipeCategories.category_id == category_id).all()

# Instructions CRUD
def create_instruction(db: Session, instruction: Instructions, recipe: Recipes):
    try:
        db_instruction = Instructions(
            step_number=instruction.step_number,
            description=instruction.description,
            recipe_id=recipe.recipe_id
        )
        db.add(db_instruction)
        db.commit()
        db.refresh(db_instruction)
        return db_instruction
    except Exception as e:
        print(e)
        return e

def get_instruction(db: Session, instruction_id: int):
    return db.query(Instructions).filter(Instructions.instruction_id == instruction_id).first()

def get_instructions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Instructions).offset(skip).limit(limit).all()

def delete_instruction(db: Session, instruction_id: int):
    db_instruction = db.query(Instructions).filter(Instructions.instruction_id == instruction_id).first()
    if db_instruction:
        db.delete(db_instruction)
        db.commit()
        return True
    return False

def get_instructions_by_recipe(db: Session, recipe_id: int):
    return db.query(Instructions).filter(Instructions.recipe_id == recipe_id).all()

def get_instructions_by_step_number(db: Session, step_number: int):
    return db.query(Instructions).filter(Instructions.step_number == step_number).all()

def get_instructions_by_description(db: Session, description: str):
    return db.query(Instructions).filter(Instructions.description == description).all()
