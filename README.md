# TimeSweeper Experiments

Repo for experiments for the TimeSweeper manuscript.

**Note:** All code here was run using the `blinx.yml` conda environment found in the Timesweeper repo **!add link when public**

## Empirical Analysis

- Link to paper: https://www.nature.com/articles/s41586-021-03336-2
- Supplementary tables found in `/samp_data/raw/Online_table*` were downloaded from the online article in the Supplementary section.
- Accession information and direct links can be found here: https://www.ncbi.nlm.nih.gov/bioproject/PRJEB42781/

- Please note that preparing Timesweeper models and processing the study data could happen in any order, the only dependency is that you have the dates, sample sizes, and other config information for the Timesweeper simulations prior to simulating and training the model.
  
---

**Note:** To replicate the analysis performed in the manuscript section "Application of Timesweeper on Ancient DNA Samples" do the following:

### Prep Timesweeper Model

1. Generate Out-of-Africa (OoA) SLiM model using stdpopsim 

    ```
    stdpopsim -e slim \ 
    --slim-path <SLiM executable> \
    --slim-script \
    --slim-scaling-factor 5 \
    HomSap -d OutOfAfrica_3G09 0 0 0 > 
    OoA.slim
    ```
2. Run `scripts/workflow/1_timesweeper_sim.sh` to simulate data 
3. Run `scripts/workflow/2_timesweeper_workflow.sh` to do the rest of the TimeSweeper prep work:
   1. Convert individual-timepoint VCFs to merged VCFs using the `process_vcfs` module 
   2. Collect and organize merged VCFs, and optionally add missingness, before saving to `training_data.pkl` using the `make_training_data` module
   3. Train the neural networks using the `nets` module


After model training the `nets` module will automatically evaluate the model on held-out test data taken from the training data. Confusion matrices, ROC curves, and PR curves will be plotted and saved in the `/images` directory of the working directory specified by the config file, for the OoA simulations with Neolithic Mongolian sampling schema these can be found in `/mongolian_samples/images`

---

#### Download and Process Study Data

1. Download bam files found in the study with `$bash scripts/download_bams.sh`
   - These samples were filtered from the entire set using `scripts/filter_bin_samps.py` 
     - By samples found in the Mongolia region described in the publication
     - Average coverage (minimum of 1)
     - Contamination status (preserved if potentially contaminated in regions we're not interested in)
2. Run the snakemake pipeline for variant calling and merging 