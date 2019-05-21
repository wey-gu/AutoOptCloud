<template>
  <v-container>
    <v-layout>
      <v-flex xs12 md2>
        <v-container>
          <v-card class="text-xs-center hover">
            <v-card-text
              class="text-xs-center display-2 font-weight-regular"
            >{{ chart_data_perf.labels.length }}</v-card-text>
            <v-card-text class="text-xs-center body-1 grey--text font-weight-light">iterations</v-card-text>
          </v-card>
        </v-container>

        <!-- <v-container>
          <v-card class="text-xs-center hover">
            <v-card-text class="text-xs-center display-2 font-weight-regular">{{ max_iteration }}</v-card-text>
            <v-card-text class="text-xs-center body-1 grey--text font-weight-light">max benchmark</v-card-text>
          </v-card>
        </v-container>

        <v-container>
          <v-card class="text-xs-center hover">
            <v-card-text
              class="text-xs-center display-2 font-weight-regular"
            >{{ max_iteration_index }}</v-card-text>
            <v-card-text
              class="text-xs-center body-1 grey--text font-weight-light"
            >max benchmark iteration</v-card-text>
          </v-card>
        </v-container>-->
      </v-flex>
      <v-flex xs12 md12>
        <v-container>
          <v-card class="dark elevation-5" color="blue-grey darken-4">
            <v-card-text primary-title>
              <div class="chart-title">
                <h2
                  class="text-xs-center grey--text text--lighten-1"
                >Performance impacted per iteration</h2>
              </div>
            </v-card-text>
            <v-container>
              <performance-chart
                :chart-data="this.chart_data_perf"
                :chart-option="{maintainAspectRatio:false}"
                :height="160"
              ></performance-chart>
            </v-container>
          </v-card>
        </v-container>

        <v-container>
          <v-card class="dark elevation-5" color="blue-grey darken-4">
            <v-card-text primary-title>
              <div class="chart-title">
                <h2 class="text-xs-center grey--text text--lighten-1">Tuned weighers per iteration</h2>
              </div>
            </v-card-text>
            <v-container>
              <weigher-chart
                :chart-data="this.chart_data_w"
                :chart-option="{maintainAspectRatio:false}"
                :height="160"
              ></weigher-chart>
            </v-container>
          </v-card>
        </v-container>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import { mapGetters } from "vuex";
import PerformanceChart from "./PerformanceChart.vue";
import WeigherChart from "./WeigherChart.vue";

export default {
  data: () => ({
    // https://vue-chartjs.org/api/#canvas
    // gradientBlue: null,
    // gradientGreen: null,
    // gradientOrange: null,
    // gradientRed: null,
    // gradientPink: null,
    // gradientIdigo: null,
    // gradientYellow: null,
    // gradientTeal: null,
    // gradientList: null,
    // colorList: null,
  }),
  components: {
    PerformanceChart,
    WeigherChart
  },
  mounted() {
    // let canvas = this.$refs.canvas
    // this.gradientBlue = canvas.getContext('2d').createLinearGradient(0, 0, 0, 450)
    // this.gradientGreen = canvas.getContext('2d').createLinearGradient(0, 0, 0, 450)
    // this.gradientOrange = canvas.getContext('2d').createLinearGradient(0, 0, 0, 450)
    // this.gradientRed = canvas.getContext('2d').createLinearGradient(0, 0, 0, 450)
    // this.gradientPink = canvas.getContext('2d').createLinearGradient(0, 0, 0, 450)
    // this.gradientIdigo = canvas.getContext('2d').createLinearGradient(0, 0, 0, 450)
    // this.gradientYellow = canvas.getContext('2d').createLinearGradient(0, 0, 0, 450)
    // this.gradientTeal = canvas.getContext('2d').createLinearGradient(0, 0, 0, 450)
    // this.gradientBlue.addColorStop(0, "rgba(33, 150, 243, 0.5)")
    // this.gradientBlue.addColorStop(0.5, "rgba(33, 150, 243, 0.25)")
    // this.gradientBlue.addColorStop(1, "rgba(33, 150, 243, 0)")
    // this.gradientGreen.addColorStop(0, "rgba(76, 175, 80, 0.5)")
    // this.gradientGreen.addColorStop(0.5, "rgba(76, 175, 80, 0.25)")
    // this.gradientGreen.addColorStop(1, "rgba(76, 175, 80, 0)")
    // this.gradientOrange.addColorStop(0, "rgba(255, 152, 0, 0.5)")
    // this.gradientOrange.addColorStop(0.5, "rgba(255, 152, 0, 0.25)")
    // this.gradientOrange.addColorStop(1, "rgba(255, 152, 0, 0)")
    // this.gradientRed.addColorStop(0, "rgba(244, 67, 54, 0.5)")
    // this.gradientRed.addColorStop(0.5, "rgba(244, 67, 54, 0.25)")
    // this.gradientRed.addColorStop(1, "rgba(244, 67, 54, 0)")
    // this.gradientPink.addColorStop(0, "rgba(233, 30, 99, 0.5)")
    // this.gradientPink.addColorStop(0.5, "rgba(233, 30, 99, 0.25)")
    // this.gradientPink.addColorStop(1, "rgba(233, 30, 99, 0)")
    // this.gradientIdigo.addColorStop(0, "rgba(63, 81, 181, 0.5)")
    // this.gradientIdigo.addColorStop(0.5, "rgba(63, 81, 181, 0.25)")
    // this.gradientIdigo.addColorStop(1, "rgba(63, 81, 181, 0)")
    // this.gradientYellow.addColorStop(0, "rgba(255, 235, 59, 0.5)")
    // this.gradientYellow.addColorStop(0.5, "rgba(255, 235, 59, 0.25)")
    // this.gradientYellow.addColorStop(1, "rgba(255, 235, 59, 0)")
    // this.gradientTeal.addColorStop(0, "rgba(0, 150, 136, 0.5)")
    // this.gradientTeal.addColorStop(0.5, "rgba(0, 150, 136, 0.25)")
    // this.gradientTeal.addColorStop(1, "rgba(0, 150, 136, 0)")
    // this.gradientList = [
    //   this.gradientBlue,
    //   this.gradientGreen,
    //   this.gradientOrange,
    //   this.gradientRed,
    //   this.gradientPink,
    //   this.gradientIdigo,
    //   this.gradientYellow,
    //   this.gradientTeal
    // ]
  },
  computed: {
    ...mapGetters([
      "chart_data_perf",
      "chart_data_w"
      // "max_iteration",
      // "max_iteration_index"
    ])
  }
};
</script>

<style>
.chart-title h2 {
  font-family: "Ericsson Capital TT", Times, serif;
  text-align: center;
}
</style>
