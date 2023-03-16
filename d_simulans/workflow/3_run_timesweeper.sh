cd ..
for i in FreqInputs/aftInputsVelocity/*
do
    sbatch --time=1:00:00 --mem=8G -c 4 --wrap="\
    timesweeper detect-npz \
        -i $i \
        -o d_simulans_output/ \
        -y d_simulans_config.yaml "
done