@app.post("/recipes/")
# def create_recipe(title: str, description: str, user_id: int, db: Session = Depends(get_db)):
#     recipe = models.Recipes(title=title, description=description, user_id=user_id)
#     return crud.create_recipe(db=db, recipe=recipe)

# @app.get("/recipes/{recipe_id}")
# def read_recipe(recipe_id: int, db: Session = Depends(get_db)):
#     db_recipe = crud.get_recipe(db, recipe_id=recipe_id)
#     if db_recipe is None:
#         raise HTTPException(status_code=404, detail="Recipe not found")
#     return db_recipe