<template lang="pug">
v-card.mx-0
  v-card-title Configuration
  v-card-text
    fieldset.pa-1.mb-5
      legend.left-align.pl-2.font-weight-bold(@click="isExpanded = !isExpanded")
        span General configuration
        //v-tooltip(text="123" )
        //  template(v-slot:activator="{ props }")
        //    v-icon(v-bind="props").pl-2 fa-solid fa-circle-info
      div(id="expand")
        v-icon(:icon="expansionIcon" size="x-large"
          @click="isExpanded = !isExpanded")
      div(v-show="!isExpanded").py-1
      div(v-show="isExpanded" )
        v-row
          v-col(cols="12")
            v-radio-group(inline label="Work-order type" v-model="woType")
              v-radio(label="Basic" value="basic")
              v-radio(label="Validate" value="validate")
              v-radio(label="Edit" value="edit")

        v-row
          v-col(cols="12")
            v-checkbox(label="Include Hardcoded dynamic preset data ?" hide-details
          v-model="includehardcodedDpd"
          density="compact" )


</template>

<script>


export default {
  name: "LauncherPresetConfiguration",
   data(){
    return {
      isExpanded: true,
    }
  },
  computed: {
    includehardcodedDpd: {
      get() {
        return this.$store.getters["launcherPreset/includehardcodedDpd"]
      },
      set(value) {
        this.$store.dispatch('launcherPreset/updateIncludehardcodedDpd', value)
      }
    },
    woType: {
      get() {
        return this.$store.getters["launcherPreset/woType"]
      },
      set(value) {
        this.$store.dispatch('launcherPreset/updateWoType', value)
      }
    },
    expansionIcon() {
      if (this.isExpanded === false) {
        return "fa-solid fa-caret-down"
      } else {
        return "fa-solid fa-caret-right"
      }
    },
  },
}
</script>

<style scoped>
fieldset{
  border-style: dashed;
}
legend{
  font-size: large;
}
</style>