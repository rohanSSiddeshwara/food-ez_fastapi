from datetime import date, time
from fastapi import FastAPI
import pandas as pd
from typing import Optional
import razorpay

key_id="rzp_test_K4MJfjm368c8s7"
key_secret="NUBqtflhYsaUU2LoN8SoGqXh"

app=FastAPI()

# @app.get("/orders")
# def read_orders():
#     orders = pd.read_csv("data_sets/Orders.csv")
#     return orders.to_dict(orient="records")

@app.get("/orders/users/{user_name}")
def read_orders_username(user_name: str):
    data=pd.read_csv("data_sets/Orders.csv",parse_dates=True)
    return data.loc[data["User_Name"]==user_name].to_dict(orient='index')


# @app.get("/orders/canteen/{canteen_name}")
# def read_orders_canteen(canteen_name: str):
#     data=pd.read_csv("data_sets/Orders.csv",parse_dates=True)
#     return data.loc[data["Canteen_Name"]==canteen_name].to_dict(orient='index')

# @app.get("/orders/date/{date}")
# def read_orders_date(date: str):
#     data=pd.read_csv("Orders.csv",parse_dates=True)
#     return data.loc[data["Date"]==date].to_dict(orient='index')

@app.post("/orders/create")
def create_orders(User_Name:str,Food_id:int,Quantity:int,Price:float,Payment_id:str,Payment_Status:str,Order_Status:str,Canteen_Name:str): 
    data=pd.read_csv("data_sets/Orders.csv")
    if len(data[data["Payment_id"]==Payment_id])!=0:
        return {"message":"Payment failed"}
    else:
        lenght=len(data)
        record={'Order_id':[len(data)+1],
            'User_Name':[User_Name],
            'Food_id':[Food_id],
            'Quantity':[Quantity],
            'Price':[Price],
            'Payment_id':[Payment_id],
            'Payment_Status':[Payment_Status],
            'Order_Status':[Order_Status],
            'Canteen_Name':[Canteen_Name]}
        record=pd.DataFrame(record)
        data=data.append(record,ignore_index=True)
        data.to_csv("data_sets/Orders.csv",index=False)
    if len(data)>lenght:
        return {"message":"Order created successfully"}

@app.get("/orders/pay")
def pay():
    data = { "amount": 500, "currency": "INR", "receipt": "testing_1" }
    client = razorpay.Client(auth=(key_id, key_secret))
    global payment
    payment = client.order.create(data=data)
    return payment    



# @app.put("/orders/update/")
# def update_orders(Order_id:int,Order_Status:str):
#     data=pd.read_csv("data_sets/Orders.csv",parse_dates=True)
#     if len(data[data["Order_id"]==Order_id])==0:
#         return {"message":"Order not found"}
#     else:
#         data.loc[data["Order_id"]==Order_id,"Order_Status"]=Order_Status
#         data.to_csv("data_sets/Orders.csv",index=False)
#         return {"message":"Order updated successfully"}