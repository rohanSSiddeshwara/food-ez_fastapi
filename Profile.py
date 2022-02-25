from fastapi import FastAPI
import pandas as pd
from typing import Optional
app=FastAPI()

@app.get("/")
def index():
    return {"Hello": "World"}

@app.get("/Profile/")
def user_profile(user_name:str):
    data=pd.read_csv("data_sets/Users.csv")
    if len(data[data['User_Name']==user_name])==0:
        return {"Error":"User not found"}
    else:
        return data[data['User_Name']==user_name].to_dict()

@app.post('/Profile/create-user')
def create_user(user_name:str,user_fname:str,user_lname:str,user_email:str,user_phone:str,user_password:str):
    data=pd.read_csv("data_sets/Users.csv")
    if len(data[data['User_Name']==user_name])!=0:
        return {"Error":"User already exists"}
    else:
        record={'User_Name':[user_name],
                'First_Name': [user_fname],
                'Last_Name': [user_lname],
                'Email': [user_email],
                'Phone_Number':[user_phone],
                'Password': [user_password]}
        record=pd.DataFrame(record)
        data=data.append(record,ignore_index=True)
        data.to_csv("data_sets/Users.csv",index=False)
        if len(data[data['User_Name']==user_name])!=0:
            return {"Success":"User created"}


@app.put('/Profile/update-user/{user_name}')
def update_user(user_name:str,user_fname:Optional[str]=None,user_lname:Optional[str]=None,user_email:Optional[str]=None,user_phone:Optional[str]=None,user_password:Optional[str]=None):
    data=pd.read_csv("data_sets/Users.csv")
    if len(data[data['User_Name']==user_name])==0:
        return {"Error":"User not found"}
    else:
        if user_fname!=None:
            data.loc[data['User_Name']==user_name,'First_Name']=user_fname
        if user_lname!=None:
            data.loc[data['User_Name']==user_name,'Last_Name']=user_lname
        if user_email!=None:
            data.loc[data['User_Name']==user_name,'Email']=user_email
        if user_phone!=None:
            data.loc[data['User_Name']==user_name,'Phone_Number']=user_phone
        if user_password!=None:
            data.loc[data['User_Name']==user_name,'Password']=user_password
        data.to_csv("data_sets/Users.csv",index=False)

        return {"Success":"User updated"}
