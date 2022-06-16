for rep in $(seq 1 100)
    do
    for swp in hard soft neut
        do
            i=/pine/scr/l/s/lswhiteh/timesweeper-experiments/empirical_model/mongolian_samples/vcfs/$swp/$rep/merged.vcf 
            echo $i
            echo $(dirname $i)
            timesweeper detect -i $i \
                --benchmark \
                --aft-model /pine/scr/l/s/lswhiteh/timesweeper-experiments/simple_sims/sample_size/ss_10/sample_size_10/trained_models/Sample_Size_10_Timesweeper_aft \
                -o ./results/$swp/$rep \
                yaml /pine/scr/l/s/lswhiteh/timesweeper-experiments/empirical_model/OoA_config.yaml
        done
    done
    