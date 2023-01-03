Figures were created by first copying all images from an experiment set to a temp folder, re-creating the metrics using scripts/plot_exp_metrics.py, and then stitching with scripts/stitch_figures.py.

e.g. 
```
$ mkdir simple_sims/sel_coeff/fig_imgs
cp simple_sims/sel_coeff/*/*/images/* simple_sims/sel_coeff/fig_imgs
for i in simple_sims/sel_coeff/s_*; do python scripts/plot_exp_metrics.py -id $i -o simple_sims/sel_coeff/fig_imgs/; done
