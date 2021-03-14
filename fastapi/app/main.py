from fastapi import FastAPI, UploadFile, File
from starlette.responses import JSONResponse
from joblib import load
import pandas as pd
import numpy as np
import torch

app = FastAPI()

sc = load('../models/standard_scaler.joblib')
brewery_name_encoder = load('../models/brewery_name_encoder.joblib')
beer_style_encoder = load('../models/beer_style_encoder.joblib')
# nn_model = torch.load('../models/neural_net_final_assignment.pt', encoding='ascii')
nn_model = torch.load('../models/neural_net_final_assignment.pt')
nn_model.eval()


@app.get("/")
def read_root():
    desc = "Beer Style Prediction Assignment!!"
    return desc


@app.get('/health', status_code=200)
def healthcheck():
    return 'Beer Prediction is all ready to go!'


@app.get("/model/architecture/")
def architecture():
    return nn_model


def format_features(breweryname: str, reviewaroma: float, reviewappearance: float, reviewpalate: float,
                    reviewtaste: float):
    b_name = brewery_name_encoder.transform(np.array(breweryname).reshape(-1, 1).ravel())
    scaler_val = [reviewaroma, reviewappearance, reviewpalate, reviewtaste]
    arr = np.array(scaler_val).reshape(1, -1)
    scaled_val = sc.transform(arr)
    return {
        'brewery_name_encoded': b_name.tolist()
        , 'review_aroma': scaled_val[:, 0].tolist()
        , 'review_appearance': scaled_val[:, 1].tolist()
        , 'review_palate': scaled_val[:, 2].tolist()
        , 'review_taste': scaled_val[:, 3].tolist()
    }


@app.get("/beer/type/")
def predict(breweryname: str, reviewaroma: float, reviewappearance: float, reviewpalate: float, reviewtaste: float):
    print(breweryname)
    print(reviewaroma)
    print(reviewappearance)
    print(reviewpalate)
    print(reviewtaste)
    features = format_features(breweryname, reviewaroma, reviewappearance, reviewpalate, reviewtaste)
    print(features)
    obs = torch.Tensor(pd.DataFrame(features).values)
    print(obs)
    pred = nn_model(obs)
    print('Class')
    print(np.argmax(pred.detach().numpy()))
    print(pred)
    print(beer_style_encoder.inverse_transform([np.argmax(pred.detach().numpy())]).tolist())
    return JSONResponse(beer_style_encoder.inverse_transform([np.argmax(pred.detach().numpy())]).tolist())


@app.post("/beers/type/")
async def upload_csv(csv_file: UploadFile = File(...)):
    contents = await csv_file.read()
    data = contents.decode('utf-8-sig').splitlines()
    print(data)
    df_cleaned = pd.DataFrame([sub.split(",") for sub in data],
                              columns=['brewery_name', 'review_aroma', 'review_appearance', 'review_palate',
                                       'review_taste'])
    # df_cleaned.columns = df_cleaned.iloc[0]
    # df_cleaned = df_cleaned.drop(df_cleaned.index[0])
    print(df_cleaned.columns)
    num_cols = ['review_aroma', 'review_appearance', 'review_palate', 'review_taste']
    df_cleaned[num_cols] = sc.transform(df_cleaned[num_cols])
    print(df_cleaned)
    df_cleaned['brewery_name_encoded'] = brewery_name_encoder.transform(df_cleaned['brewery_name'])
    print(df_cleaned)
    df_cleaned = df_cleaned.drop(['brewery_name'], axis=1)
    print(df_cleaned)
    df_cleaned = df_cleaned.astype(np.float64)
    print(df_cleaned.info())
    obs = torch.Tensor(df_cleaned.values)
    print(obs)
    pred_multiple = nn_model(obs)
    output = []
    for a in pred_multiple.detach().numpy().tolist():
        print(a)
        print(beer_style_encoder.inverse_transform([np.argmax(a)]).tolist())
        output.append(beer_style_encoder.inverse_transform([np.argmax(a)]).tolist())
    print(output)
    return output
