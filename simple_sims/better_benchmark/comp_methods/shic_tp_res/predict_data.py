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
agp.add_argument(
    "-s",
    "--scaler",
    dest="scaler",
    help="Minmax scaler used during the training process on selection coefficients",
    default="Benchmark_selcoeff_scaler.pkl",
)

ua = agp.parse_args()

class_model = load_model(ua.class_model)

if "ssv" in ua.reg_model:
    ssv_model = load_model(ua.reg_model)
    sdn_model = load_model(str(ua.reg_model).replace("ssv", "sdn"))
elif "sdn" in ua.reg_model:
    ssv_model = load_model(str(ua.reg_model).replace("sdn", "ssv"))
    sdn_model = load_model(ua.reg_model)


pikl_dict = pkl.load(open(ua.input_data, "rb"))

d = np.stack(pikl_dict["data"])
class_probs = class_model.predict(d)
pikl_dict["pred_class"] = np.argmax(class_probs, axis=1)
pikl_dict["neut_prob"] = class_probs[:, 0].flatten()
pikl_dict["sdn_prob"] = class_probs[:, 1].flatten()
pikl_dict["ssv_prob"] = class_probs[:, 2].flatten()


raw_sdn_s = sdn_model.predict(d)
raw_ssv_s = ssv_model.predict(d)

scaler = pkl.load(open(ua.scaler, "rb"))
sdn_s = scaler.inverse_transform(raw_sdn_s).squeeze()
ssv_s = scaler.inverse_transform(raw_ssv_s).squeeze()
print(sdn_s.shape)

pikl_dict["sdn_pred_s"] = sdn_s
pikl_dict["ssv_pred_s"] = ssv_s


del pikl_dict["data"]
pd.DataFrame(pikl_dict).to_csv("TP_SHIC_res.csv", index=False)
