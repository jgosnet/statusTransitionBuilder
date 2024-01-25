import __tbmd_helper
from rally import supplyChain
from __pl_tbmd_google import GoogleTBMD
from __pl_tbmd_factory import MarkerColor

def eval_main(context):
    movie_label = 'movie'
    data = context.get("dynamicPresetData") or {}
    tbmd_rsl_output = "demo2023_artifacts"
    accurate_tbmds, access_tbmds = [], []
    provider_map = {
        "GoogleVi": {
            "label": 'GoogleVI-Raw',
            "class": GoogleTBMD,
            "marker_color": MarkerColor.CYAN
        }
    }

    __tbmd_helper.process_provider_dict(movie_label, provider_map, accurate_tbmds, access_tbmds)
    __tbmd_helper.add_files_to_inventory(tbmd_rsl_output, accurate_tbmds, access_tbmds)


    return supplyChain.SupplyChainStep("resume", dynamic_preset_data=data)