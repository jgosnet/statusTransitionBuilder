import cookie from 'vue-cookies'
import {api} from "@/scripts/axios_config";


export default {
  updateVideoLabel(context, value){
    context.commit('updateVideoLabel', value)
  },
  updateVideoAssetName(context, value){
    context.commit('updateVideoAssetName', value)
  },
  updateIncludeAssetName(context, value){
    context.commit('updateIncludeAssetName', value)
  },
  async loadProjectsList(context) {
    const url = `config/project`
    this.isLoading = true
    context.commit('updateErrorMessage', "")
    api.get(url)
      .then((response) => {
        if (response.statusText === 'OK'){
          // Following order:
          // 1\ use cookies to setup array and order
          // 2\ insert remaining items
          // update vuex
          let newProjectsList = []
          console.log(`getting projects list..`)
          if (cookie.isKey('selectedProjects')){
            console.log(`Cookies found for: selectedProjects`)
            const cachedProjectsList = JSON.parse(JSON.stringify(cookie.get('selectedProjects')));
            console.log(cachedProjectsList)
            for (const cachedProject of cachedProjectsList){
              const filteredArray = response.data.filter((project) => cachedProject.id == project.id);
              if (filteredArray.length > 0){
                newProjectsList.push(cachedProject)
              }
            }
          }
          console.log(`Cached projects loaded: `)
          console.log(newProjectsList)
          for (let obj of response.data){
            const filteredArray = newProjectsList.filter((project) => project.id == obj.id);
            if (filteredArray.length === 0){
              newProjectsList.push({
                id: obj.id,
                name: obj.name,
                type: obj.project_type,
                path: obj.local_path,
                config_type: obj.config_type,
              })
            }
          }
          context.commit('updateProjectsList', newProjectsList)
          return response.data
        }
        console.log(response.data)
      })
      .catch((error) => {
        console.log(error)
        const errorMessage = 'Failed to get the project list from server'
        context.dispatch('snackbar/showMessage', {
            message: errorMessage
          },
          { root: true }
        )
        context.commit('updateErrorMessage', errorMessage)
      })
      .finally(() => {
      })
  },

}