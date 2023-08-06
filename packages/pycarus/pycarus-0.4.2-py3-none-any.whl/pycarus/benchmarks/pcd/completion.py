from collections import defaultdict
from pathlib import Path
from statistics import mean

from pycarus.geometry.pcd import read_pcd
from pycarus.metrics.chamfer_distance import chamfer
from pycarus.metrics.emd_distance import emd
from pycarus.metrics.f_score import fscore


def pcd_completion_evaluation(gt_dir: Path, pred_dir: Path, results_dir: Path) -> None:
    """Evaluate point cloud completion results.

    The function requires the ground-truth clouds and the predicted ones to be
    organized in two separate directories with the same structure. Each directory
    must contain one sub-directory for each category and each subdirectory must
    contain one .ply file for each cloud. The function expects the name of the files
    in the "gt_dir" and "pred_dir" directories to be matching in order to perform
    the comparison.

    Four metrics are computed: the two Chamfer Distances proposed in the paper
    "Variational Relational Point Completion Network.", Earth Mover's Distance and F1 score.
    Results are saved into two files ("global_results.csv" and "single_results.csv")
    inside the given "result_dir" directory.

    Args:
        gt_dir: Directory with ground-truth clouds.
        pred_dir: Directory with predicted clouds.
        results_dir: Directory where the .csv files with the results will be saved.

    Raises:
        ValueError: If one prediction is missing.
    """
    results_dir.mkdir(parents=True, exist_ok=True)

    single_results_file = results_dir / "single_results.csv"
    if single_results_file.exists():
        single_results_file.unlink()

    with open(single_results_file, "wt") as f:
        f.write("CATEGORY/NAME,CD_P,CD_T,EMD,F1-SCORE\n")

    cd_ps = defaultdict(list)
    cd_ts = defaultdict(list)
    emds = defaultdict(list)
    f1_scores = defaultdict(list)

    categories_dirs = [subdir for subdir in gt_dir.iterdir() if subdir.is_dir()]
    for category_dir in categories_dirs:
        category = category_dir.name

        for gt_file in category_dir.glob("*.ply"):
            shape_name = gt_file.stem

            pred_file = pred_dir / category / gt_file.name
            if not pred_file.exists():
                raise ValueError(f"Cannot find prediction for shape {category}/{shape_name}.")

            gt = read_pcd(gt_file)
            pred = read_pcd(pred_file)

            cd_pred_gt, cd_gt_pred = chamfer(pred, gt, squared=False)
            cd_p = float(((cd_gt_pred + cd_pred_gt) / 2).item())
            cd_ps["all"].append(cd_p)
            cd_ps[category].append(cd_p)

            cd_pred_gt_sq, cd_gt_pred_sq = chamfer(pred, gt, squared=True)
            cd_t = float((cd_gt_pred_sq + cd_pred_gt_sq).item())
            cd_ts["all"].append(cd_t)
            cd_ts[category].append(cd_t)

            emd_, _ = emd(pred, gt, eps=0.004, iterations=3000, squared=False)
            emds["all"].append(float(emd_.item()))
            emds[category].append(float(emd_.item()))

            f1_score, _, _ = fscore(pred, gt, 0.01)
            f1_scores["all"].append(float(f1_score))
            f1_scores[category].append(float(f1_score))

            with open(single_results_file, "at") as f:
                line = f"{category}/{shape_name},{cd_p:.4f},{cd_t:.4f},{emd_:.4f},{f1_score:.4f}\n"
                f.write(line)

    global_results_file = results_dir / "global_results.csv"
    if global_results_file.exists():
        global_results_file.unlink()

    with open(global_results_file, "wt") as f:
        f.write("CATEGORY,CD_P,CD_T,EMD,F1-SCORE\n")

    for category in cd_ps:
        if category != "all":
            m_cd_p = mean(cd_ps[category])
            m_cd_t = mean(cd_ts[category])
            m_emd_ = mean(emds[category])
            m_f1_score = mean(f1_scores[category])

            with open(global_results_file, "at") as f:
                f.write(f"{category},{m_cd_p:.4f},{m_cd_t:.4f},{m_emd_:.4f},{m_f1_score:.4f}\n")

    with open(global_results_file, "at") as f:
        f.write("\n\n")
        f.write(f"MEAN CD_P,{mean(cd_ps['all']):.4f}")
        f.write(f"MEAN CD_T,{mean(cd_ts['all']):.4f}")
        f.write(f"MEAN EMD,{mean(emds['all']):.4f}")
        f.write(f"MEAN F1 SCORE,{mean(f1_scores['all']):.4f}")
