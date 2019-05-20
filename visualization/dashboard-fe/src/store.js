import Vue from "vue"
import Vuex from "vuex"

import client from "./api/RESTful"

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    data: {
      handsontable_datas: {},
      charjs_datas: {},
    },
  },
  getters: {
    chart_data_perf: state => {
      return state.data.charjs_datas.peformance
    },
    chart_data_w: state => {
      return state.data.charjs_datas.weighers
    },
    handsontable_data: state => {
      return state.data.handsontable_datas.weighers
    },
  },
  mutations: {
    setData (state, payload) {
      state.data.handsontable_datas = payload["handsontable_datas"]
      state.data.charjs_datas = payload["charjs_datas"]
      // eslint-disable-next-line
      // console.log("[DEBUG] setData: " + state.data)
    },
    setHistory (state, payload) {
      let parsedPayload = JSON.parse(payload)
      let name = Object.keys(parsedPayload)[0]
      Vue.set(state.histories, name, parsedPayload[name])
    },
  },
  actions: {
    getData ({commit}) {
      // initially fetch Data from backend
      // context.commit is the callback passed to client.getData
      client.getData(commit)
    },
    // eslint-disable-next-line
    SOCKET_updateData ({commit}, data) {
      // eslint-disable-next-line
      // console.log('[DEBUG] SOCKET_updateData:\n\t' + data)
      // update_board from socket.io server
      commit('setData', data)
    },
  }
})
