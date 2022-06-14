for i in vcfs/*/*/merged.vcf
    do 
    echo $i
    echo $(dirname $i)
    timesweeper detect -i $i \
    --benchmark \
    --aft-model /pine/scr/l/s/lswhiteh/timesweeper-experiments/simple_sims/sample_size/ss_10/sample_size_10/trained_models/Sample_Size_10_Timesweeper_aft \
    -o $(dirname $i) \
    --hft-model /pine/scr/l/s/lswhiteh/timesweeper-experiments/simple_sims/sample_size/ss_10/sample_size_10/trained_models/Sample_Size_10_Timesweeper_hft \
    yaml ../config.yaml
    done