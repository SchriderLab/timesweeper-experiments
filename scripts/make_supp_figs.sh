echo ${1}
mkdir -p ${1}/fig_imgs
#cp ${1}/*/*/images/* ${1}/fig_imgs
for i in ${1}/*; do python scripts/plot_exp_metrics.py -id ${i} -o ${1}/fig_imgs/; done
python scripts/stitch_figures.py -i ${1}/fig_imgs/ -o simple_sims/figs/$(basename ${1})/