<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
  <head>
    <%@ include file="/WEB-INF/jsp/static.jsp" %>
    <%@ include file="/WEB-INF/jsp/meta.jsp" %>
    <title>Take a Look &mdash; Predict</title>
  </head>
  <body>
    <v-app id="app">
      <v-content>
        <v-container class="pa-8" fluid>
          <v-row>
            <v-col cols="12" lg="6">
              <v-card>
                <v-card-title>Predict</v-card-title>
                <v-card-text>
                  <v-form class="px-3 py-1">
                    <v-file-input v-model="form.image" accept="image/*" label="Image input"></v-file-input>
                    <v-select
                      v-model="form.label"
                      :items="['Cat', 'Dog']"
                      prepend-icon="mdi-label"
                      label="Label of image"
                    ></v-select>
                    <v-select
                      v-model="form.model"
                      :items="['SVM', 'CNN']"
                      prepend-icon="mdi-graph"
                      hide-details
                      single-line
                      label="Model to use"
                    ></v-select>
                    <v-layout class="mt-6 justify-end">
                      <v-btn text color="primary" :disabled="loading" @click="predict">Submit</v-btn>
                    </v-layout>
                  </v-form>
                </v-card-text>
              </v-card>
            </v-col>
            <v-col cols="12" lg="6">
              <v-card :loading="loading">
                <v-card-title>Result</v-card-title>
                <v-card-text>
                  <p class="subtitle-1">&dash; Request</p>
                  <div 
                    v-for="key in Object.keys(form)" 
                    :key="key"
                    class="body-2 pl-3 mb-3"
                    >{{ key }}: {{ form[key] }}<br/>
                  </div>

                  <p class="subtitle-1">&dash; Response</p>
                  <div 
                    v-for="key in Object.keys(result)" 
                    :key="key"
                    class="body-2 pl-3 mb-3"
                    >{{ key }}: {{ result[key] }}<br/>
                  </div>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
        </v-container>
      </v-content>
      <%@ include file="/WEB-INF/jsp/components/appbar.jsp" %>
      <%@ include file="/WEB-INF/jsp/components/bottom-nav-bar.jsp" %>
      <%@ include file="/WEB-INF/jsp/components/footer.jsp" %>
    </v-app>
  </body>
  <script>
    var app = new Vue({
      el: '#app',
      vuetify: new Vuetify(),
      data: () => ({
        meta: {
          context: 'predict'
        },
        // request
        form: {
          image: null,
          label: null,
          model: null
        },
        // response
        loading: false,
        result: {
          id: null,
          prediction: null,
        }
      }),
      methods: {
        predict () {
          this.loading = true
          setTimeout(() => {
            this.loading = false
            this.result.id = 3
            this.result.prediction = 'Dog'
          }, 4000)
        }
      }
    })
  </script>
</html>
