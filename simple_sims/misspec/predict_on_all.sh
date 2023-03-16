#!/usr/bin/bash

for data_type in aft hft
do
    ### Bottleneck Model

    # Bottleneck on Bottleneck
    python predict_data.py -i bottleneck_demo/bottleneck_test_data.pkl \
        -cm bottleneck_demo/bottleneck/trained_models/Bottleneck_Timesweeper_Class_${data_type} \
        -rm bottleneck_demo/bottleneck/trained_models/REG_Bottleneck_sdn_Timesweeper_Reg_${data_type} \
        -s bottleneck_demo/bottleneck/trained_models/Bottleneck_selcoeff_scaler.pkl \
        -o results/bottleneck_on_bottleneck_${data_type}.csv

    # Bottleneck on OoA
    python predict_data.py -i OoA_demo/OoA_test_data.pkl \
        -cm bottleneck_demo/bottleneck/trained_models/Bottleneck_Timesweeper_Class_${data_type} \
        -rm bottleneck_demo/bottleneck/trained_models/REG_Bottleneck_sdn_Timesweeper_Reg_${data_type} \
        -s bottleneck_demo/bottleneck/trained_models/Bottleneck_selcoeff_scaler.pkl \
        -o results/bottleneck_on_ooa_${data_type}.csv

    # Bottleneck on Constant
    python predict_data.py -i constant_demo/testing_data.pkl \
        -cm bottleneck_demo/bottleneck/trained_models/Bottleneck_Timesweeper_Class_${data_type} \
        -rm bottleneck_demo/bottleneck/trained_models/REG_Bottleneck_sdn_Timesweeper_Reg_${data_type} \
        -s bottleneck_demo/bottleneck/trained_models/Bottleneck_selcoeff_scaler.pkl \
        -o results/bottleneck_on_constant_${data_type}.csv



    ### OoA Model

    #OoA on OoA
    python predict_data.py -i OoA_demo/OoA_test_data.pkl \
        -cm OoA_demo/OoA/trained_models/OoA_Timesweeper_Class_${data_type} \
        -rm OoA_demo/OoA/trained_models/REG_OoA_sdn_Timesweeper_Reg_${data_type} \
        -s OoA_demo/OoA/trained_models/OoA_selcoeff_scaler\.pkl \
        -o results/ooa_on_ooa_${data_type}.csv


    #OoA on Bottleneck
    python predict_data.py -i bottleneck_demo/bottleneck_test_data.pkl \
        -cm OoA_demo/OoA/trained_models/OoA_Timesweeper_Class_${data_type} \
        -rm OoA_demo/OoA/trained_models/REG_OoA_sdn_Timesweeper_Reg_${data_type} \
        -s OoA_demo/OoA/trained_models/OoA_selcoeff_scaler\.pkl \
        -o results/ooa_on_bottleneck_${data_type}.csv


    #OoA on Constant
    python predict_data.py -i constant_demo/testing_data.pkl \
        -cm OoA_demo/OoA/trained_models/OoA_Timesweeper_Class_${data_type} \
        -rm OoA_demo/OoA/trained_models/REG_OoA_sdn_Timesweeper_Reg_${data_type} \
        -s OoA_demo/OoA/trained_models/OoA_selcoeff_scaler\.pkl \
        -o results/ooa_on_constant_${data_type}.csv


    ### Constant Model

    #Constant on Constant
    python predict_data.py -i constant_demo/testing_data.pkl \
        -cm constant_demo/constant_train/trained_models/Constant_Pop_Timesweeper_Class_${data_type} \
        -rm constant_demo/constant_train/trained_models/REG_Constant_Pop_sdn_Timesweeper_Reg_${data_type} \
        -s constant_demo/constant_train/trained_models/Constant_Pop_selcoeff_scaler.pkl \
        -o results/constant_on_constant_${data_type}.csv

    #Constant on Bottleneck
    python predict_data.py -i bottleneck_demo/bottleneck_test_data.pkl \
        -cm constant_demo/constant_train/trained_models/Constant_Pop_Timesweeper_Class_${data_type} \
        -rm constant_demo/constant_train/trained_models/REG_Constant_Pop_sdn_Timesweeper_Reg_${data_type} \
        -s constant_demo/constant_train/trained_models/Constant_Pop_selcoeff_scaler.pkl \
        -o results/constant_on_bottleneck_${data_type}.csv

    #Constant on OoA
    python predict_data.py -i OoA_demo/OoA_test_data.pkl \
        -cm constant_demo/constant_train/trained_models/Constant_Pop_Timesweeper_Class_${data_type} \
        -rm constant_demo/constant_train/trained_models/REG_Constant_Pop_sdn_Timesweeper_Reg_${data_type} \
        -s constant_demo/constant_train/trained_models/Constant_Pop_selcoeff_scaler.pkl \
        -o results/constant_on_ooa_${data_type}.csv

done