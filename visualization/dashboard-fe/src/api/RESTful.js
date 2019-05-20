import axios from 'axios'
import config from '../config'

export default {
    getData (commitCallback) {
      const URL = config.backendURL + '/data'
      axios.get(URL)
        .then((response) => {
          let parsedPayload = JSON.parse(response.data)
          commitCallback('setData', parsedPayload)
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error)
        })
    }
  }