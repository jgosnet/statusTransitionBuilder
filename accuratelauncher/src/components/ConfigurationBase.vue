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
</template>

<script>
import VideoDetails from "@/components/VideoSection/VideoDetails";
import AudioDetails from "@/components/AudioSection/AudioDetails";
import CaptionDetails from "@/components/CaptionSection/CaptionDetails";
import TbmdDetails from "@/components/TbmdSection/TbmdDetails";
import SpritemapDetails from "@/components/SpritemapSection/SpritemapDetails";
import GeneralDetails from "@/components/GeneralConfigSection/GeneralDetails";

export default {
  name: "ConfigurationBase",
  components: {
    GeneralDetails,
    SpritemapDetails,
    CaptionDetails,
    AudioDetails,
    VideoDetails,
    TbmdDetails
  }
}
</script>

<style scoped>

</style>