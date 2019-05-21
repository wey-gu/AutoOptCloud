import Vue from "vue";
import Vuex from "vuex";

import client from "./api/RESTful";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    data: {
      handsontable_datas: {},
      charjs_datas: {
        peformance: {
          labels: [],
          datasets: [
            {
              data: [0]
            }
          ]
        },
        weighers: {
          labels: [],
          datasets: []
        }
      }
    }
  },
  getters: {
    chart_data_perf: state => {
      return state.data.charjs_datas.peformance;
    },
    chart_data_w: state => {
      return state.data.charjs_datas.weighers;
    },
    handsontable_data: state => {
      return state.data.handsontable_datas.weighers;
    }
    // max_iteration: state => {
    //   console.log(
    //     "DEBUG: " + state.data.charjs_datas.peformance.datasets[0].data
    //   );
    //   return Math.max(state.data.charjs_datas.peformance.datasets[0].data);
    // },
    // max_iteration_index: state => {
    //   let benchmarkData = state.data.charjs_datas.peformance.datasets[0].data;
    //   return benchmarkData.indexOf(Math.max(benchmarkData));
    // }
  },
  mutations: {
    setData(state, payload) {
      state.data.handsontable_datas = payload["handsontable_datas"];
      state.data.charjs_datas = payload["charjs_datas"];
      // eslint-disable-next-line
      // console.log("[DEBUG] setData: " + state.data)
    }
  },
  actions: {
    getData({ commit }) {
      // initially fetch Data from backend
      // context.commit is the callback passed to client.getData
      client.getData(commit);
    },
    // eslint-disable-next-line
    SOCKET_updateData({ commit }, data) {
      // eslint-disable-next-line
      // console.log('[DEBUG] SOCKET_updateData:\n\t' + data)
      // update_board from socket.io server
      commit("setData", data);
    }
  }
});
