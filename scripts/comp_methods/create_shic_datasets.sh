train_vcf_dir=/work/users/l/s/lswhiteh/timesweeper-experiments/simple_sims/better_benchmark/train_benchmark/vcfs/
train_data_dir=/work/users/l/s/lswhiteh/timesweeper-experiments/simple_sims/better_benchmark/train_benchmark/shic_data

head -n 1 ${train_vcf_dir}/neut/0/0.final.neut.win_5.fvec -n 1 > ${train_data_dir}/neuts.fvec
head -n 1 ${train_vcf_dir}/neut/0/0.final.neut.win_5.fvec -n 1 > ${train_data_dir}/hard.fvec
head -n 1 ${train_vcf_dir}/neut/0/0.final.neut.win_5.fvec -n 1 > ${train_data_dir}/soft.fvec
head -n 1 ${train_vcf_dir}/neut/0/0.final.neut.win_5.fvec -n 1 > ${train_data_dir}/linkedSoft.fvec
head -n 1 ${train_vcf_dir}/neut/0/0.final.neut.win_5.fvec -n 1 > ${train_data_dir}/linkedHard.fvec


for i in $(seq 0 10000)
do
    tail -n 1 ${train_vcf_dir}/neut/${i}/${i}.final.neut.win_5.fvec >> ${train_data_dir}/neuts.fvec
    tail -n 1 ${train_vcf_dir}/sdn/${i}/${i}.final.sdn.win_5.fvec >> ${train_data_dir}/hard.fvec
    tail -n 1 ${train_vcf_dir}/ssv/${i}/${i}.final.ssv.win_5.fvec >> ${train_data_dir}/soft.fvec
done

for i in $(seq 0 10000 | shuf -n 1000)
do
    for win in 0 1 2 3 4 6 7 8 9 10
    do
        tail -n 1 ${train_vcf_dir}/sdn/${i}/${i}.final.sdn.win_${win}.fvec >> ${train_data_dir}/linkedHard.fvec
        tail -n 1 ${train_vcf_dir}/ssv/${i}/${i}.final.ssv.win_${win}.fvec >> ${train_data_dir}/linkedSoft.fvec
    done
done