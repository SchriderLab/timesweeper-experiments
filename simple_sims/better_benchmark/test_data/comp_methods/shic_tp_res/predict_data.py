import argparse as ap
import os
import pickle as pkl

import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
from tqdm import tqdm

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"


agp = ap.ArgumentParser(
    formatter_class=ap.ArgumentDefaultsHelpFormatter,
)
agp.add_argument(
    "-i",
    "--input-data",
    dest="input_data",
    help="Pickle file containing time-series Timesweeper feature vectors.",
)
agp.add_argument(
    "-cm",
    "--trained-class-model",
    dest="class_model",
    help="Trained Keras classification model to use for prediction.",
)
agp.add_argument(
    "-rm",
    "--trained-reg-model",
    dest="reg_model",
    help="Trained Keras regression model to use for prediction. Either SSV or SDN work.",
)

ua = agp.parse_args()

class_model = load_model(ua.class_model)

if "ssv" in ua.reg_model:
    ssv_model = load_model(ua.reg_model)
    sdn_model = load_model(str(ua.reg_model).replace("ssv", "sdn"))
elif "sdn" in ua.reg_model:
    ssv_model = load_model(str(ua.reg_model).replace("ssv", "sdn"))
    sdn_model = load_model(ua.reg_model)

sweep_list = []
rep_list = []
data_list = []
sel_coeffs = []
sweep_types = []
pikl_dict = pkl.load(open(ua.input_data, "rb"))
for sweep in pikl_dict.keys():
    sweep_types.append(sweep)
    for rep in pikl_dict[sweep].keys():
        try:
            data_list.append(np.array(pikl_dict[sweep][rep][data_type.lower()]))
        except:
            continue

        sweep_list.append(sweep)
        rep_list.append(rep)
        sel_coeffs.append(pikl_dict[sweep][rep]["sel_coeff"])

pred_classes = []
pred_s = []

for d in tqdm(data_list):
    pred_class = class_model.predict(d)
    pred_classes.append(pred_class)

    if pred_class == 1:
        pred_s.append(sdn_model.predict(d))
    elif pred_class == 2:
        pred_s.append(ssv_model.predict(d))
    else:
        pred_s.append(0.0)


pd.DataFrame(
    {
        "rep": rep_list,
        "sweep": sweep_list,
        "pred_sweep": pred_classes,
        "s_val": sel_coeffs,
        "pred_s": pred_s,
    }
).to_csv("Timesweeper_res.csv")
