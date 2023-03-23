import os
import re
import subprocess
from argparse import ArgumentParser
from glob import glob

from tqdm import tqdm

"""Requires Imagemagick < v7 and pdf2pdf"""


def extract_nums(filename):
    try:
        if "neg" in filename:
            ele = float(re.findall(r"[-+]?\d*\.\d+|\d+", filename)[-1])
            return (0, ele, "")
        else:
            ele = float(re.findall(r"[-+]?\d*\.\d+|\d+", filename)[-1])
            return (1, ele, "")
    except:
        return (2, filename, "")


def get_file_from_partial(partial_name, filelist):
    print(f"[debug] Partial name: {partial_name}")

    return [i for i in filelist if i.split("/")[-1].startswith(partial_name)][0]


def make_class_fig(pdfs, ids, data_types, class_plot_types, tmpdir, outdir):
    # Classification
    fig_rows = []
    for id in tqdm(ids, desc="Making classification figs"):
        print(id)
        f_imgs = []
        for d in data_types:
            imgs = []
            for c in class_plot_types:
                imgfile = get_file_from_partial(f"{id}_Timesweeper_Class_{d}_{c}", pdfs)
                imgs.append(imgfile)

            _name = f"{tmpdir}/{id}_{d}_classfigs.png"
            f_imgs.append(_name)
            subprocess.run(
                f"convert -gravity center -quality 100 -density 500 +append {' '.join(imgs)} -resample 300 {_name}",
                shell=True,
            )

        _name = f"{tmpdir}/{id}_all_classfigs.png"
        fig_rows.append(_name)
        subprocess.run(
            f"convert -gravity center -quality 100 -density 500 +append {' '.join(f_imgs)} -resample 300 {_name}",
            shell=True,
        )

    subprocess.run(
        f"convert -gravity center -quality 100 -density 150  -size 500 -colorspace sRGB -append {' '.join(fig_rows)} {outdir}/final_classfigs.png",
        shell=True,
    )
    subprocess.run(
        f"convert {outdir}/final_classfigs.png {outdir}/final_classfigs.pdf",
        shell=True,
    )


def make_reg_fig(
    pdfs, ids, data_types, reg_plot_types, reg_class_types, tmpdir, outdir
):
    # Regression
    fig_rows = []
    for id in tqdm(ids, desc="Making regression figs"):
        print(id)
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

                _name = f"{tmpdir}/{id}_bothclass_{d}_{c}.png"
                c_imgs.append(_name)
                subprocess.run(
                    f"convert -gravity center -quality 100 -density 150  -colorspace sRGB +append {' '.join(s_imgs)} {_name}",
                    shell=True,
                )

            _name = f"{tmpdir}/{id}_bothclass_{d}_all.png"
            d_imgs.append(_name)
            subprocess.run(
                f"convert -gravity center -quality 100 -density 150  -colorspace sRGB +append {' '.join(c_imgs)} {_name}",
                shell=True,
            )

        _name = f"{tmpdir}/{id}_all_regfigs.png"
        fig_rows.append(_name)
        subprocess.run(
            f"convert -gravity center -quality 100 -density 150  -colorspace sRGB +append {' '.join(d_imgs)} {_name}",
            shell=True,
        )

    subprocess.run(
        f"convert -gravity center -quality 100 -density 150  -colorspace sRGB -append {' '.join(fig_rows)} {outdir}/final_regfigs.png",
        shell=True,
    )
    subprocess.run(
        f"convert {outdir}/final_regfigs.png {outdir}/final_regfigs.pdf",
        shell=True,
    )


def get_ua():
    agp = ArgumentParser()
    agp.add_argument(
        "-i",
        "--in-dirs",
        dest="in_dirs",
        type=str,
        nargs="+",
        help="Directories to search for images in.",
    )
    agp.add_argument(
        "-o",
        "--outdir",
        dest="outdir",
        default=f"{os.getcwd()}/finalfigs",
        type=str,
        help="Output path for pdf files.",
    )
    agp.add_argument(
        "-t",
        "--tmpdir",
        dest="tmpdir",
        default=f"{os.getcwd()}/tmp",
        type=str,
        help="Path to store temp files.",
    )
    agp.add_argument(
        "--keep-tmp",
        dest="keeptmp",
        help="Whether to keep tmpdir or not.",
        action="store_true",
    )
    agp.add_argument(
        "-m",
        "--mode",
        dest="mode",
        default="model",
        choices=["model", "input"],
        help="Whether to stitch together a figure for input data or model validation images.",
    )
    return agp.parse_args()


ua = get_ua()

os.makedirs(ua.tmpdir, exist_ok=True)
os.makedirs(ua.outdir, exist_ok=True)

data_types = ["aft", "hft"]
reg_class_types = ["sdn", "ssv"]
confmat_normed = ["normed", "unnormed"]
class_plot_types = ["pr", "roc", "confmat_normed", "confmat_unnormed", "training"]
reg_plot_types = ["selcoeffs", "reg_mse_training"]

if ua.mode == "model":
    pdfs = []
    for dir in ua.in_dirs:
        pdfs.extend(glob(f"{dir}/*.pdf", recursive=True))

    filter_term = "_Timesweeper_Class_aft_confmat_normed.pdf"
    ids = list(
        set([i.split("/")[-1].split(filter_term)[0] for i in pdfs if filter_term in i])
    )
    ids = [i for i in ids if "Timepoints" not in i]
    print(ids)
    ids.sort(key=extract_nums)
    # Want absolute distance if working with timing
    if "neg" in ids[0]:
        ids[:3] = reversed(ids[:3])

    print(ids)

    make_class_fig(pdfs, ids, data_types, class_plot_types, ua.tmpdir, ua.outdir)
    make_reg_fig(
        pdfs, ids, data_types, reg_plot_types, reg_class_types, ua.tmpdir, ua.outdir
    )

    if not ua.keeptmp:
        for f in glob(f"{ua.tmpdir}/*"):
            os.remove(f)
        os.rmdir(ua.tmpdir)
