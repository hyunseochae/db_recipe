# main.py
import crud
import models
import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/can_login")
def can_login(user: str, password: str, db: Session = Depends(get_db)):
    r = crud.can_login(db, user=user, password=password)
    return r

# --------------user---------------
@app.post("/users/")
def create_user(username: str, email: str, password: str, db: Session = Depends(get_db)):
    try :
        user = models.User(username=username, email=email, password=password)
        r = crud.create_user(db=db, user=user)
        return r
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/users/{user_id}")
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.get("/users/")
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.put("/users/{user_id}")
def update_user(user_id: int, username: str = None, email: str = None, 
                password: str = None, db: Session = Depends(get_db)):
    db_user = crud.update_user(db, user_id, username, email, password)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    success = crud.delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}


# ------------------categories---------------
@app.post("/categories/")
def create_category(name: str, db: Session = Depends(get_db)):
    try :
        category = models.Categories(name=name)
        return crud.create_category(db=db, category=category)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/categories/{category_id}")
def read_categories(category_id: int = 0, db: Session = Depends(get_db)):
    db_categories = crud.get_categories(db, category_id=category_id)
    if db_categories is None:
        raise HTTPException(status_code=404, detail="Categories not found")
    return db_categories

@app.get("/categories/")
def read_category(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    categories = crud.get_categories(db, skip=skip, limit=limit)
    return categories

@app.delete("/categories/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    success = crud.delete_category(db, category_id)
    if not success:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"message": "Category deleted successfully"}


# ------------------recipes---------------
@app.post("/recipes/")
def create_recipe(
    title: str, 
    category_id: int, 
    ingredient_ids: str, 
    description: str, 
    cooking_time: int, 
    difficulty_level: int, 
    servings: str, 
    user_id: int=1, 
    db: Session = Depends(get_db)):
    try :
        user = db.query(models.User).filter(models.User.user_id==user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        recipe = models.Recipes(title=title, description=description, cooking_time=cooking_time, difficulty_level=difficulty_level, servings=servings, user_id=user_id)
        r = crud.create_recipe(db=db, recipe=recipe, user=user)
        # add recipecategories
        crud.create_recipe_category(db=db, recipe_id=r.recipe_id, category_id=category_id)
        # add recipeingredients
        for i in [int(x.strip()) for x in ingredient_ids.split(',')]:
            crud.create_recipe_ingredient(db=db, recipe_id=r.recipe_id, ingredient_id=i)
        rd = {
            'title': r.title,
            'description': r.description,
            'cooking_time': r.cooking_time,
            'difficulty_level': r.difficulty_level,
            'servings': r.servings,
            'category_id': category_id,
            'ingredient_ids': ingredient_ids,
            'recipe_id': r.recipe_id
        }
        return JSONResponse(content=jsonable_encoder(rd))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/recipes/{recipe_id}")
def read_recipes(recipe_id: int = 0, db: Session = Depends(get_db)):
    recipes = crud.get_recipe(db, recipe_id=recipe_id)
    if recipes is None:
        raise HTTPException(status_code=404, detail="Recipes not found")
    return recipes

@app.get("/recipes/")
def read_recipe(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    recipes = crud.get_recipes(db, skip=skip, limit=limit)
    return recipes

@app.put("/recipes/{recipe_id}")
def update_recipe(recipe_id: int, title: str = None, description: str = None, 
                  cooking_time: int = None, difficulty_level: int = None, servings: str = None, db: Session = Depends(get_db)):
    db_recipe = crud.update_recipe(db, recipe_id, title, description, cooking_time, difficulty_level, servings)
    if db_recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return db_recipe

@app.delete("/recipes/{recipe_id}")
def delete_recipe(recipe_id: int, db: Session = Depends(get_db)):
    # delete recipecategories
    crud.delete_recipe_category(db, recipe_id)
    # delete recipeingredients
    crud.delete_recipe_ingredient(db, recipe_id)
    success = crud.delete_recipe(db, recipe_id)
    if not success:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return {"message": "Recipe deleted successfully"}

    
# ------------------ingredients---------------
@app.post("/ingredients/")
def create_ingredient(name: str, unit: str, db: Session = Depends(get_db)):
    try :
        ingredient = models.Ingredients(name=name, unit=unit)

        return crud.create_ingredient(db=db, ingredient=ingredient)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/ingredients/{ingredient_id}")
def read_ingredients(ingredient_id: int = 0, db: Session = Depends(get_db)):
    db_ingredient = crud.get_ingredient(db, ingredient_id=ingredient_id)
    if db_ingredient is None:
        raise HTTPException(status_code=404, detail="ingredient not found")
    return db_ingredient

@app.get("/ingredients/")
def read_ingredient(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    ingredients = crud.get_ingredients(db, skip=skip, limit=limit)
    return ingredients

@app.delete("/ingredients/{ingredient_id}")
def delete_ingredient(ingredient_id: int, db: Session = Depends(get_db)):
    success = crud.delete_ingredient(db, ingredient_id)
    if not success:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    return {"message": "Ingredient deleted successfully"}



    
@app.post("/recipeingredients/")
def create_recipe_ingredient(quantity: str, recipe_id: int, ingredient_id: int, db: Session = Depends(get_db)):
    try :
        recipe = db.query(models.Recipes).filter(models.Recipes.recipe_id==recipe_id).first()
        if not recipe:
            raise HTTPException(status_code=404, detail="Recipe not found")
        
        ingredient = db.query(models.Ingredients).filter(models.Ingredients.ingredient_id==ingredient_id).first()
        if not ingredient:
            raise HTTPException(status_code=404, detail="Ingredient not found")
        
        recipe_ingredient = models.RecipeIngredients(quantity=quantity, recipe_id=recipe_id, ingredient_id=ingredient_id)

        return crud.create_recipe_ingredient(db=db, recipe_ingredient=recipe_ingredient, recipe=recipe, ingredient=ingredient)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/recipeingredients/")
def read_recipe_ingredients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    recipe_ingredients = crud.get_recipe_ingredients(db, skip=skip, limit=limit)
    if recipe_ingredients is None:
        raise HTTPException(status_code=404, detail="Recipe Ingredients not found")
    return recipe_ingredients

@app.get("/recipeingredients/{recipe_id}")
def read_recipe_ingredient(recipe_id: int = 0, db: Session = Depends(get_db)):
    recipe_ingredients = crud.get_recipe_ingredient(db, recipe_id=recipe_id)
    if recipe_ingredients is None:
        raise HTTPException(status_code=404, detail="Recipe Ingredients not found")
    return recipe_ingredients


@app.delete("/recipeingredients/{recipe_id}")
def delete_recipe_ingredient(recipe_id: int, db: Session = Depends(get_db)):
    success = crud.delete_recipe_ingredient(db, recipe_id)
    if not success:
        raise HTTPException(status_code=404, detail="Recipe category not found")
    return {"message": "Recipe category deleted successfully"}


@app.post("/ratings/")
def create_rating(score: int, comment: str, user_id: int, recipe_id: int, db: Session = Depends(get_db)):
    try :
        return crud.create_rating(db=db, score=score, comment=comment, user_id=user_id, recipe_id=recipe_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# @app.post("/savedrecipes/")
# def create_saved_recipe(user_id: int, recipe_id: int, db: Session = Depends(get_db)):
#     try :
#         user = db.query(models.User).filter(models.User.user_id==user_id).first()
#         if not user:
#             raise HTTPException(status_code=404, detail="User not found")
        
#         recipe = db.query(models.Recipes).filter(models.Recipes.recipe_id==recipe_id).first()
#         if not recipe:
#             raise HTTPException(status_code=404, detail="Recipe not found")
        
#         saved_recipe = models.SavedRecipes(user_id=user_id, recipe_id=recipe_id)

#         return crud.create_saved_recipe(db=db, saved_recipe=saved_recipe, user_id=user_id, recipe_id=recipe_id)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/userpreferences/")
def create_user_preference(user_id: int, category_id: int, db: Session = Depends(get_db)):
    try :
        return crud.create_user_preference(db=db, user_id=user_id, category_id=category_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# --------------recipe categories--------------
@app.post("/recipecategories/")
def create_recipe_category(recipe_id: int, category_id: int, db: Session = Depends(get_db)):
    try :
        return crud.create_recipe_category(db=db, recipe_id=recipe_id, category_id=category_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/recipecategories/{recipe_id}")
def read_recipe_category(recipe_id: int = 0, db: Session = Depends(get_db)):
    recipe_categories = crud.get_recipe_category(db, recipe_id=recipe_id)
    return recipe_categories
    
@app.get("/recipecategories/")
def read_recipe_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    recipe_categories = crud.get_recipe_categories(db, skip=skip, limit=limit)
    if recipe_categories is None:
        raise HTTPException(status_code=404, detail="Recipe Categories not found")
    return recipe_categories

@app.delete("/recipecategories/{recipe_id}")
def delete_recipe_category(recipe_id: int, db: Session = Depends(get_db)):
    success = crud.delete_recipe_category(db, recipe_id)
    if not success:
        raise HTTPException(status_code=404, detail="Recipe category not found")
    return {"message": "Recipe category deleted successfully"}
    
@app.post("/instructions/")
def create_instruction(step_number: int, description: str, recipe_id: int, db: Session = Depends(get_db)):
    try :
        recipe = db.query(models.Recipes).filter(models.Recipes.recipe_id==recipe_id).first()
        if not recipe:
            raise HTTPException(status_code=404, detail="Recipe not found")
        
        instruction = models.Instructions(step_number=step_number, description=description, recipe_id=recipe_id)

        return crud.create_instruction(db=db, instruction=instruction, recipe=recipe)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


# -------------------get-------------------










@app.get("/ratings/{rating_id}")
def read_ratings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    ratings = crud.get_ratings(db, skip=skip, limit=limit)
    if ratings is None:
        raise HTTPException(status_code=404, detail="Ratings not found")
    return ratings

# @app.get("/savedrecipes/")
# def read_saved_recipes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     saved_recipes = crud.get_saved_recipes(db, skip=skip, limit=limit)
#     if saved_recipes is None:
#         raise HTTPException(status_code=404, detail="Saved Recipes not found")
#     return saved_recipes

# @app.get("/userpreferences/")
# def read_user_preferences(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     user_preferences = crud.get_user_preferences(db, skip=skip, limit=limit)
#     if user_preferences is None:
#         raise HTTPException(status_code=404, detail="User Preferences not found")
#     return user_preferences



@app.get("/instructions/{instruction_id}")
def read_instructions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    instructions = crud.get_instructions(db, skip=skip, limit=limit)
    if instructions is None:
        raise HTTPException(status_code=404, detail="Instructions not found")
    return instructions

# -------------------get_all-------------------








@app.get("/ratings/")
def read_rating(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    ratings = crud.get_ratings(db, skip=skip, limit=limit)
    return ratings

# @app.get("/savedrecipes/")
# def read_saved_recipe(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     saved_recipes = crud.get_saved_recipes(db, skip=skip, limit=limit)
#     return saved_recipes

@app.get("/userpreferences/")
def read_user_preference(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    user_preferences = crud.get_user_preferences(db, skip=skip, limit=limit)
    return user_preferences



@app.get("/instructions/")
def read_instruction(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    instructions = crud.get_instructions(db, skip=skip, limit=limit)
    return instructions

# -------------------update-------------------
@app.put("/users/{user_id}")
def update_user(user_id: int, username: str = None, email: str = None, 
                password: str = None, db: Session = Depends(get_db)):
    db_user = crud.update_user(db, user_id, username, email, password)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.put("/categories/{category_id}")
def update_category(category_id: int, name: str = None, db: Session = Depends(get_db)):
    db_category = crud.update_category(db, category_id, name)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category


@app.put("/ingredients/{ingredient_id}")
def update_ingredient(ingredient_id: int, name: str = None, unit: str = None, db: Session = Depends(get_db)):
    db_ingredient = crud.update_ingredient(db, ingredient_id, name, unit)
    if db_ingredient is None:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    return db_ingredient

@app.put("/ratings/{rating_id}")
def update_rating(rating_id: int, score: int = None, comment: str = None, db: Session = Depends(get_db)):
    db_rating = crud.update_rating(db, rating_id, score, comment)
    if db_rating is None:
        raise HTTPException(status_code=404, detail="Rating not found")
    return db_rating

# @app.put("/savedrecipes/{saved_recipe_id}")
# def update_saved_recipe(saved_recipe_id: int, saved_at: str = None, db: Session = Depends(get_db)):
#     db_saved_recipe = crud.update_saved_recipe(db, saved_recipe_id, saved_at)
#     if db_saved_recipe is None:
#         raise HTTPException(status_code=404, detail="Saved recipe not found")
#     return db_saved_recipe

# @app.put("/userpreferences/{user_preference_id}")
# def update_user_preference(user_preference_id: int, preference_level: int = None, db: Session = Depends(get_db)):
#     db_user_preference = crud.update_user_preference(db, user_preference_id, preference_level)
#     if db_user_preference is None:
#         raise HTTPException(status_code=404, detail="User preference not found")
#     return db_user_preference

# @app.put("/recipecategories/{recipe_category_id}")
# def update_recipe_category(recipe_category_id: int, category_id: int = None, db: Session = Depends(get_db)):
#     db_recipe_category = crud.update_recipe_category(db, recipe_category_id, category_id)
#     if db_recipe_category is None:
#         raise HTTPException(status_code=404, detail="Recipe category not found")
#     return db_recipe_category

@app.put("/instructions/{instruction_id}")
def update_instruction(instruction_id: int, step_number: int = None, description: str = None, db: Session = Depends(get_db)):
    db_instruction = crud.update_instruction(db, instruction_id, step_number, description)
    if db_instruction is None:
        raise HTTPException(status_code=404, detail="Instruction not found")
    return db_instruction


# -------------------delete-------------------






@app.delete("/ratings/{rating_id}")
def delete_rating(rating_id: int, db: Session = Depends(get_db)):
    success = crud.delete_rating(db, rating_id)
    if not success:
        raise HTTPException(status_code=404, detail="Rating not found")
    return {"message": "Rating deleted successfully"}

# @app.delete("/savedrecipes/{saved_recipe_id}")
# def delete_saved_recipe(saved_recipe_id: int, db: Session = Depends(get_db)):
#     success = crud.delete_saved_recipe(db, saved_recipe_id)
#     if not success:
#         raise HTTPException(status_code=404, detail="Saved recipe not found")
#     return {"message": "Saved recipe deleted successfully"}

# @app.delete("/userpreferences/{user_preference_id}")
# def delete_user_preference(user_preference_id: int, db: Session = Depends(get_db)):
#     success = crud.delete_user_preference(db, user_preference_id)
#     if not success:
#         raise HTTPException(status_code=404, detail="User preference not found")
#     return {"message": "User preference deleted successfully"}



@app.delete("/instructions/{instruction_id}")
def delete_instruction(instruction_id: int, db: Session = Depends(get_db)):
    success = crud.delete_instruction(db, instruction_id)
    if not success:
        raise HTTPException(status_code=404, detail="Instruction not found")
    return {"message": "Instruction deleted successfully"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )