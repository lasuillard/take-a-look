<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
  <head>
    <link href="https://fonts.googleapis.com/css?family=Roboto:100,300,400,500,700,900" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/@mdi/font@4.x/css/materialdesignicons.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/vuetify@2.x/dist/vuetify.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/vue@2.x/dist/vue.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/vuetify@2.x/dist/vuetify.js"></script>
    <script src="https://unpkg.com/axios/dist/axios.min.js"></script>
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no, minimal-ui">
    <title>Take a Look</title>
  </head>
  <body>
    <div id="app">
      <v-app>
        <v-content>
          <v-container>
            <h1>Hello JSP! (feat. Vuetify)</h1>
            <h3>{{ ping }}</h3>
          </v-container>
        </v-content>
      </v-app>
    </div>
  </body>
  <script>
    new Vue({
      el: '#app',
      vuetify: new Vuetify(),
      data: () => ({
        ping: '-'
      }),
      created: async function () {
        let { data } = await axios.get('/api/ping')
        this.ping = data.ping
      }
    })
  </script>
</html>
