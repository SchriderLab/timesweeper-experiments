from glob import glob
from argparse import ArgumentParser
import re
import subprocess


"""Requires Imagemagick < v7"""


def extract_nums(filename):
    return int(re.findall(r"\d+", filename)[-1])


def get_file_from_partial(partial_name, filelist):
    return [i for i in filelist if partial_name in i][0]


agp = ArgumentParser()
agp.add_argument(
    "-i",
    "--in-dir",
    dest="in_dir",
    type=str,
    help="Top-level directory to search for images in.",
)
agp.add_argument(
    "-m",
    "--mode",
    dest="mode",
    default="model",
    choices=["model", "input"],
    help="Whether to stitch together a figure for input data or model validation images.",
)
ua = agp.parse_args()

data_types = ["aft", "hft"]
reg_class_types = ["sdn", "ssv"]
confmat_normed = ["normed", "unnormed"]
class_plot_types = ["pr", "roc", "confmat_normed", "confmat_unnormed", "training"]
reg_plot_types = ["selcoeffs", "corrected_selcoeffs", "mse_training"]

if ua.mode == "model":
    pdfs = glob(f"{ua.in_dir}/*.pdf", recursive=True)
    filter_term = "_Timesweeper_Class_aft_confmat_normed.pdf"
    ids = list(
        set([i.split("/")[-1].split(filter_term)[0] for i in pdfs if filter_term in i])
    )
    ids.sort(key=extract_nums)

    # Classification
    fig_rows = []
    for id in ids:
        f_imgs = []
        for d in data_types:
            imgs = []
            for c in class_plot_types:
                imgfile = get_file_from_partial(f"{id}_Timesweeper_Class_{d}_{c}", pdfs)
                imgs.append(imgfile)
            f_imgs.append(f"{id}_{d}_classfigs.tiff")
            subprocess.run(
                f"convert -density 300 +append {' '.join(imgs)} {id}_{d}_classfigs.tiff",
                shell=True,
            )
        fig_rows.append(f"{id}_all_classfigs.tiff")
        subprocess.run(
            f"convert -density 300 +append {' '.join(f_imgs)} {id}_all_classfigs.tiff",
            shell=True,
        )

    subprocess.run(
        f"convert -density 300 -append {' '.join(fig_rows)} final_classfigs.tiff",
        shell=True,
    )

    # Regression
    fig_rows = []
    for id in ids:
        d_imgs = []
        for d in data_types:
            c_imgs = []
            for c in reg_plot_types:
                s_imgs = []
                for s in reg_class_types:
                    imgfile = get_file_from_partial(
                        f"{id}_{s}_Timesweeper_Reg_{d}_{c}", pdfs
                    )
                    s_imgs.append(imgfile)

                _name = f"{id}_bothclass_{d}_{c}.tiff"
                c_imgs.append(_name)
                subprocess.run(
                    f"convert -density 300 +append {' '.join(s_imgs)} {_name}",
                    shell=True,
                )

            _name = f"{id}_bothclass_{d}_all.tiff"
            d_imgs.append(_name)
            subprocess.run(
                f"convert -density 300 +append {' '.join(c_imgs)} {_name}", shell=True
            )

        _name = f"{id}_all_regfits.tiff"
        fig_rows.append(_name)
        subprocess.run(
            f"convert -density 300 +append {' '.join(d_imgs)} _name", shell=True
        )

    subprocess.run(
        f"convert -density 300 -append {' '.join(fig_rows)} final_regfigs.tiff",
        shell=True,
    )
