<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
  <head>
    <%@ include file="/WEB-INF/jsp/static.jsp" %>
    <%@ include file="/WEB-INF/jsp/meta.jsp" %>
    <title>Take a Look</title>
  </head>
  <body>
    <v-app id="app">
      <v-parallax 
        src="/static/ai-parallax.jpg"
        style="position: absolute; top: 60vh; right: 0; width: 100%; height: 50vh; z-index: 0;"
      ></v-parallax>
      <v-content style="z-index: 1;">
        <v-container fluid>
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
                  v-for="(img, i) in carousel.images"
                  :id="'recent-submit-' + i"
                  :key="i"
                  :src="img"
                ></v-carousel-item>
              </v-carousel>
            </v-col>
          </v-row>
          <v-row class="mt-6" align="center" justify="center">
            <v-col cols="11" lg="8">
              <p class="font-weight-thin display-1 white--text">Models we provide:</p>
              <v-expansion-panels id="model-previews" inset>
                <v-expansion-panel v-for="(model, i) in models" :key="i" :id="'model-' + i">
                  <v-expansion-panel-header>{{ model.aka.toUpperCase() }} ({{ model.name }})</v-expansion-panel-header>
                  <v-expansion-panel-content :id="'model-' + i + '-content'">
                    <v-container>
                      {{ model.intro }}
                    </v-container>
                  </v-expansion-panel-content>
                </v-expansion-panel>
              </v-expansion-panels>
            </v-col>
          </v-row>
          <div style="height: 10vh;"></div>
        </v-container>
      </v-content>
      <%@ include file="/WEB-INF/jsp/components/appbar.jsp" %>
      <%@ include file="/WEB-INF/jsp/components/bottom-nav-bar.jsp" %>
      <%@ include file="/WEB-INF/jsp/components/footer.jsp" %>
    </v-app>
  </body>
  <script>
    var app =new Vue({
      el: '#app',
      vuetify: new Vuetify(),
      data: () => ({
        meta: {
          context: 'index'
        },
        carousel: {
          images: ['/static/kaggle-dogs-vs-cats.jpg', ]  // default image
        },
        models: []
      }),
      async created () {
        // carousel images
        var response = await axios.get('/api/history/')
        this.carousel.images = response.data.results.map(i => i.img)

        // model previews
        var response = await axios.get('/api/model/')
        this.models = response.data.results
      }
    })
  </script>
</html>
