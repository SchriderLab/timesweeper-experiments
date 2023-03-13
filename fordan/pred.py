from tensorflow.keras.models import load_model 
import numpy as np
import pickle as pkl

data = pkl.load(open("/work/users/l/s/lswhiteh/timesweeper-experiments/simple_sims/better_benchmark/testing_data.pkl", 'rb'))

bp1_model = load_model("/work/users/l/s/lswhiteh/timesweeper-experiments/simple_sims/win_sizes/k51/win_size_sims/trained_models/Win_size_1_Timesweeper_Class_aft")
bp51_model = load_model("/work/users/l/s/lswhiteh/timesweeper-experiments/simple_sims/win_sizes/k51/win_size_sims/trained_models/Win_size_51_Timesweeper_Class_aft")

for i in range(5):
    np.savetxt(f"neuts/{i}_freqs.tsv", data["neut"][str(i)]["aft"].T, fmt='%1.2f')
    np.savetxt(f"ssvs/{i}_freqs.tsv", data["ssv"][str(i)]["aft"].T, fmt='%1.2f')
    np.savetxt(f"sdns/{i}_freqs.tsv", data["sdn"][str(i)]["aft"].T, fmt='%1.2f')
    
    np.savetxt(f"neuts/{i}_probs_51.tsv", bp51_model.predict(np.expand_dims(data["neut"][str(i)]["aft"], axis=0)), fmt='%1.3f')
    np.savetxt(f"neuts/{i}_probs_1.tsv", bp1_model.predict(np.swapaxes(np.expand_dims(data["neut"][str(i)]["aft"], axis=0), 0, 2)), fmt='%1.3f')

    np.savetxt(f"ssvs/{i}_probs_51.tsv", bp51_model.predict(np.expand_dims(data["ssv"][str(i)]["aft"], axis=0)), fmt='%1.3f')
    np.savetxt(f"ssvs/{i}_probs_1.tsv", bp1_model.predict(np.swapaxes(np.expand_dims(data["ssv"][str(i)]["aft"], axis=0), 0, 2)), fmt='%1.3f')

    np.savetxt(f"sdns/{i}_probs_51.tsv", bp51_model.predict(np.expand_dims(data["sdn"][str(i)]["aft"], axis=0)), fmt='%1.3f')
    np.savetxt(f"sdns/{i}_probs_1.tsv", bp1_model.predict(np.swapaxes(np.expand_dims(data["sdn"][str(i)]["aft"], axis=0), 0, 2)), fmt='%1.3f')
