export default {
  // eslint-disable-next-line no-unused-vars
  jsonForm(state, getters, rootState, rootGetters){
    // eslint-disable-next-line no-unused-vars
    // const videoDetails = rootGetters["videoDetails/jsonForm"];
    let res = {}
    for (const stepItem of state.status){
      console.log("status item:")
      console.log(stepItem.name)

      let itemStatuses = {}
      for (const statusItem of stepItem.status){
        itemStatuses[statusItem.name] = {
          message: statusItem.message,
          group: statusItem.group,
          icon: statusItem.icon,
          color: statusItem.color,
        }
      }

      let itemTransitions = {}
      for (const transitionItem of stepItem.transitions){
        itemTransitions[transitionItem.name] = {
          message: transitionItem.message
        }
      }

      res[stepItem.name] = {
        status: itemStatuses,
        transitions: itemTransitions,
      }
    }
    let resString = "STATUS_TRANSITIONS = " + JSON.stringify(res, null, 2);
    return resString
  },
  status(state){
    return state.status;
  },
  possibleGroups(state){
    let items = [];
    for (const stepItem of state.status){
      for (const statusItem of stepItem.status){
        if (!items.includes(statusItem.group) && statusItem.group !== ''){
          items.push(statusItem.group)
        }

      }
    }
    return items;
  },
  possibleMessages(state){
    let items = [];
    for (const stepItem of state.status){
      for (const statusItem of stepItem.status){
        if (!items.includes(statusItem.message) && statusItem.message !== ''){
          items.push(statusItem.message)
        }

      }
    }
    return items;
  },
  possibleEndpoints(state){
    let items = [];
    for (const stepItem of state.status){
      for (const statusItem of stepItem.status){
        if (statusItem.includeNotification){
          for (const endpoint of statusItem.endpoints){
            if (!items.includes(endpoint) && endpoint !== ''){
            items.push(endpoint)
          }
          }
        }
      }
    }
    return items;
  },
  possibleMetadataJmespath(state){
    let items = [];
    for (const stepItem of state.status){
      for (const statusItem of stepItem.status){
        if (statusItem.includeNotification){
          for (const metadata of statusItem.includeMetadata){
            if (!items.includes(metadata.jmespath) && metadata.jmespath !== ''){
            items.push(metadata.jmespath)
          }
          }
        }
      }
    }
    return items;
  },
  possibleOperations(state){
    return state.possibleOperations
  }
}