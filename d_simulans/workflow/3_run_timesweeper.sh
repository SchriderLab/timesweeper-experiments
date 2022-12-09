####Unif

###Vel - non-rounded

#0 thresh
for i in aftInputsVelocity/*3R*
    do sbatch \
        --time=2:00:00 \
        --mem=16G \
        -c 4 \
        --partition=general \
        --constraint=rhel8 \
        --wrap="source activate blinx; conda activate blinx; \
            python find_sweeps_npz.py -i $i \
            -o unif_vel_0_thresh \
            --aft-model /pine/scr/l/s/lswhiteh/timesweeper-experiments/d_simulans/ts_simulans/trained_models/d_simulans_0_thresh_velocity_TimeSweeper_aft \
            -y d_simulans_config.-y" 
    done

#25 thresh
for i in aftInputsVelocity/*
    do sbatch \
        --time=1:00:00 \
        --mem=8G \
        -c 4 \
        --partition=general \
        --constraint=rhel8 \
        --wrap="source activate blinx; conda activate blinx; \
            python find_sweeps_npz.py -i $i \
            -o unif_vel_25_thresh \
            --aft-model /pine/scr/l/s/lswhiteh/timesweeper-experiments/d_simulans/ts_simulans/trained_models/d_simulans_25_thresh_velocity_TimeSweeper_aft \
            -y d_simulans_config.-y" 
    done

### Vel - rounded
#0 thresh
for i in aftInputsVelocityRounded/*
    do sbatch \
        --time=1:00:00 \
        --mem=8G \
        -c 4 \
        --partition=general \
        --constraint=rhel8 \
        --wrap="source activate blinx; conda activate blinx; \
            python find_sweeps_npz.py -i $i \
            -o unif_vel_0_thresh_rounded \
            --aft-model /pine/scr/l/s/lswhiteh/timesweeper-experiments/d_simulans/ts_simulans/trained_models/d_simulans_0_thresh_velocity_TimeSweeper_aft \
            -y d_simulans_config.-y" 
    done
    
#25 thresh
for i in aftInputsVelocityRounded/*
    do sbatch \
        --time=1:00:00 \
        --mem=8G \
        -c 4 \
        --partition=general \
        --constraint=rhel8 \
        --wrap="source activate blinx; conda activate blinx; \
            python find_sweeps_npz.py -i $i \
            -o unif_vel_25_thresh_rounded \
            --aft-model /pine/scr/l/s/lswhiteh/timesweeper-experiments/d_simulans/ts_simulans/trained_models/d_simulans_25_thresh_velocity_TimeSweeper_aft \
            -y d_simulans_config.-y" 
    done

####Unif
###Last
#0 thresh
for i in aftInputs/*
    do sbatch \
        --time=1:00:00 \
        --mem=8G \
        -c 4 \
        --partition=general \
        --constraint=rhel8 \
        --wrap="source activate blinx; conda activate blinx; \
            python find_sweeps_npz.py -i $i \
            -o unif_last_0_thresh \
            --aft-model /pine/scr/l/s/lswhiteh/timesweeper-experiments/d_simulans/ts_simulans/trained_models/d_simulans_0_thresh_last_TimeSweeper_aft \
            -y d_simulans_config.-y" 
    done

for i in aftInputs/*
    do sbatch \
        --time=1:00:00 \
        --mem=8G \
        -c 4 \
        --partition=general \
        --constraint=rhel8 \
        --wrap="source activate blinx; conda activate blinx; \
            python find_sweeps_npz.py -i $i \
            -o unif_vel_25_thresh \
            --aft-model /pine/scr/l/s/lswhiteh/timesweeper-experiments/d_simulans/ts_simulans/trained_models/d_simulans_25_thresh_vel_TimeSweeper_aft \
            -y d_simulans_config.-y" 
    done

###############################################

####LogUnif

###Vel - non-rounded

#0 thresh
for i in aftInputsVelocity/*
    do sbatch \
        --time=1:00:00 \
        --mem=8G \
        -c 4 \
        --partition=general \
        --constraint=rhel8 \
        --wrap="source activate blinx; conda activate blinx; \
            python find_sweeps_npz.py -i $i \
            -o logunif_vel_0_thresh \
            --aft-model /pine/scr/l/s/lswhiteh/timesweeper-experiments/d_simulans/ts_simulans/trained_models/d_simulans_log_uni_0_thresh_vel_TimeSweeper_aft \
            -y d_simulans_config.-y" 
    done

#25 thresh
for i in aftInputsVelocity/*
    do sbatch \
        --time=1:00:00 \
        --mem=8G \
        -c 4 \
        --partition=general \
        --constraint=rhel8 \
        --wrap="source activate blinx; conda activate blinx; \
            python find_sweeps_npz.py -i $i \
            -o logunif_vel_25_thresh \
            --aft-model /pine/scr/l/s/lswhiteh/timesweeper-experiments/d_simulans/ts_simulans/trained_models/d_simulans_log_uni_25_thresh_vel_TimeSweeper_aft \
            -y d_simulans_config.-y" 
    done

### Vel - rounded
#0 thresh
for i in aftInputsVelocityRounded/*
    do sbatch \
        --time=1:00:00 \
        --mem=8G \
        -c 4 \
        --partition=general \
        --constraint=rhel8 \
        --wrap="source activate blinx; conda activate blinx; \
            python find_sweeps_npz.py -i $i \
            -o logunif_vel_0_thresh_rounded \
            --aft-model /pine/scr/l/s/lswhiteh/timesweeper-experiments/d_simulans/ts_simulans/trained_models/d_simulans_log_uni_0_thresh_vel_TimeSweeper_aft \
            -y d_simulans_config.-y" 
    done
    
#25 thresh
for i in aftInputsVelocityRounded/*
    do sbatch \
        --time=1:00:00 \
        --mem=8G \
        -c 4 \
        --partition=general \
        --constraint=rhel8 \
        --wrap="source activate blinx; conda activate blinx; \
            python find_sweeps_npz.py -i $i \
            -o logunif_vel_25_thresh_rounded \
            --aft-model /pine/scr/l/s/lswhiteh/timesweeper-experiments/d_simulans/ts_simulans/trained_models/d_simulans_log_uni_25_thresh_vel_TimeSweeper_aft \
            -y d_simulans_config.-y" 
    done

####LogUnif
###Last
#0 thresh
for i in aftInputs/*
    do sbatch \
        --time=1:00:00 \
        --mem=8G \
        -c 4 \
        --partition=general \
        --constraint=rhel8 \
        --wrap="source activate blinx; conda activate blinx; \
            python find_sweeps_npz.py -i $i \
            -o logunif_last_0_thresh \
            --aft-model /pine/scr/l/s/lswhiteh/timesweeper-experiments/d_simulans/ts_simulans/trained_models/d_simulans_log_uni_0_thresh_last_TimeSweeper_aft \
            -y d_simulans_config.-y" 
    done

for i in aftInputs/*
    do sbatch \
        --time=1:00:00 \
        --mem=8G \
        -c 4 \
        --partition=general \
        --constraint=rhel8 \
        --wrap="source activate blinx; conda activate blinx; \
            python find_sweeps_npz.py -i $i \
            -o logunif_vel_25_thresh \
            --aft-model /pine/scr/l/s/lswhiteh/timesweeper-experiments/d_simulans/ts_simulans/trained_models/d_simulans_log_uni_25_thresh_vel_TimeSweeper_aft \
            -y d_simulans_config.-y" 
    done
