conda activate blinx
for rep in $(seq 1 100)
    do
    for swp in hard soft neut
        do
            i=/pine/scr/l/s/lswhiteh/timesweeper-experiments/misspec/sample_size_10_benchmark/sample_size_10_benchmark_uni_sel/vcfs/$swp/$rep/merged.vcf 
            echo $i
            echo $(dirname $i)
            timesweeper detect -i $i \
                --benchmark \
                --aft-model /pine/scr/l/s/lswhiteh/timesweeper-experiments/empirical_model/OoA_samples_constant_sampling_uni_selcoeff/trained_models/OoA_Constant_uni_sel_Timesweeper_aft \
                --hft-model /pine/scr/l/s/lswhiteh/timesweeper-experiments/empirical_model/OoA_samples_constant_sampling_uni_selcoeff/trained_models/OoA_Constant_uni_sel_Timesweeper_hft \
                -o ./results_uni_sel/$swp/$rep \
                yaml /pine/scr/l/s/lswhiteh/timesweeper-experiments/misspec/sample_size_10_benchmark/config.yaml
        done
    done
    