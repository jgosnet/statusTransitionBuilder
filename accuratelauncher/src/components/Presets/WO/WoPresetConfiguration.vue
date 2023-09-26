<template lang="pug">
v-card.mx-0
  v-card-title Configuration
  v-card-text
    OutputSpecs.mb-3
    AssetStatus.mb-3
    MetadataFields.mb-3
    MetadataView.mb-3

</template>

<script>
import AssetStatus from "@/components/Presets/WO/AssetStatus";
import MetadataFields from "@/components/Presets/WO/MetadataFields";
import MetadataView from "@/components/Presets/WO/MetadataView";
import OutputSpecs from "@/components/Presets/WO/OutputSpecs";

export default {
  name: "WoPresetConfiguration",
  components: {
    OutputSpecs,
    MetadataView,
    AssetStatus, MetadataFields
  }
}
</script>

<style scoped>

</style>