from flask import Flask,render_template,request
import pickle
import numpy as np
import pandas as pd


top_products=pickle.load(open("./Models/top_products.pkl","rb"))
final_df=pickle.load(open("./Models/final_df.pkl","rb"))
similarity=pickle.load(open("./Models/similarity.pkl","rb"))
df=pickle.load(open("./Models/df.pkl","rb"))

print(len(top_products))

app=Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html",
                               title = [str(t)[:20] for t in top_products['title'].values],
                               imgurl=list(top_products['imgUrl'].values),
                               producturl=list(top_products['productURL'].values),
                               stars=list(top_products['stars'].values),
                               reviews=list(top_products['reviews'].values),
                               price=list(top_products['price'].values),
                               blm=list(top_products["boughtInLastMonth"].values),
                               cname=list(top_products["category_name"].values),
        )

@app.route("/recommend")
def recommend_ui():
    return render_template("recommend.html")


@app.route("/recommend_product",methods=["POST"])
def recommendProduct():
    userInput=request.form.get("recommend")
    index=np.where(df.index == userInput)[0][0]
    distances=similarity[index]
    similar_items=sorted(list(enumerate(distances)),key=lambda x:x[1],reverse=True)[1:6]
    data=[]
    for i in similar_items:
        li=[]
        temp_df=final_df[final_df["title"] == df.index[i[0]]]
        li.extend(list(temp_df["title"].values))
        li.extend(list(temp_df["imgUrl"].values))
        li.extend(list(temp_df["productURL"].values))
        li.extend(list(temp_df["stars"].values))
        li.extend(list(temp_df["reviews"].values))
        li.extend(list(temp_df["category_name"].values))
        data.append(li)
    return render_template("recommend.html",data=data)

                               

if __name__ == "__main__":
    app.run(debug=True)