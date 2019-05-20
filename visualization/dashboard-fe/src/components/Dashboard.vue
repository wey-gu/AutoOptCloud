<template>
  <v-container>
    <v-layout
      wrap
    >

    <v-flex xs12 md2>

    </v-flex>

    <v-flex xs12 md10>
      <div class="container">
        <performance-chart
          :chart-data="this.chart_data_perf"
        >
        </performance-chart>
      </div>

      <div class="container">
        <weigher-chart
          :chart-data="this.chart_data_w"
        >
        </weigher-chart>
      </div>

    </v-flex>

    </v-layout>
  </v-container>
</template>

<script>
  import { mapGetters } from 'vuex'
  import PerformanceChart from './PerformanceChart.vue'
  import WeigherChart from './WeigherChart.vue'


  export default {
    data: () => ({
    }),
    components: {
      PerformanceChart,
      WeigherChart
    },
    computed: {
      ...mapGetters([
        "chart_data_perf",
        "chart_data_w"
      ])
    }
  }

</script>

<style>

</style>
