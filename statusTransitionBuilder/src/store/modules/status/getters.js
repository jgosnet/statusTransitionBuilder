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
        };
        if (statusItem.includeNotification){
          itemStatuses[statusItem.name]['subject'] = statusItem.subject;
          itemStatuses[statusItem.name]['endpoints'] = statusItem.endpoints;
          itemStatuses[statusItem.name]['attachments'] = statusItem.attachments;
          itemStatuses[statusItem.name]['include_metadata'] = [];
          for (const mdObj of statusItem.includeMetadata){
            itemStatuses[statusItem.name]['include_metadata'].push("!!"+mdObj.name + ", "+  mdObj.jmespath + "!!");
          }
        }

      }

      let itemTransitions = {}
      console.log("!!!!!!")
      console.log(stepItem)
      for (const transitionItem of stepItem.transitions){
        itemTransitions[transitionItem.name] = [];
        for (const transOperation of transitionItem.operations){

          let transitionOp = {
            operation: transOperation.opType
          }
          if (transOperation.opType === 'clear'){
            transitionOp['groups'] = transOperation.groups;
          } else{
            transitionOp['keys'] = transOperation.keys;
          }
          if (transOperation.otherStepName){
            transitionOp['step_name'] = transOperation.stepName;
          }
          itemTransitions[transitionItem.name].push(transitionOp)
        }
      }

      res[stepItem.name] = {
        statuses: itemStatuses,
        transitions: itemTransitions,
      }
    }
    let resString = "STATUS_TRANSITIONS = " + JSON.stringify(res, null, 2)
      .replaceAll('"!!', '("').replaceAll('!!"', '")')
      .replaceAll('true', 'True').replaceAll('false', 'False');
    return resString
  },
  statusList(state){
    return state.status;
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
  // eslint-disable-next-line no-unused-vars
  possibleMessages(state){
    console.log("getting possible messages")
    return ['test123', 'test'];
    // let items = [];
    // for (const stepItem of state.status){
    //   for (const statusItem of stepItem.status){
    //     if (!items.includes(statusItem.message) && statusItem.message !== ''){
    //       items.push(statusItem.message)
    //     }
    //
    //   }
    // }
    // return items;
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
  },
  availableStepNames(state){
    return state.status.map(obj => obj.name);
  },
  stepNameForm(state){
    return state.stepNameForm;
  }
}