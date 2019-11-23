<v-bottom-navigation app id="bottom-navbar" :value="meta.context">
  <v-layout class="justify-space-around">
    <v-btn id="navbar-link-home" value="index" href="/">
      <span>Home</span>
      <v-icon>mdi-home</v-icon>
    </v-btn>
    <v-btn id="navbar-link-model" value="model" href="/model">
      <span>Model</span>
      <v-icon>mdi-graph</v-icon>
    </v-btn>
    <v-btn id="navbar-link-predict" value="predict" href="/predict">
      <span>Predict</span>
      <v-icon>mdi-robot</v-icon>
    </v-btn>
  </v-layout>
</v-bottom-navigation>
