<template lang="pug">
fieldset.pa-1.mb-5
  legend.left-align.pl-2.font-weight-bold(@click="isExpanded = !isExpanded")
    span General details
    v-tooltip(text="123" )
      template(v-slot:activator="{ props }")
        v-icon(v-bind="props").pl-2 fa-solid fa-circle-info
  div(id="expand")
    v-icon(:icon="expansionIcon" size="x-large"
      @click="isExpanded = !isExpanded")
  div(v-show="!isExpanded").py-1
  div(v-show="isExpanded" )
    v-row.px-3.py-1.my-0
      v-col(cols="12").py-0
        v-checkbox(v-model="ignoreMissingFiles"
          hide-details
          label="Ignore missing files ?"
          density="compact" )

    //v-row.px-3.py-1.my-0
    //  v-col(cols="12")
    //    v-checkbox(v-model="ignoreMissingFiles"
    //      hide-details
    //      label="Ignore missing files ?"
    //      density="compact" )

    v-row.px-3.py-1.my-0
      v-col(:cols="editStartTc ? 1 : 12").py-0
        v-checkbox(v-model="editStartTc" hide-details
        :label="editStartTc ? '': 'Specify Start TC ?'" density="compact" )
      v-col(v-show="editStartTc" cols="11").py-0
        v-text-field(v-model="startTc"
        label="Start TC" density="compact"
          :rules="[rules.required, rules.tcOrIntFormat]"
          hint="Frames count or TC (hh:mm:ss:;ff)")

</template>

<script>

export default {
  name: "GeneralDetails",
  components: {},
  computed: {
    expansionIcon(){
      if (this.isExpanded === false){
        return "fa-solid fa-caret-down"
      } else{
        return "fa-solid fa-caret-right"
      }
    },
    ignoreMissingFiles: {
      get() {
        return this.$store.getters["generalDetails/ignoreMissingFiles"]
      },
      set(value) {
        this.$store.dispatch('generalDetails/updateIgnoreMissingFiles', value)
      }
    },
    editStartTc: {
      get() {
        return this.$store.getters["generalDetails/editStartTc"]
      },
      set(value) {
        this.$store.dispatch('generalDetails/updateEditStartTc', value)
      }
    },
    startTc: {
      get() {
        return this.$store.getters["generalDetails/startTc"]
      },
      set(value) {
        this.$store.dispatch('generalDetails/updateStartTc', value)
      }
    },
  },
  methods: {

  },
  data: function(){
    return {
      tcRegexp: "^([0-1][0-9]|[0-2][0-3]):([0-5][0-9]):([0-5][0-9])[:;]([0-6][0-9])$",
      intRegexp: "^\\d+$",
      rules: {
        required: value => !!value || 'Frames count or TC (hh:mm:ss:;ff) is required',
        tcOrIntFormat: value => value.match(this.intRegexp) || value.match(this.tcRegexp) || 'Frames count or TC (hh:mm:ss:;ff) is required',
      },
      isExpanded: true,
    }
  }
}
</script>

<style scoped>
fieldset{
  border-style: dashed;
}
</style>