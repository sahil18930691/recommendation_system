from fastapi import FastAPI, Body
from typing import Annotated
from typing import Optional
from pydantic import BaseModel
from fastapi import Query
import uvicorn
import pickle
import pandas as pd

class recommend:
    import pickle
    import pandas as pd
    import numpy as np
    
    global data,combined_features
    data = pd.read_pickle("my_data2.pkl")
    # Get the item feature matrix
    combined_features = np.vstack(data["combined_vector"])

    # Define a function to find the top-k products that are most similar to a given product
    def find_similar_products(product_id, k):
        import pandas as pd
        import numpy as np
    # Import sklearn and other libraries
        import sklearn
        from sklearn.metrics.pairwise import cosine_similarity

        if product_id==None:
            return{"Error":"Sorry, the input product id and matched product id could not be found for this title and category"}
        
        # Get the index of the product in the data
        index = data[data["product_id"] == product_id].index[0]
        
        indexlist = data[data["product_id"] == product_id].index.tolist()[1:] 

        data2 = data.drop(index=indexlist)
        
        # Get the item feature matrix
        combined_features = np.vstack(data2["combined_vector"])
        # Get the vector of the product
        vector = combined_features[index]
        
        # Compute the cosine similarity between the product vector and all the other vectors
        similarities = sklearn.metrics.pairwise.cosine_similarity(vector.reshape(1,-1), combined_features)[0]
        
         # Sort the similarities in descending order and get the indices of the top-k products
        indices = np.argsort(similarities)[::-1][:k]
        
        df = data2[["product_id", "product_title", "rating", "unix_review_time","help_prop", "salesrank","category","clean_text","imgurl"]].iloc[indices]
        df["similarity"] = similarities[indices]
        df["similarity"] = df['similarity'].round(decimals = 3)
        
    # Sort the data by rating
        df = df.sort_values('rating', ascending=False)
    # Convert to dictionary preserving the order of rows    
        df = df.to_dict('records')
  # Return the names of the top-k products
        return df

app = FastAPI()

class Product(BaseModel):
    product_title: str
    category : str
                      
@app.get("/{product_id}")
def get_recommendations_by_product_id(product_id : str): #product_id : str , prod : Annotated[Product_id,Body(examples = example_id)]
    '''Some Product IDs : B009RSSMBU , B008Z0QG5A , B0054MZGTO , B00D4L2D6Q , B004S92MIW '''
    product_id = product_id.strip()
    try:
        rows = data[data['product_id'] == product_id].values[0]     
    except:
        # this means there are no matches in the dataframe
        return {"Error":"Sorry, no product found for this product id"}
    
    return recommend.find_similar_products(product_id,5)

global example
example={
                "1": {
                  "summary": "A normal example 1",
                    "value": {
                                "product_title": "La Leela Men's Hawaiian Print Shirt",
                                "category": "casual button down shirts"
                             },
                     },
                
                "2": {
                    "summary": "A normal example 2",
                    "value": {
                                "product_title": "Reyn Spooner Men's Christmas Commemorative Shirt",
                                "category": "casual button down shirts"
                             },
                     },
                "3": {
                    "summary": "A normal example 3",
                    "value": {
                                "product_title": "Men's Short Sleeve Rayon Hawaiian Tropical Pattern Shirts",
                                "category": "casual button down shirts"
                             },
                     },
                "4": {
                    "summary": "A normal example 4",
                    "value": {
                                "product_title": "Parrot Hawaiian Shirt",
                                "category": "casual button down shirts"
                             },
                     },
                "5": {
                    "summary": "A normal example 5",
                    "value": {
                                "product_title": "Cubavera Men's Short Sleeve Rayon Hawaiian Printed Color Block Shirt, Blue, Small",
                                "category": "casual button down shirts"
                             },
                     }
            }

@app.post("/{product_title}/{category}")
def get_recommendations_by_product_details(prod : Annotated[Product,Body(examples = example)]): #prodproduct_title : str,category : str

    try:
        product_id = data.loc[(data['product_title'] == prod.product_title) & (data['category'] == prod.category), 'product_id'].values[0]     
    except IndexError:
        # this means there are no matches in the dataframe
        return {"Error":"Sorry, no product found for this title and category"}
    return recommend.find_similar_products(product_id,5)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)    