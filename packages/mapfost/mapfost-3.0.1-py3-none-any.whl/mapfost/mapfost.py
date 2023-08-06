import numpy as np
import costLib as ctl
import mtfLib as mtl
import imageLib as iml
from scipy.optimize import minimize
import configparser
import ast
from PIL import Image
import os
import glob
import shutil


def est_aberr(test_ims, pix_size_um = None, crop_ref=None, config_ini="default.ini"):

    foc_params = configparser.ConfigParser()
    foc_params.read( config_ini )

    if pix_size_um is None:
        pix_size_um = float(foc_params.get("sem", "pix_size_um"))
    num_aperture = float(foc_params.get("sem", "num_aperture"))
    stig_rot_deg = float(foc_params.get("sem", "stig_rot_deg"))

    test_aberrs = ast.literal_eval(foc_params.get("focus", "test_aberrs"))
    test_ims_aligned = int(foc_params.get("focus", "test_ims_aligned"))
    use_bessel = int(foc_params.get("focus", "use_bessel"))

    if crop_ref is None:
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


def test_installation():
    im1 = Image.open("test_im1.tif")
    im2 = Image.open("test_im2.tif")

    estValid, res = est_aberr([im1, im2])
    if res.x[0] == 2.11 and res.x[1] == 0.05 and res.x[2] == 0.16:
        print("...Installation Test Successful...")
    return res


def update_config_ini(ini_name, section, option, value):
    stop_default_edit([ini_name])
    foc_params = configparser.ConfigParser()
    foc_params.read( ini_name)
    sections = foc_params.sections()
    if section not in sections:
        foc_params.add_section(section)
    foc_params.set(section, option, value)
    with open( ini_name, 'w') as configfile:
        foc_params.write(configfile)

    print("Changed " + option + " parameter in " + ini_name
          + " of section " + section + " to " + value )


def stop_default_edit(ini_names):
    for ini_name in ini_names:
        if ini_name == 'default.ini':
            print("Editing default.ini not allowed.")
            raise PermissionError


def create_new_config_ini(ini_name):
    stop_default_edit([ini_name])
    foc_params = configparser.ConfigParser()
    with open( ini_name, 'w') as configfile:
        foc_params.write(configfile)


def rename_config_ini(old_ini_name, new_ini_name):
    stop_default_edit([old_ini_name,new_ini_name])
    if os.path.isfile(old_ini_name):
        shutil.move( old_ini_name,new_ini_name)
    return True


def update_config_ini_from_exisiting_ini(to_ini, from_ini):

    stop_default_edit([to_ini])
    foc_params_from = configparser.ConfigParser()
    foc_params_from.read(from_ini)
    foc_params_to = configparser.ConfigParser()
    for section in foc_params_from.sections():
        if section not in foc_params_to.sections():
            foc_params_to.add_section(section)
        for option in foc_params_from[section]:
            foc_params_to.set(section,option,foc_params_from.get(section,option))

    with open( to_ini, 'w') as configfile:
        foc_params_to.write(configfile)

def list_all_config_ini():
    all_inis = [os.path.basename(cini) for cini in glob.glob( "*.ini")]
    return all_inis

def read_config_ini(ini_name):
    foc_params = configparser.ConfigParser()
    foc_params.read( ini_name)
    ini_dict = {}
    for section in foc_params.sections():
        ini_dict[section] = {}
        print("\n")
        print("[" + section + "]")
        for option in foc_params[section]:
            print(option, "=", foc_params.get(section,option))
            ini_dict[section][option] = foc_params.get(section,option)

    return ini_dict

def update_config_ini_from_dict(ini_name, update_from_dict):
    stop_default_edit([ini_name])
    foc_params = configparser.ConfigParser()
    foc_params.read( ini_name)
    for section in update_from_dict:
        if section not in foc_params.sections():
            foc_params.add_section(section)
        for option in update_from_dict[section]:
            foc_params[section][option] = update_from_dict[section][option]
    with open(ini_name, 'w') as configfile:
        foc_params.write(configfile)

test_installation()