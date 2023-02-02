#Feed this script a top-level experiment folder (e.g. /simple_sims/win_sizes/)
echo ${1}
rm -rf ${1}/fig_imgs
mkdir -p ${1}/fig_imgs
cp ${1}/*/*/images/* ${1}/fig_imgs 2>/dev/null
for i in ${1}/*
do 
    python scripts/plotting/plot_exp_metrics.py -id ${i} -o ${1}/fig_imgs/
done

python scripts/plotting/stitch_figures.py -i ${1}/fig_imgs/ -o simple_sims/figs/$(basename ${1})/