from rally import supplyChain

def eval_main(context):

    split = supplyChain.SupplyChainSplit("finish")

    split.add_split("celeb")
    split.add_split("moderation")
    split.add_split("transcribe")

    return split
