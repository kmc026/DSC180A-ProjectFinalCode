import sys
import json

from src.main import find_yellow_lanes
from src.main import find_n_largest_contours


def main(targets):

    test_config = json.load(open("config/config.json"))

    if 'test' in targets:
        
        find_yellow_lanes(test_config['test_image_dir'], test_config['lane_image_result_dir'])
        find_n_largest_contours(test_config['lane_image_result_dir'], test_config['lane_centroids_image_result_dir'])

    if 'lane' in targets:
        find_yellow_lanes(test_config['test_image_dir'], test_config['lane_image_result_dir'])

    if 'centroids' in targets:
        find_n_largest_contours(test_config['lane_image_result_dir'], test_config['lane_centroids_image_result_dir'])

if __name__ == '__main__':

    targets = sys.argv[1:]
    main(targets)