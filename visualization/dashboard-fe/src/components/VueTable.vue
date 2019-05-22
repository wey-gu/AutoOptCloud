<template>
  <!-- <v-container> -->
  <v-layout>
    <v-flex xs12>
      <v-data-table
        :v-if="!this.loading"
        class="elevation-1"
        :headers="this.get_headers"
        :items="this.table_datas"
        :rows-per-page-items="[50, 100]"
      >
        <template slot="items" slot-scope="props">
          <td class="text-xs-right">{{ props.item.id }}</td>
          <td class="text-xs-right">{{ props.item.benchmark }}</td>
          <td class="text-xs-right">{{ props.item.timestamp }}</td>
          <td class="text-xs-right">{{ props.item.rabbitmq }}</td>
          <td class="text-xs-right">{{ props.item.fileio }}</td>
          <td class="text-xs-right">{{ props.item.mysql }}</td>
          <td class="text-xs-right">{{ props.item.iperf3 }}</td>
          <td class="text-xs-right">{{ props.item.cpu }}</td>
          <td class="text-xs-right">{{ props.item.w_ram }}</td>
          <td class="text-xs-right">{{ props.item.w_disk }}</td>
          <td class="text-xs-right">{{ props.item.w_user_p }}</td>
          <td class="text-xs-right">{{ props.item.w_iowait_p }}</td>
          <td class="text-xs-right">{{ props.item.w_frequency }}</td>
          <td class="text-xs-right">{{ props.item.w_idle_p }}</td>
          <td class="text-xs-right">{{ props.item.w_cpu_p }}</td>
          <td class="text-xs-right">{{ props.item.w_kernel_p }}</td>
        </template>
      </v-data-table>
    </v-flex>
  </v-layout>
  <!-- </v-container> -->
</template>

<script>
// import Vuetable from "vuetable-2";
import { mapGetters } from "vuex";

export default {
  data() {
    return {};
  },
  components: {
    // Vuetable
  },
  computed: {
    ...mapGetters(["table_datas", "get_headers", "loading"])
  }
};
</script>

<style>
</style>