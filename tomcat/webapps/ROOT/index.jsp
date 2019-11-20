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
        <v-parallax 
          src="https://cdn.vuetifyjs.com/images/backgrounds/vbanner.jpg"
          style="position: absolute; top: 50vh; right: 0; width: 100%; height: 30vh; z-index: 0;"
        ></v-parallax>
        <v-content style="z-index: 1;">
          <v-row class="mt-10" align="center" justify="center">
            <v-col class="text-center" cols="12">
              <h1 class="font-weight-regular text-uppercase display-3">Take a Look</h1>
              <v-divider class="my-6"></v-divider>
              <h4 class="font-weight-thin display-1">Test your image with our trained ML model</h4>
            </v-col>
          </v-row>
          <v-row class="mt-6" align="center" justify="center">
            <v-col cols="8" lg="6">
              <v-carousel id="recent-submits" 
                height="60vh"
                continuous cycle interval="4000"
                hide-delimiters
              >
                <v-carousel-item
                  v-for="(item, i) in carousel.items"
                  :key="i"
                  :src="item.src"
                  link :href="item.link"
                ></v-carousel-item>
              </v-carousel>
            </v-col>
          </v-row>
          <v-row class="mt-6" align="center" justify="center">
            <v-col cols="11" lg="8">
              <p class="font-weight-thin display-1">Models we provide:</p>
              <v-expansion-panels id="model-previews">
                <v-expansion-panel id="model-1">
                  <v-expansion-panel-header>SVM (Support Vector Machine)</v-expansion-panel-header>
                  <v-expansion-panel-content id="model-1-content">
                    <v-container>
                      Oh, some saying
                    </v-container>
                    <v-flex class="text-right">
                      <v-btn id="model-1-link" text link href="/model/svm/">Let's see</v-btn>
                    </v-flex>
                  </v-expansion-panel-content>
                </v-expansion-panel>
                <v-expansion-panel id="model-2">
                  <v-expansion-panel-header>CNN (Convolutional Neural Network)</v-expansion-panel-header>
                  <v-expansion-panel-content id="model-2-content">
                    <v-container>
                      Oh, some saying
                    </v-container>
                    <v-flex class="text-right">
                      <v-btn id="model-2-link" text link href="/model/cnn/">Let's see</v-btn>
                    </v-flex>
                  </v-expansion-panel-content>
                </v-expansion-panel>
              </v-expansion-panels>
            </v-col>
          </v-row>
          <br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
        </v-content>
        <v-bottom-navigation app id="bottom-navbar" value="index">
          <v-btn id="navbar-link-home" value="index" href="/">
            <span>Home</span>
            <v-icon>mdi-home</v-icon>
          </v-btn>
          <v-btn id="navbar-link-history" value="history" href="/history/">
            <span>History</span>
            <v-icon>mdi-view-dashboard</v-icon>
          </v-btn>
          <v-btn id="navbar-link-model" value="model" href="/model/">
            <span>Model</span>
            <v-icon>mdi-robot</v-icon>
          </v-btn>
        </v-bottom-navigation>
      </v-app>
    </div>
  </body>
  <script>
    new Vue({
      el: '#app',
      vuetify: new Vuetify(),
      data: () => ({
        ping: '-',
        meta: {

        },
        carousel: {
          items: [
            {
              src: 'https://cdn.vuetifyjs.com/images/carousel/squirrel.jpg',
              link: '/history/1/',
            },
            {
              src: 'https://cdn.vuetifyjs.com/images/carousel/sky.jpg',
              link: '/history/2/',
            },
            {
              src: 'https://cdn.vuetifyjs.com/images/carousel/bird.jpg',
              link: '/history/3/',
            },
            {
              src: 'https://cdn.vuetifyjs.com/images/carousel/planet.jpg',
              link: '/history/4/',
            },
          ]
        }
      }),
    })
  </script>
</html>
