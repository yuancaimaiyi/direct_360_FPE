from config import read_config, overwrite_scene_data
from config.config import overwite_version
from data_manager import DataManager
from src import DirectFloorPlanEstimation
from utils.visualization.vispy_utils import plot_color_plc
from utils.enum import CAM_REF
import numpy as np
from utils.data_utils import flatten_lists_of_lists
import matplotlib.pyplot as plt
from utils.visualization.room_utils import plot_curr_room_by_patches, plot_all_rooms_by_patches
from utils.visualization.room_utils import plot_floor_plan
from utils.room_id_eval_utils import eval_2D_room_id_iou, summarize_results_room_id_iou
from utils.io import read_csv_file, save_csv_file
import os


def main(config_file, scene_list_file, version):
    # ! Reading list of scenes
    list_scenes = read_csv_file(scene_list_file)

    cfg = read_config(config_file=config_file)

    # for param in np.linspace(1, 10, 10):
    #     ver = version + "_sigma{0:2.2f}".format(param)
    #     cfg["room_id.temporal_weighting_sigma"] = float(param) 
    
    # for param in (0.1, 0.25, 0.5, 0.75, 0.95):
    #     ver = version + f"_thr{param}"
    #     cfg["room_id.ocg_threshold"] = param 
        
    # ! Running every scene
    for scene in list_scenes:
        overwrite_scene_data(cfg, scene)
        overwite_version(cfg, version)
        
        dt = DataManager(cfg)

        fpe = DirectFloorPlanEstimation(dt)
        list_ly = dt.get_list_ly(cam_ref=CAM_REF.WC_SO3)

        for ly in list_ly:
            fpe.estimate(ly)

        # fpe.eval_room_overlapping()
        
        fpe.global_ocg_patch.update_bins()
        fpe.global_ocg_patch.update_ocg_map()
        # plot_all_rooms_by_patches(fpe, only_save=True)

        # exit()
        eval_2D_room_id_iou(fpe)
        fpe.dt.save_config()
        
            # sumarize_restults_room_id_iou(fpe)


if __name__ == '__main__':
    # TODO read from  passed args
    config_file = "./config/config.yaml"
    scene_list_file = './data/all_scenes_list.csv'
    version = 'test_no_merge_sigma1.00'

    main(config_file, scene_list_file, version)
