import __tbmd_helper
from __pl_tbmd_rekognition import RekognitionTBMD
from __pl_tbmd_factory import MarkerColor
from rally import supplyChain
import logging
import __pl_logging
from __pl_status_transitions import StatusHelper
from AUTOAI_transitions import STATUS_TRANSITIONS
from AUTOAI_rekognition_config import MODULE_NAME

STEP_NAME = "ai"
logger = logging.getLogger(STEP_NAME)
status_helper = StatusHelper(STATUS_TRANSITIONS, STEP_NAME)

def eval_main(context):
    data = context.get('dynamicPresetData') or {}
    logger.info(f"dynamic_preset_Data: {data}\n----\n")

    movie_label = 'movie'
    tbmd_rsl_output = "demo2023_artifacts"
    accurate_tbmds, access_tbmds = [], []
    provider_map = {
        "RekCeleb": {
            "label": 'RekCelebDet-Raw',
            "class": RekognitionTBMD, 
            "marker_color": MarkerColor.GREEN,
            "tbmd_name": "Rekognition:Celebrity"
        },
        "RekMod": {
            "label": 'RekContMod-Raw',
            "class": RekognitionTBMD,
            "marker_color": MarkerColor.PURPLE,
            "tbmd_name": "Rekognition:Moderation"
        },
        "RekTranscribe": {
            "label": 'RekTranscribe-Raw',
            "class": RekognitionTBMD,
            "marker_color": MarkerColor.BLUE,
            "tbmd_name": "Rekognition:Transcribe"
        }
    }

    __tbmd_helper.process_provider_dict(movie_label, provider_map, accurate_tbmds, access_tbmds)
    __tbmd_helper.add_files_to_inventory(tbmd_rsl_output, accurate_tbmds, access_tbmds)

    return supplyChain.SupplyChainStep("resume", dynamic_preset_data=data)
