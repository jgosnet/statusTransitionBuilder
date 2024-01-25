import json
from __pl_tbmd_azure import AzureTBMD
from rally import files, supplyChain
import __tbmd_helper
from __pl_tbmd_factory import MarkerColor
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
        "AzureBrands": {
            "label": 'VidIndexVideo_Raw',
            "filter": AzureTBMD.BRANDS,
            "class": AzureTBMD,
            "marker_color": MarkerColor.GREEN,
            "tbmd_name": "Azure:Brands"
        },
        "AzureLabels": {
            "label": 'VidIndexVideo_Raw',
            "filter": AzureTBMD.LABELS,
            "class": AzureTBMD,
            "marker_color": MarkerColor.RED,
            "tbmd_name": "Azure:Labels"
        },
        "AzurePatterns": {
            "label": 'VidIndexVideo_Raw',
            "filter": AzureTBMD.FRAMEPATTERNS,
            "class": AzureTBMD,
            "marker_color": MarkerColor.BLUE,
            "tbmd_name": "Azure:Patterns"
        },
        "AzureKeywords": {
            "label": 'VidIndexVideo_Raw',
            "filter": AzureTBMD.KEYWORDS,
            "class": AzureTBMD,
            "marker_color": MarkerColor.PURPLE,
            "tbmd_name": "Azure:Keywords"
        }
    }

    __tbmd_helper.process_provider_dict(movie_label, provider_map, accurate_tbmds, access_tbmds)
    __tbmd_helper.add_files_to_inventory(tbmd_rsl_output, accurate_tbmds, access_tbmds)

    return supplyChain.SupplyChainStep("resume", dynamic_preset_data=data)