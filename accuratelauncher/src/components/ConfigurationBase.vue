<template lang="pug">
v-card.mx-0
  v-card-title Configuration
  v-card-text
    GeneralDetails.mb-3
    VideoDetails.my-3
    AudioDetails.my-3
    CaptionDetails.my-3
    TbmdDetails.my-3
    SpritemapDetails.my-3
    MetadataDetails.my-3
</template>

<script>
import VideoDetails from "@/components/DPD/VideoSection/VideoDetails";
import AudioDetails from "@/components/DPD/AudioSection/AudioDetails";
import CaptionDetails from "@/components/DPD/CaptionSection/CaptionDetails";
import TbmdDetails from "@/components/DPD/TbmdSection/TbmdDetails";
import SpritemapDetails from "@/components/DPD/SpritemapSection/SpritemapDetails";
import GeneralDetails from "@/components/DPD/GeneralConfigSection/GeneralDetails";
import MetadataDetails from "@/components/DPD/MetadataSection/metadataDetails";

export default {
  name: "ConfigurationBase",
  components: {
    GeneralDetails,
    SpritemapDetails,
    CaptionDetails,
    AudioDetails,
    VideoDetails,
    TbmdDetails,
    MetadataDetails,
  }
}
</script>

<style scoped>

</style>