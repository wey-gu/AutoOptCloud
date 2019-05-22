import Vue from "vue";
import Vuex from "vuex";

import client from "./api/RESTful";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    data: {
      // handsontable_datas: {},
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
      },
      table_datas: [],
      max_benchmark: 0,
      max_benchmark_index: 0,
      headers: [
        {
          text: "",
          value: ""
        }
      ]
    },
    loading: true
  },
  getters: {
    chart_data_perf: state => {
      return state.data.charjs_datas.peformance;
    },
    chart_data_w: state => {
      return state.data.charjs_datas.weighers;
    },
    // handsontable_data: state => {
    //   return state.data.handsontable_datas;
    // },
    table_datas: state => {
      return state.data.table_datas;
    },
    get_headers: state => {
      return state.data.headers;
    },
    max_benchmark: state => {
      return state.data.max_benchmark;
    },
    max_benchmark_index: state => {
      return state.data.max_benchmark_index;
    },
    loading: state => {
      return state.loading;
    }
  },
  mutations: {
    setData(state, payload) {
      // state.data.handsontable_datas = payload["handsontable_datas"];
      state.data.charjs_datas = payload["charjs_datas"];
      state.data.max_benchmark = payload["max_benchmark"];
      state.data.max_benchmark_index = payload["max_benchmark_index"];
      state.data.table_datas = payload["table_datas"];
      state.data.headers = payload["headers"];
      // state.data.headers.splice(0, state.data.headers, ...payload["headers"]);
      state.loading = false;
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
