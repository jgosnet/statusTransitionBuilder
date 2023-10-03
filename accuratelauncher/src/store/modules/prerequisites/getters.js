export default {
  pl_accurate(){
    const python = require('raw-loader!@/assets/code/__pl_accurate.py').default;
    return python;
  },
    pl_logging(){
    const python = require('raw-loader!@/assets/code/__pl_logging.py').default;
    return python;
  },
    pl_files(){
    const python = require('raw-loader!@/assets/code/__pl_files.py').default;
    return python;
  },
    pl_technical(){
    const python = require('raw-loader!@/assets/code/__pl_technical.py').default;
    return python;
  },
}