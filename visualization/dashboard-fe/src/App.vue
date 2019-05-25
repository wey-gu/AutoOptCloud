<template>
  <v-app dark>
    <v-toolbar dark fixed app clipped-right>
      <v-toolbar-side-icon @click.stop="drawer = !drawer"></v-toolbar-side-icon>
      <v-toolbar-title class="headline">
        <span class="font-weight-light">Cloud</span>
        <span>Optimization</span>
      </v-toolbar-title>
      <v-spacer></v-spacer>
    </v-toolbar>

    <v-navigation-drawer v-model="drawer" absolute temporary>
      <v-list class="pa-1">
        <v-list-tile avatar>
          <v-list-tile-avatar>
            <v-icon>settings</v-icon>
          </v-list-tile-avatar>

          <v-list-tile-content>
            <v-list-tile-title class="font-weight-light">UltraCloud Opt Toolchain</v-list-tile-title>
          </v-list-tile-content>
        </v-list-tile>
      </v-list>

      <v-list class="pt-1" dense>
        <v-divider light></v-divider>

        <v-list-tile>
          <v-list-tile-avatar>
            <v-icon>show_chart</v-icon>
          </v-list-tile-avatar>
          <v-list-tile-content>
            <v-btn to="/" flat>
              <v-list-tile-title class="font-weight-light">Dashboard</v-list-tile-title>
            </v-btn>
          </v-list-tile-content>
        </v-list-tile>

        <v-list-tile>
          <v-list-tile-avatar>
            <v-icon>table_chart</v-icon>
          </v-list-tile-avatar>
          <v-list-tile-content>
            <v-btn to="/datatable" flat>
              <v-list-tile-title class="font-weight-light">Data Sheet</v-list-tile-title>
            </v-btn>
          </v-list-tile-content>
        </v-list-tile>
      </v-list>
    </v-navigation-drawer>
    <v-content>
      <v-container fluid fill-height>
        <keep-alive>
          <router-view></router-view>
        </keep-alive>
      </v-container>
    </v-content>

    <v-footer dark height="auto">
      <v-card class="flex" flat tile>
        <v-card-actions class="grey darken-3 justify-center font-weight-light">
          &copy;2019
          &nbsp;— Team MlxCl — Ericsson
        </v-card-actions>
      </v-card>
    </v-footer>
  </v-app>
</template>

<script>
export default {
  name: "App",
  components: {},
  data() {
    return {
      drawer: false,
      activeBtn: 1,
      showNav: true
    };
  },
  created() {
    this.$store.dispatch("getData");
  }
};
</script>
