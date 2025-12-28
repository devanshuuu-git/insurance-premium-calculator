from fastapi import FastAPI
from fastapi.responses import JSONResponse
from schema import response_model
from schema.model import UserInput
from MLmodel.predict import predict_output, MODEL_VERSION, model
from schema.response_model import ResponseModel

app = FastAPI()

@app.get("/")
def home():
    return {'message':'Insurance Premium Prediction API'}

@app.get("/health")
def health_check():
    return {
        'status':'OK',
        'version': MODEL_VERSION,
        'model_loaded': model is not None
    }

@app.post("/predict")
def predict_premium(data: UserInput):

    user_input={
        'bmi':data.bmi,
        'age_group':data.age_group,
        'lifestyle_risk':data.lifestyle_risk,
        'city_tier':data.city_tier,
        'income_lpa':data.income_lpa,
        'occupation':data.occupation
    }

    prediction = predict_output(user_input, response_model=ResponseModel)

    try:
        return JSONResponse(status_code=200, content={'response': prediction})
    except Exception as e:
        return JSONResponse(status_code=500, content=str(e))
