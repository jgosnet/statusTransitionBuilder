<template lang="pug">
v-container(fluid).border-solid
  v-row
    v-col(cols="8")
      ConfigurationBase
    v-spacer
    v-col(cols="4")
      //TheImporter.mb-2
      JinjaHelper.mb-2
      JsonViewerPage.mb-2
</template>

<script>
import JsonViewerPage from "@/components/JsonViewerPage";
import ConfigurationBase from "@/components/ConfigurationBase";
import JinjaHelper from "@/components/Jinja/JinjaHelper";
import TheImporter from "@/components/Importer/TheImporter";
export default {
  name: "DpdBuilderPage",
  components: {TheImporter, JinjaHelper, ConfigurationBase, JsonViewerPage},
  data: function() {
    return {
      dismissSecs: 5,
      dismissCountDown: 0,
      stringOutput: "test123",
    }
  },
  methods: {
    // eslint-disable-next-line no-unused-vars
    clipboardSuccessHandler () {
      console.log('success')
      this.dismissCountDown = this.dismissSecs
      setTimeout(() => {
        this.dismissCountDown = 0
      }, 3000)
    },

    // eslint-disable-next-line no-unused-vars
    clipboardErrorHandler () {
      console.log('error')
    }
  }
}
</script>

<style scoped>

</style>