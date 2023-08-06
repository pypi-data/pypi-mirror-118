import numpy as np
from libs import costLib as ctl, mtfLib as mtl, imageLib as iml
from scipy.optimize import minimize
import configparser
import ast


def est_aberr(test_ims, config_ini="default.ini"):

    foc_params = configparser.ConfigParser()
    foc_params.read("../config/" + config_ini )

    pix_size_um = float(foc_params.get("sem", "pix_size_um"))
    num_aperture = float(foc_params.get("sem", "num_aperture"))
    stig_rot_deg = float(foc_params.get("sem", "stig_rot_deg"))

    test_aberrs = ast.literal_eval(foc_params.get("focus", "test_aberrs"))
    test_ims_aligned = int(foc_params.get("focus", "test_ims_aligned"))
    use_bessel = int(foc_params.get("focus", "use_bessel"))

    crop_ref = ast.literal_eval(foc_params.get("focus", "crop_ref"))
    crop_size = ast.literal_eval(foc_params.get("focus", "crop_size"))

    test_ims_cropped = [
        np.array(m.crop((crop_ref[0], crop_ref[1], crop_ref[0] + crop_size[0], crop_ref[1] + crop_size[1]))) for m
        in test_ims]

    if not test_ims_aligned:
        shift_in_meas = [iml.get_shift_vec(test_ims_cropped[0], test_ims_cropped[1]), [0, 0]]
    else:
        shift_in_meas = [[0, 0], [0, 0]]

    all_crop_refS = [[crop_ref[0] + shift_in_meas[k][0],
                      crop_ref[1] + shift_in_meas[k][1],
                      crop_ref[0] + crop_size[0] + shift_in_meas[k][0],
                      crop_ref[1] + crop_size[1] + shift_in_meas[k][1]] for k in [0, 1]]
    cropping_valid = True
    for cr in all_crop_refS:
        if not cr[0] > 0 or not cr[1] > 0 or not cr[2] < test_ims[0].size[0] \
                or not cr[3] < test_ims[0].size[1] or not cropping_valid:
            cropping_valid = False

    if cropping_valid:
        test_ims_cr_al = [np.array(m.crop((crop_ref[0] + shift_in_meas[k][0], crop_ref[1] + shift_in_meas[k][1],
                                           crop_ref[0] + crop_size[0] + shift_in_meas[k][0],
                                           crop_ref[1] + crop_size[1]
                                           + shift_in_meas[k][1]))) for k, m in enumerate(test_ims)]

        test_ims_cr_al_pr = [iml.removeMeanAndMeanSlope(im) for im in test_ims_cr_al]
        test_ims_cr_al_pr_fft = [np.fft.fftshift(np.fft.fft2(im)) for im in test_ims_cr_al_pr]
        test_ims_cr_al_pr_fft_lp = [iml.low_pass_filter(m) for m in test_ims_cr_al_pr_fft]

        ps_width, ps_height = test_ims_cr_al_pr_fft_lp[0].shape
        kspace_xy = mtl.get_kspace_xy(ps_width, pix_size_um, stig_rot_deg)

        res = minimize(ctl.cost_mapfost, [0, 0, 0],
                       args=(test_ims_cr_al_pr_fft_lp, test_aberrs, num_aperture, use_bessel, kspace_xy),
                       method="L-BFGS-B")
        res.x = np.round(res.x,2)

        return True, res

    else:
        return False, None
