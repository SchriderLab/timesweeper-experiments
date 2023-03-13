cd ..
for i in FreqInputs/aftInputsVelocity/*
do
    sbatch --time=1:00:00 --mem=8G -c 4 --wrap="\
    python workflow/find_sweeps_npz.py \
        -i $i \
        -o d_simulans_output/ \
        --class-model ts_simulans/trained_models/d_simulans_Timesweeper_Class_aft/ \
        --reg-model ts_simulans/trained_models/REG_d_simulans_ssv_minmax_Timesweeper_Reg_aft/ \
        --scaler ts_simulans/d_simulans_selcoeff_scaler.pkl \
        "
done