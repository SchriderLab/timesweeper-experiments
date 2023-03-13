for i in sample_size_10_benchmark_novel/vcfs/*/*/merged.vcf
    do 
    echo $i
    echo $(dirname $i)
    timesweeper detect -i $i \
    --benchmark \
    --aft-model sample_size_10_benchmark/trained_models/Sample_Size_10_benchmark_Timesweeper_aft \
    -o $(dirname $i) \
    --hft-model sample_size_10_benchmark/trained_models/Sample_Size_10_benchmark_Timesweeper_hft \
    -y config.-y
    done