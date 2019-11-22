<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
  <head>
    <%@ include file="/WEB-INF/jsp/static.jsp" %>
    <%@ include file="/WEB-INF/jsp/meta.jsp" %>
    <title>Take a Look</title>
  </head>
  <body>
    <div id="app">
      <v-app>
        <v-parallax 
          src="https://cdn.vuetifyjs.com/images/backgrounds/vbanner.jpg"
          style="position: absolute; top: 50vh; right: 0; width: 100%; height: 60vh; z-index: 0;"
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
                height="40vh"
                continuous cycle interval="4000"
                hide-delimiters
              >
                <v-carousel-item
                  v-for="(item, i) in carousel.items"
                  id="recent-submit-1"
                  :key="i"
                  :src="item.src"
                  link :href="item.link"
                ></v-carousel-item>
              </v-carousel>
            </v-col>
          </v-row>
          <v-row class="mt-6" align="center" justify="center">
            <v-col cols="11" lg="8">
              <p class="font-weight-thin display-1 white--text">Models we provide:</p>
              <v-expansion-panels id="model-previews" inset>
                <v-expansion-panel id="model-1">
                  <v-expansion-panel-header>SVM (Support Vector Machine)</v-expansion-panel-header>
                  <v-expansion-panel-content id="model-1-content">
                    <v-container>
                      Oh, some saying
                    </v-container>
                    <v-flex class="text-right">
                      <v-btn id="model-1-link" text link href="/model/svm">Let's see</v-btn>
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
                      <v-btn id="model-2-link" text link href="/model/cnn">Let's see</v-btn>
                    </v-flex>
                  </v-expansion-panel-content>
                </v-expansion-panel>
              </v-expansion-panels>
            </v-col>
          </v-row>
          <br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
        </v-content>
        <%@ include file="/WEB-INF/jsp/components/bottom-nav-bar.jsp" %>
      </v-app>
    </div>
  </body>
  <script>
    new Vue({
      el: '#app',
      vuetify: new Vuetify(),
      data: () => ({
        meta: {
          context: 'index'
        },
        carousel: {
          items: [
            {
              src: 'https://cdn.vuetifyjs.com/images/carousel/squirrel.jpg',
              link: '/history/1',
            },
            {
              src: 'https://cdn.vuetifyjs.com/images/carousel/sky.jpg',
              link: '/history/2',
            },
            {
              src: 'https://cdn.vuetifyjs.com/images/carousel/bird.jpg',
              link: '/history/3',
            },
            {
              src: 'https://cdn.vuetifyjs.com/images/carousel/planet.jpg',
              link: '/history/4',
            },
          ]
        }
      }),
    })
  </script>
</html>
