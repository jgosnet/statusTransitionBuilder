from rally import supplyChain
import json
import __pl_technical
import logging
import __pl_logging
from __pl_status_transitions import StatusHelper
from ACCEDIT_status_transitions import STATUS_TRANSITIONS

STEP_NAME = "accurate_edit"
logger = logging.getLogger(STEP_NAME)
status_helper = StatusHelper(STATUS_TRANSITIONS, STEP_NAME)

techReport = __pl_technical.TechnicalReport()


def eval_main(context):
    data = context.get("dynamicPresetData") or {}
    logger.info(f"dynamicPresetData: {data}\n----\n")

    movieLabel = 'movie'

    audioLayout = techReport.get_audio_layout(label=movieLabel)
    trackCount = len(audioLayout)

    if trackCount == 1 and audioLayout[1] == 1:
        data["audioConfig"] = "1-Track-MONO"
    elif trackCount >= 2 and audioLayout[1] == 1 and audioLayout[2] == 1:
        data["audioConfig"] = "2-Track-MONO"
    elif trackCount >= 1 and audioLayout[1] == 2:
        data["audioConfig"] = "STEREO"
    else:
        data["audioConfig"] = "AUTO"

    logger.info(json.dumps(data, indent=4))

    status_helper.execute_transition("on_audio_config", parameters_dict={"audio_config": data["audioConfig"]})

    status_helper.execute_transition("on_proxy_start", parameters_dict={})

    # utils_asset_status.add_status_if_unique(message='Proxy: FFMPEG Job Started',
    #                                         group='Proxy Module',
    #                                         icon='fa-solid fa-p',
    #                                         color='blue',
    #                                         curate_message=True,
    #                                         curate_group=True)

    sequence = supplyChain.SupplyChainSequence()
    sequence.add_step(supplyChain.SupplyChainStep(name='resume', dynamic_preset_data=data))
    sequence.add_step(supplyChain.SupplyChainStep(name='resume', dynamic_preset_data=data))

    return sequence

