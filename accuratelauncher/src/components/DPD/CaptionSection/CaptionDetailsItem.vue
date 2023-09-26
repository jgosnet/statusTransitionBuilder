<template lang="pug">
fieldset.dashed-border.pa-1
  legend.left-align.pl-2
    | {{ captionItem.name }}
    v-icon.ml-3(@click="deleteCaptionItem"
      size="x-small" ) fa-solid fa-trash-can
  div()
    v-row.px-3.py-1
      v-col(cols="9").py-1
        v-text-field(v-model="captionItem.name" hide-details
          label="Display name" density="compact" )
      v-col(cols="1")
      v-col(cols="2").py-1.my-0
        v-checkbox(label="Enabled ?" hide-details
          v-model="captionItem.enabled"
          :color="captionItem.enabled ? 'green' : 'red'"
          density="compact" )

    v-row.px-3.py-1.my-0
      v-col(:cols="labelSize").py-1.my-0
        v-text-field(v-model="captionItem.label" hide-details
          label="Caption label"
          density="compact" )
      v-col(:cols="checkboxcols").py-1.my-0
        v-checkbox(:label="checkboxName" hide-details
          v-model="captionItem.includeAssetName"
          density="compact" )
      v-col(v-show="captionItem.includeAssetName" cols="5").py-1.my-0
        v-text-field(v-model="captionItem.assetName" hide-details
          label="Asset Name"
          density="compact" )

    v-row.px-3.py-1.my-0
      v-col(:cols="captionItem.includeLanguage ? 1 : 12").py-1
        v-checkbox(v-model="captionItem.includeLanguage" hide-details
          :label="captionItem.includeLanguage ? '': 'Specify Language ?'" density="compact" )
      v-col(v-show="captionItem.includeLanguage" cols="11").py-1
        v-text-field(v-model="captionItem.language" hide-details
          label="Language" density="compact" )

    v-row.px-3.py-1.my-0
      v-col(:cols="captionItem.includeStartTc ? 1 : 6").py-1
        v-checkbox(v-model="captionItem.includeStartTc" hide-details
          :label="captionItem.includeStartTc ? '': 'Specify Start Timecode ?'" density="compact" )
      v-col(v-show="captionItem.includeStartTc" cols="5").py-1
        v-text-field(v-model="captionItem.startTc"
          label="Start Timecode" density="compact"
          :rules="[rules.required, rules.tcOrIntFormat]"
          hint="Frames count or TC (hh:mm:ss:;ff)")

      v-col(:cols="captionItem.includeFormat ? 1 : 6").py-1
        v-checkbox(v-model="captionItem.includeFormat" hide-details
          :label="captionItem.includeFormat ? '': 'Specify Format ?'" density="compact" )
      v-col(v-show="captionItem.includeFormat" cols="5").py-1
        v-combobox(v-model="captionItem.format" hide-details
          :items="supportedFormat"
        chips
          label="Format" density="compact"
          hint="Supported formats: ['ttml', 'vtt', 'webvtt', 'xml', 'scc']")

    v-row.px-3.py-1.my-0


</template>

<script>
export default {
  name: "CaptionDetailsItem",
  props:["captionItem"],
  data(){
    return {
      supportedFormat: ['ttml', 'vtt', 'webvtt', 'xml', 'scc'],
      tcRegexp: "^([0-1][0-9]|[0-2][0-3]):([0-5][0-9]):([0-5][0-9])[:;]([0-6][0-9])$",
      intRegexp: "^\\d+$",
      rules: {
        required: value => !!value || 'Frames count or TC (hh:mm:ss:;ff) is required',
        tcOrIntFormat: value => value.match(this.intRegexp) || value.match(this.tcRegexp) || 'Frames count or TC (hh:mm:ss:;ff) is required',
      }
    }
  },
    computed: {
    expansionIcon(){
      if (this.isExpanded === false){
        return "fa-solid fa-caret-down"
      } else{
        return "fa-solid fa-caret-right"
      }
    },
    labelSize(){
      if (this.captionItem.includeAssetName === false){
        return 10
      } else{
        return 6
      }
    },
    checkboxName(){
      if (this.captionItem.includeAssetName === false){
        return "Asset?"
      } else {
        return ""
      }
    },
    checkboxcols() {
      if (this.captionItem.includeAssetName === false) {
        return 2
      } else {
        return 1
      }
    },
  },
  methods: {
    deleteCaptionItem(){
        console.log(`deleting caption item:`)
        console.log(this.captionItem)
      this.$store.dispatch("captionDetails/deleteItem", this.captionItem)
      }
  }
}
</script>

<style scoped>
.dashed-border{
 border-style: dashed;
  background-color: whitesmoke;
}
</style>