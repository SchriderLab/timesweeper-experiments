import argparse as ap
import os
import pickle as pkl

import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
from tqdm import tqdm
from sklearn.preprocessing import MinMaxScaler

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"


agp = ap.ArgumentParser(
    formatter_class=ap.ArgumentDefaultsHelpFormatter,
)
agp.add_argument(
    "-i",
    "--input-data",
    dest="input_data",
    help="Pickle file containing time-series Timesweeper feature vectors.",
    default="/work/users/l/s/lswhiteh/timesweeper-experiments/simple_sims/better_benchmark/testing_data.pkl",
)
agp.add_argument(
    "-cm",
    "--trained-class-model",
    dest="class_model",
    help="Trained Keras classification model to use for prediction.",
    default="/work/users/l/s/lswhiteh/timesweeper-experiments/simple_sims/misspec/bottleneck_demo/bottleneck/trained_models/Bottleneck_Timesweeper_Class_aft",
)
agp.add_argument(
    "-rm",
    "--trained-reg-model",
    dest="reg_model",
    help="Trained Keras regression model to use for prediction. Either SSV or SDN work.",
    default="/work/users/l/s/lswhiteh/timesweeper-experiments/simple_sims/misspec/bottleneck_demo/bottleneck/trained_models/REG_Bottleneck_sdn_minmax_Timesweeper_Reg_aft",
)
agp.add_argument(
    "-s",
    "--scaler",
    dest="mm_scaler",
    help="MinMax Scaler used during model training.",
    default="/work/users/l/s/lswhiteh/timesweeper-experiments/simple_sims/misspec/bottleneck_demo/bottleneck/Bottleneck_selcoeff_scaler.pkl",
)
agp.add_argument(
    "-o",
    "--outfile",
    dest="outfile",
    help="File to write results to.",
    default="timesweeper_res.csv",
)

ua = agp.parse_args()

class_model = load_model(ua.class_model)

if "ssv" in ua.reg_model:
    ssv_model = load_model(ua.reg_model)
    sdn_model = load_model(str(ua.reg_model).replace("ssv", "sdn"))
elif "sdn" in ua.reg_model:
    ssv_model = load_model(str(ua.reg_model).replace("sdn", "ssv"))
    sdn_model = load_model(ua.reg_model)


if "aft" in ua.class_model.lower():
    data_type = "aft"
elif "hft" in ua.class_model.lower():
    data_type = "hft"

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
            data_list.append(np.expand_dims(np.array(pikl_dict[sweep][rep][data_type]), 0))
            sweep_list.append(sweep)
            rep_list.append(rep)
            sel_coeffs.append(pikl_dict[sweep][rep]["sel_coeff"])
        except:
            pass

data_arr = np.concatenate(data_list, axis=0)
class_probs = class_model.predict(data_arr)
pred_class = np.argmax(class_probs, axis=1)

raw_sdn_s = sdn_model.predict(data_arr)
raw_ssv_s = ssv_model.predict(data_arr)


scaler = pkl.load(open(ua.mm_scaler, "rb"))
sdn_s = scaler.inverse_transform(raw_sdn_s).squeeze()
ssv_s = scaler.inverse_transform(raw_ssv_s).squeeze()

pd.DataFrame(
    {
        "rep": rep_list,
        "sweep": sweep_list,
        "pred_sweep": pred_class,
        "neut_prob": [i[0] for i in class_probs],
        "sdn_prob": [i[1] for i in class_probs],
        "ssv_prob": [i[2] for i in class_probs],
        "s_val": sel_coeffs,
        "sdn_sval": sdn_s,
        "ssv_sval": ssv_s,
    }
).to_csv(ua.outfile, index=False)
