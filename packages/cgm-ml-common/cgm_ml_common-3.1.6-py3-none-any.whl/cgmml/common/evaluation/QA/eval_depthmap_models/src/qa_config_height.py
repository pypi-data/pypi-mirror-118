import os

from bunch import Bunch

CONFIG_NAME = os.path.splitext(os.path.basename(__file__))[0]

# Details of model used for evaluation
MODEL_CONFIG = Bunch(dict(
    EXPERIMENT_NAME='q3-depthmap-plaincnn-height-95k',
    RUN_ID='q3-depthmap-plaincnn-height-95k_1629821224_3ce63344',  # Run 9
    INPUT_LOCATION='outputs',
    NAME='best_model.ckpt',
))


EVAL_CONFIG = Bunch(dict(
    # Name of evaluation
    NAME='q3-depthmap-plaincnn-height-95k_run_02',

    # Experiment in Azure ML which will be used for evaluation

    # Used for Debug the QA pipeline
    DEBUG_RUN=False,

    # Will run eval on specified # of scan instead of full dataset
    DEBUG_NUMBER_OF_SCAN=25,

    SPLIT_SEED=0,
))

# Details of Evaluation Dataset
DATA_CONFIG = Bunch(dict(
    NAME='anon-realtime-testdata',  # Name of evaluation dataset

    IMAGE_TARGET_HEIGHT=240,
    IMAGE_TARGET_WIDTH=180,

    BATCH_SIZE=512,  # Batch size for evaluation
    NORMALIZATION_VALUE=7.5,

    # 0 is height, 1 is weight, 2 is muac, 3 is age,
    # 4 is sex('male' or 'female'), 5 is quality ('good' or 'bad'), 6 is test
    TARGET_INDEXES=[0, 3, 4, 5],

    CODES=['100', '101', '102', '200', '201', '202']
))

# Result configuration for result generation after evaluation is done
RESULT_CONFIG = Bunch(dict(
    # Error margin on various ranges
    ACCURACIES=[.2, .4, .6, 1., 1.2, 2., 2.5, 3., 4., 5., 6.],  # 0.2cm, 0.4cm, 0.6cm, 1cm, ...
    ACCURACY_MAIN_THRESH=1.0,  # 1cm
    AGE_BUCKETS=[0, 1, 2, 3, 4, 5],

    COLUMNS=['qrcode', 'artifact', 'scantype', 'GT', 'predicted'],

    # uncertainty
    USE_UNCERTAINTY=False,  # Flag to enable model uncertainty calculation

    # path of csv file in the experiment which final result is stored
    SAVE_PATH=f'./outputs/{CONFIG_NAME}',
))
