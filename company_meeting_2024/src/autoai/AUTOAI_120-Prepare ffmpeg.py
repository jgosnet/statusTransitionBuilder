from rally import files, supplyChain, asset, jobs
import json
import copy
import __pl_technical

techReport = __pl_technical.TechnicalReport()


def eval_main(context):
    data = context.get('dynamicPresetData') or {}
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

    print(json.dumps(data, indent=4))

    # Get the AI provider to correctly build the next steps

    ai_provider = data.get('ai_provider')

    sequence = supplyChain.SupplyChainSequence()

    # FFMPEG proxy job
    sequence.add_step(supplyChain.SupplyChainStep('start_ffmpeg', dynamic_preset_data=data))

    # Step after proxy creation
    print("Next step: ffmpeg creates SdviProxy and SdviThumbnail files")
    print("Next step after that:")

    if ai_provider == "rekog":

        print("Prepare Rekognition split jobs")
        sequence.add_step(supplyChain.SupplyChainStep('rekog', dynamic_preset_data=data))

    elif ai_provider == "google_vi":

        print("Google VI: copy proxy to GCP storage and execute job")
        sequence.add_step(supplyChain.SupplyChainStep('google_vi', dynamic_preset_data=data))

    elif ai_provider == "azure_vi":

        print("Azure VI job")
        sequence.add_step(supplyChain.SupplyChainStep('azure_vi', dynamic_preset_data=data))

    return sequence
