<template>
  <v-app>

    <v-toolbar
      dark
      fixed
      app
      clipped-right
    >
      <v-toolbar-side-icon @click.stop="drawer = !drawer"></v-toolbar-side-icon>
          <v-toolbar-title class="headline" >
            <span class="font-weight-light">
              Cloud </span><span>Optimization
            </span>
          </v-toolbar-title>
      <v-spacer></v-spacer>

    </v-toolbar>
    <v-navigation-drawer
      fixed
      v-model="drawer"
      app
      temporary
    >
      <v-list dense>
        <v-list-tile @click.stop="left = !left">
          <v-list-tile-action>
            <v-icon>exit_to_app</v-icon>
          </v-list-tile-action>
          <v-list-tile-content>
            <v-list-tile-title>Open Temporary Drawer</v-list-tile-title>
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

  <v-footer
    dark
    height="auto"
  >
    <v-card
      class="flex"
      flat
      tile
    >
      <v-card-actions class="grey darken-3 justify-center">
        &copy;2019
        &nbsp;— &nbsp; Team MlxCl — 
        <strong>&nbsp; Ericsson</strong>
      </v-card-actions>
    </v-card>
  </v-footer>

  </v-app>
</template>

<script>

export default {
  name: 'App',
  components: {
  },
  data () {
    return {
      drawer: false,
    }
  },
  created () {
    this.$store.dispatch('getData')
  },
}
</script>
