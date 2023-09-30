export default {
  // eslint-disable-next-line no-unused-vars
  launcherProviderData(state, getters, rootState, rootGetters){
    console.log("loading code")
    let code = ""
    if (getters['woType'] === 'edit'){
      const python = require('raw-loader!@/assets/code/launcherEdit.py')
      code = python.default
    } else if (getters['woType'] === 'validate'){
      const python = require('raw-loader!@/assets/code/launcherValidate.py')
      code = python.default
    }else if (getters['woType'] === 'basic'){
      const python = require('raw-loader!@/assets/code/launcherBasic.py')
      code = python.default
    }

    if (getters['includehardcodedDpd']){
      const dpd = rootGetters['jsonForm']
      console.log("loading json form: ")
      console.log(dpd)

      let formattedDpd = `dpd = ${JSON.stringify(dpd)}`
        .replace('false', 'False')
        .replace('true', 'True')
        .replace('null', 'None')

      code = code.replace("#REPLACE_DPD", formattedDpd)
    }

    return code;

  },
  woType(state){
    return state.woType;
  },
  includehardcodedDpd(state){
    return state.includehardcodedDpd;
  },
}