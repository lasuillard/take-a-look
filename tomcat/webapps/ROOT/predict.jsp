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
                  <v-form id="prediction-form" class="px-3 py-1">
                    <v-file-input 
                      id="upload-image"
                      v-model="form.img"
                      accept="image/*"
                      label="Image input"
                    ></v-file-input>
                    <v-select
                      id="select-label"
                      v-model="form.label"
                      :items="labels"
                      item-text="display_name"
                      item-value="value"
                      prepend-icon="mdi-label"
                      label="Label of image"
                    ></v-select>
                    <v-select
                      id="select-model"
                      v-model="form.model"
                      :items="models"
                      item-text="display_name"
                      item-value="value"
                      prepend-icon="mdi-graph"
                      hide-details
                      label="Model to use"
                    ></v-select>
                    <v-layout class="mt-6 justify-end">
                      <v-btn 
                        id="request-submit"
                        text color="primary"
                        :disabled="loading"
                        @click="predict"
                      >Submit</v-btn>
                    </v-layout>
                  </v-form>
                </v-card-text>
              </v-card>
            </v-col>
            <v-col cols="12" lg="6">
              <v-card :loading="loading">
                <v-card-title>Result</v-card-title>
                <v-card-text>Status: <span id="result-sign">{{ status }}</span></v-card-text>
                <v-card-text>
                  <p class="subtitle-1">&dash; Request Body</p>
                  <div 
                    v-for="key in Object.keys(form)" 
                    :key="'rq-' + key"
                    class="body-2 pl-3 mb-3"
                    >{{ key }}: {{ form[key] }}<br/>
                  </div>

                  <p class="subtitle-1">&dash; Response Data</p>
                  <div 
                    v-for="key in Object.keys(result)" 
                    :key="'rs-' + key"
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
        // page meta & status data
        labels: [],
        models: [],
        status: 'Ready',  // no state machine for it, just for display
        loading: false,
        // request
        form: {
          img: null,
          label: null,
          model: null
        },
        // response
        result: {}
      }),
      methods: {
        predict () {
          this.loading = true
          let data = new FormData()  // for image data transfer
          for (var key in this.form) {
            data.append(key, this.form[key])
          }
          axios.post('/api/history/', data, { 
            headers: {
              'Content-Type': 'multipart/form-data',
            }
          }).then(response => {
            this.status = 'OK'
            this.result = response.data
          }).catch(error => {
            this.status = 'ERROR'
          }).finally(() => {
            this.loading = false
          })
        }
      },
      async created () {
        var option = await axios.options('/api/history/')
        this.labels = option.data.actions.POST.label.choices
        this.models = option.data.actions.POST.model.choices
      }
    })
  </script>
</html>
