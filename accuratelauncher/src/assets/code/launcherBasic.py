import logging
import __pl_logging
from __pl_accurate import AccurateBasicWO
from __pl_accurate import AccurateEditWO
from __pl_accurate import AccurateValidateWO, AccurateConfiguration
import json
from rally import supplyChain

logger = logging.getLogger("prepare_accurate_wo")


def eval_main(context):
    dpd = context.get('dynamicPresetData') or {}
    logger.info(f"dynamicPresetData: {dpd}\n----\n")

    #REPLACE_DPD
    accurate_wo = AccurateBasicWO(dpd, ignore_missing_files=False)

    accurate_config = AccurateConfiguration()
    accurate_config.add_input_specs_dict(accurate_wo.get_input_specs())
    accurate_config.add_video_specs_dict("video", accurate_wo.get_video_data())

    print(f"MISSING LABELS: {accurate_wo.missing_file_items}")

    logger.info(json.dumps(accurate_config.get_specs(), indent=4))
    return supplyChain.SupplyChainStep("resume", dynamic_preset_data=accurate_config.get_specs())
