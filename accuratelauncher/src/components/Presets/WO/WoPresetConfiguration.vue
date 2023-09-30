<template lang="pug">
v-card.mx-0
  v-card-title Configuration
  v-card-text
    OutputSpecs.mb-3
    AssetStatus.mb-3
    MetadataFields.mb-3
    FormsView.mb-3
    MetadataView.mb-3
    ManualMarkerView.mb-3

</template>

<script>
import AssetStatus from "@/components/Presets/WO/AssetStatus";
import MetadataFields from "@/components/Presets/WO/MetadataFields";
import MetadataView from "@/components/Presets/WO/MetadataViews/MetadataView";
import ManualMarkerView from "@/components/Presets/WO/Markers/ManualMarkerView";
import OutputSpecs from "@/components/Presets/WO/OutputSpecs";
import FormsView from "@/components/Presets/WO/Forms/FormsView";

export default {
  name: "WoPresetConfiguration",
  components: {
    OutputSpecs,
    MetadataView,
    AssetStatus,
    MetadataFields,
    ManualMarkerView,
    FormsView
  }
}
</script>

<style scoped>

</style>