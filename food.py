
from tokenize import Double
from fastapi import FastAPI,Body
import pandas as pd
from typing import Optional
import razorpay
from pydantic import BaseModel


key_id="rzp_test_K4MJfjm368c8s7"
key_secret="NUBqtflhYsaUU2LoN8SoGqXh"
app=FastAPI()

class Item(BaseModel):
    amount:str
    user_name:str

class Ver_Item(BaseModel):
    payment_id:str
    order_id: str
    signature:str 

class Order(BaseModel):
    user_name:str
    food_name: str
    canteen_name:str
    price: str
    quantity: str
    total_price: str
    payment_id: str
    order_id: str
    signature: str


client = razorpay.Client(auth=(key_id, key_secret))

@app.get("/")
def index():
    return {"Hello": "World"}

@app.post("/orders/pay")
def pay(item:Item):
    data = { "amount": (float(item.amount)*100), "currency": "INR", "receipt": "testing_1" ,"notes": {"User_name": item.user_name} }
    global payment
    payment = client.order.create(data=data)
    return payment

@app.post("/orders/status")
def pay_status(item:Ver_Item):
    params_dict = {
    'razorpay_order_id': item.order_id,
    'razorpay_payment_id': item.payment_id,
    'razorpay_signature': item.signature
    }
    client.utility.verify_payment_signature(params_dict)
    return {"message":"Payment Successful"}

@app.post("/orders/create")
async def create_order(item:Order):
    data=pd.read_csv("data_sets/Orders.csv")
    lenght=len(data)
    record={ "user_name": [item.user_name],
        "food_name": [item.food_name],
        "canteen_name": [item.canteen_name],
        "price": [float(item.price)],
        "quantity": [int(item.quantity)],
        "total_price": [float(item.total_price)],
        "payment_id": [item.payment_id],
        "order_id": [item.order_id],
        "signature": [item.signature]}
    record=pd.DataFrame(record)
    data=pd.concat([data,record])
    data.to_csv("data_sets/Orders.csv",index=False)
    if len(data)>lenght:
        return {"message":"Order created successfully"}
    else:
        return {"message":"Order not created"}

@app.get("/orders/users/{user_name}")
def read_orders_username(user_name: str):
    data=pd.read_csv("data_sets/Orders.csv",parse_dates=True)
    return data.loc[data["user_name"]==user_name][["user_name","food_name","canteen_name","price","quantity","total_price"]].to_dict(orient='index')

@app.get("/food")
def food():
    data=pd.read_csv("data_sets/food.csv")
    return data.to_dict(orient='index')

@app.get("/food/canteen")
def canteen(canteen:str):
    data=pd.read_csv("data_sets/food.csv")
    data = data.fillna('')
    if len(data[data["Canteen_Name"]==canteen])==0:
        return {"Food": "Not Found"}
    else:
        return data[data["Canteen_Name"]==canteen].to_dict(orient="index")

@app.get("/food/food_category")
def food_category(food_category:str):
    data=pd.read_csv("data_sets/food.csv")
    if len(data[data["Food_Cat"]==food_category])==0:
        return {"Food": "Not Found"}
    else:
        return data[data["Food_Cat"]==food_category].to_dict(orient="index")

@app.get("/food/food_type")
def food_type(food_type:str):
    data=pd.read_csv("data_sets/food.csv")
    data = data.fillna('')
    if len(data[data["Food_Type"]==food_type])==0:
        return {"Food": "Not Found"}
    else:
        return data[data["Food_Type"]==food_type].to_dict(orient="index")

@app.post("/food/create-food")
def create_food(food_name:str,canteen_name:str,food_price:str,food_type:str,food_category:str,food_description:str):
    data=pd.read_csv("data_sets/food.csv")
    if len(data[data["Food_Name"]==food_name])!=0:
        return {"Error":"Food already exists"}
    else:
        record={'Food_Id':[len(data)+1],
                'Food_Name':[food_name],
                'Food_Price': [food_price],
                'Canteen_Name': [canteen_name],
                'Food_Type': [food_type],
                'Food_Cat':[food_category],
                'Food_Description': [food_description],
                }
        record=pd.DataFrame(record)
        data=data.append(record,ignore_index=True)
        data.to_csv("data_sets/food.csv",index=False)
        if len(data[data["Food_Name"]==food_name])!=0:
            return {"Success":"Food created"}

@app.put("/food/update-food/{food_id}")
def update_food(food_id:int,food_name:Optional[str]=None,canteen_name:Optional[str]=None,food_price:Optional[str]=None,food_type:Optional[str]=None,food_category:Optional[str]=None,food_description:Optional[str]=None):
    data=pd.read_csv("data_sets/food.csv")
    if len(data[data["Food_Id"]==food_id])==0:
        return {"Error":"Food does not exist"}
    else:
        if food_name != None:
            data.loc[data["Food_Id"]==food_id,"Food_Name"]=food_name
        if canteen_name != None:
            data.loc[data["Food_Id"]==food_id,"Canteen_Name"]=canteen_name
        if food_price != None:
            data.loc[data["Food_Id"]==food_id,"Food_Price"]=food_price
        if food_type != None:
            data.loc[data["Food_Id"]==food_id,"Food_Type"]=food_type
        if food_category != None:
            data.loc[data["Food_Id"]==food_id,"Food_Cat"]=food_category
        if food_description != None:
            data.loc[data["Food_Id"]==food_id,"Food_Description"]=food_description
        data.to_csv("data_sets/food.csv",index=False)
        return {"Success":"Food updated"}

