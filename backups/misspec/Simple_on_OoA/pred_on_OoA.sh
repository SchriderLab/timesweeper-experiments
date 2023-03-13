conda activate blinx
for rep in $(seq 1 100)
    do
    for swp in sdn ssv neut
        do
            i=/pine/scr/l/s/lswhiteh/timesweeper-experiments/empirical_model/OoA_samples_constant_sampling_uni_selcoeff/vcfs/$swp/$rep/merged.vcf 
            echo $i
            echo $(dirname $i)
            timesweeper detect -i $i \
                --benchmark \
                --aft-model /pine/scr/l/s/lswhiteh/timesweeper-experiments/misspec/sample_size_10_benchmark/sample_size_10_benchmark_uni_sel/trained_models/Sample_Size_10_uni_sel_benchmark_Timesweeper_aft \
                --hft-model /pine/scr/l/s/lswhiteh/timesweeper-experiments/misspec/sample_size_10_benchmark/sample_size_10_benchmark_uni_sel/trained_models/Sample_Size_10_uni_sel_benchmark_Timesweeper_hft \
                -o ./results_uni_sel/$swp/$rep \
                -y /pine/scr/l/s/lswhiteh/timesweeper-experiments/empirical_model/OoA_constant_sampling_config.-y
        done
    done
    