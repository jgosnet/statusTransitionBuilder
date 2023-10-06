<template lang="pug">
v-container(fluid)
  v-row
    v-col(cols="8")
      ConfigurationBase
    v-spacer
    v-col(cols="4").py-0.pl-0
      ImporterPage.mb-3
      ExampleViewer.mb-3
      FormViewer.mb-3

</template>

<script>
import FormViewer from "@/components/Viewer/FormViewer";
import ConfigurationBase from "@/components/Configuration/ConfigurationBase";
import ExampleViewer from "@/components/Viewer/ExampleViewer";
import ImporterPage from "@/components/Import/ImporterPage";

export default {
  name: "MainPage",
  components: {
    ImporterPage,
    ExampleViewer,
    ConfigurationBase,
    FormViewer

  },
  data(){
    return {
      selectedTab: 'providerData',
      expandDepth: 5,
      stringOutput: "",
    }
  },
  methods: {
  },
  computed: {
  },
}
</script>

<style scoped>

</style>