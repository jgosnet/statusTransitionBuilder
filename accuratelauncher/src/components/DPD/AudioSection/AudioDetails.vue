<template lang="pug">
fieldset.pa-1
  legend.left-align.pl-2.font-weight-bold(@click="isExpanded = !isExpanded")
    span Audio details
    //v-tooltip(text="123" )
    //  template(v-slot:activator="{ props }")
    //    v-icon(v-bind="props").pl-2 fa-solid fa-circle-info
  div(id="expand")
    v-icon(:icon="expansionIcon" size="x-large"
      @click="isExpanded = !isExpanded")
  div(v-show="!isExpanded").py-1
  div(v-show="isExpanded" )
    span(v-show="Object.keys(audioItems).length === 0" ) No audio tracks specified
    v-row
      v-col(cols="12")
        AudioDetailsItem(v-for='item in audioItems'
            :key='audioItems.name'
            :audio-item="item" )
    v-row
      v-col(cols="12")
        v-btn(prepend-icon="fa-solid fa-plus"
        @click="addAudioItem" elevation="2" variant="outlined" ) Add audio track
</template>

<script>
import AudioDetailsItem from "@/components/DPD/AudioSection/AudioDetailsItem";
export default {
  name: "AudioDetails",
  components: {AudioDetailsItem},
  computed: {
    expansionIcon(){
      if (this.isExpanded === false){
        return "fa-solid fa-caret-down"
      } else{
        return "fa-solid fa-caret-right"
      }
    },
    audioItems: {
      get() {
        return this.$store.getters["audioDetails/audioItems"]
      },
      set(value) {
        this.$store.dispatch('audioDetails/updateAudioItems', value)
      }
    },
  },
  methods: {
    addAudioItem(){
      this.$store.dispatch("audioDetails/addNewAudioItem")
    },
  },
  data: function(){
    return {
      isExpanded: true,
    }
  }
}
</script>

<style scoped>

</style>