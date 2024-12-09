from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "user"
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(45))
    email = Column(String(100))
    password = Column(String(45))
    created_at = Column(String(45), default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

class Categories(Base):
    __tablename__ = "categories"
    category_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(45))

class Recipes(Base):
    __tablename__ = "recipes"
    recipe_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100))
    description = Column(String(1000))
    cooking_time = Column(Integer)
    difficulty_level = Column(Integer)
    servings = Column(Integer)
    image_url = Column(String(2024))
    created_at = Column(String(45))
    user_id = Column(Integer, ForeignKey("user.user_id"))

class Ingredients(Base):
    __tablename__ = "ingredients"
    ingredient_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    unit = Column(String(100))

class RecipeIngredients(Base):
    __tablename__ = "recipe_ingredients"
    quantity = Column(String(45))
    recipe_id = Column(Integer, ForeignKey("recipes.recipe_id"), primary_key=True)
    ingredient_id = Column(Integer, ForeignKey("ingredients.ingredient_id"), primary_key=True)

class Ratings(Base):
    __tablename__ = "ratings"
    rating_id = Column(Integer, primary_key=True, index=True)
    score = Column(Integer)
    comment = Column(String(45))
    created_at = Column(String(45), default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    user_id = Column(Integer, ForeignKey("user.user_id"))
    recipe_id = Column(Integer, ForeignKey("recipes.recipe_id"))

# class SavedRecipes(Base):
#     __tablename__ = "saved_recipes"
#     saved_at = Column(String(45), default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
#     user_id = Column(Integer, ForeignKey("user.user_id"), primary_key=True)
#     recipe_id = Column(Integer, ForeignKey("recipes.recipe_id"), primary_key=True)

class UserPreferences(Base):
    __tablename__ = "user_preferences"
    preference_level = Column(Integer)
    user_id = Column(Integer, ForeignKey("user.user_id"), primary_key=True)
    category_id = Column(Integer, ForeignKey("categories.category_id"), primary_key=True)

class RecipeCategories(Base):
    __tablename__ = "recipe_categories"
    recipe_id = Column(Integer, ForeignKey("recipes.recipe_id"), primary_key=True)
    category_id = Column(Integer, ForeignKey("categories.category_id"), primary_key=True)

class Instructions(Base):
    __tablename__ = "instructions"
    instruction_id = Column(Integer, primary_key=True, index=True)
    step_number = Column(Integer)
    description = Column(String(1024))
    recipe_id = Column(Integer, ForeignKey("recipes.recipe_id"))

# 관계 설정
User.recipes = relationship("Recipes", back_populates="user")
User.ratings = relationship("Ratings", back_populates="user")
# User.saved_recipes = relationship("SavedRecipes", back_populates="user")
User.preferences = relationship("UserPreferences", back_populates="user")

Recipes.user = relationship("User", back_populates="recipes")
Recipes.ratings = relationship("Ratings", back_populates="recipe")
Recipes.recipe_ingredients = relationship("RecipeIngredients", back_populates="recipe")
Recipes.instructions = relationship("Instructions", back_populates="recipe")
# Recipes.saved_recipes = relationship("SavedRecipes", back_populates="recipe")
Recipes.recipe_categories = relationship("RecipeCategories", back_populates="recipe")

Ingredients.recipe_ingredients = relationship("RecipeIngredients", back_populates="ingredient")

Categories.recipe_categories = relationship("RecipeCategories", back_populates="category")
Categories.user_preferences = relationship("UserPreferences", back_populates="category")

RecipeIngredients.recipe = relationship("Recipes", back_populates="recipe_ingredients")
RecipeIngredients.ingredient = relationship("Ingredients", back_populates="recipe_ingredients")

Ratings.user = relationship("User", back_populates="ratings")
Ratings.recipe = relationship("Recipes", back_populates="ratings")

# SavedRecipes.user = relationship("User", back_populates="saved_recipes")
# SavedRecipes.recipe = relationship("Recipes", back_populates="saved_recipes")

UserPreferences.user = relationship("User", back_populates="preferences")
UserPreferences.category = relationship("Categories", back_populates="user_preferences")

RecipeCategories.recipe = relationship("Recipes", back_populates="recipe_categories")
RecipeCategories.category = relationship("Categories", back_populates="recipe_categories")

Instructions.recipe = relationship("Recipes", back_populates="instructions")