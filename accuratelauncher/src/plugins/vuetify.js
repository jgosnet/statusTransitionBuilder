import '@fortawesome/fontawesome-free/css/all.css' // Ensure your project is capable of handling css files
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as labsComponents from 'vuetify/labs/components'
import { aliases, fa } from 'vuetify/iconsets/fa'

export default createVuetify({
  components: {
    ...components,
    ...labsComponents,
  },
  icons: {
    defaultSet: 'fa',
    aliases,
    sets: {
      fa,
    },
  },
})