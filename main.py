from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
import pickle

model_pkl_file="QuadraticDiscriminant_6Params.pkl"

with open(model_pkl_file, 'rb') as file:  
    clf = pickle.load(file)
    
app = FastAPI()

@app.get("/")
async def index():
   return {"message": "Hello World"}
if __name__ == "__main__":
   uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

class request_body(BaseModel):
    bounce_last12 : int
    bounce_when_pay : int
    age_during_loan : int
    days_pass_30 : int
    days_pass_60 : int
    days_pass_90 : int
    
@app.post('/predict')
def predict(data : request_body):
    # Making the data in a form suitable for prediction
    test_data = [[
            data.bounce_last12,
            data.bounce_when_pay,
            data.age_during_loan,
            data.days_pass_30,
            data.days_pass_60,
            data.days_pass_90
            
    ]]
     
    # Predicting the Class
    ans = clf.predict_proba(test_data)[0][1]*100
     
    # Return the Result
    return {ans}