<template lang="pug">
v-card.mx-0
  v-card-title Configuration
  v-card-text
    VideoDetails.my-2
    AudioDetails.my-2
</template>

<script>
import VideoDetails from "@/components/VideoSection/VideoDetails";
import AudioDetails from "@/components/AudioSection/AudioDetails";
export default {
  name: "ConfigurationBase",
  components: {AudioDetails, VideoDetails}
}
</script>

<style scoped>

</style>