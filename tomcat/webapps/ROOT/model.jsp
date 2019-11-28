<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
  <head>
    <%@ include file="/WEB-INF/jsp/static.jsp" %>
    <%@ include file="/WEB-INF/jsp/meta.jsp" %>
    <title>Take a Look &mdash; Model</title>
  </head>
  <body>
    <v-app id="app">
      <v-content class="mx-3 mt-3">
        <v-container id="model-container" fluid>
          <v-row>
            <v-col>
              <h1 class="ml-6 font-weight-regular display-2">Model</h1>
              <p class="mt-4 ml-1">Our models trained in python 3.x using Keras 2.2.4-tf with TensorFlow 1.15.0 and Scikit-learn 0.21.3. below is the detail of each model.</p>
              <v-card class="mt-6" flat tile>
                <v-tabs vertical>
                    <v-tab v-for="(model, i) in models" :key="i">{{ model.aka.toUpperCase() }}</v-tab>
                    <v-tab-item v-for="(model, i) in models" :key="i">
                      <v-card flat class="mt-2">
                        <v-card-text>
                          <div>
                            <p class="display-1">{{ model.name }}</p>
                            <p class="title">- Description</p>
                            <div class="body-2 pl-3 mb-3">
                              {{ model.desc }}
                            </div>
                            <p class="title">- Visualization</p>
                            <div class="body-2 pl-3 mb-3">
                              <v-img 
                                v-for="(view, j) in model.visualizations" :key="j"
                                :src="view"
                                contain max-height="250px"
                              ></v-img>
                            </div>
                          </div>
                        </v-card-text>
                      </v-card>
                    </v-tab-item>
                  </template>
                </v-tabs>
              </v-card>
            </v-col>
          </v-row>
        </v-container>

        <v-divider></v-divider>

        <v-container id="image-container" fluid>
          <v-row class="mt-3">
            <v-col cols="12">
              <h1 class="ml-6 font-weight-regular display-2">History</h1>
              <p class="mt-4 ml-1">Submitted and processed images are below!</p>
            </v-col>
          </v-row>
          <v-row>
            <v-col
              v-for="card in cards"
              :key="card.id"
              cols="12" sm="6" md="4" lg="3"
            >
              <v-card :id="'history-' + card.id">
                <v-img
                  class="white--text align-end"
                  :src="card.img"
                  gradient="to bottom, rgba(0, 0, 0, .1), rgba(0, 0, 0, .5)"
                  height="200px"
                >
                  <v-card-title>{{ '#' + card.id }}</v-card-title>
                </v-img>
                <v-card-text>
                  <div class="mb-1"><strong>Model : </strong>{{ card.model.toUpperCase() }}</div>
                  <div><strong>Prediction / Label : </strong>{{ nameLabel(card.prediction) }} / {{ nameLabel(card.label) }}</div>
                </v-card-text>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn icon @click="openDialog(card.id)">
                    <v-icon>mdi-file-document</v-icon>
                  </v-btn>
                </v-card-actions>
              </v-card>
            </v-col>
          </v-row>
          <v-row class="mt-4">
            <v-col cols="12" align-self="end">
              <v-btn 
                id="more-btn"
                class="mb-3"
                large outlined text block
                :disabled="last"
                @click="viewMore"
              >{{ last ? 'That was last' : 'View more' }}</v-btn>
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
          context: 'model'
        },
        // model
        tab: 'SVM',
        models: [],
        // history
        labels: [],
        next: '/api/history/',
        last: false,
        cards: [],
      }),
      methods: {
        nameLabel (value) {
          var match = this.labels.find(i => i.value == value)
          if (match)
            return match.display_name
            
          return 'Unknown'
        },
        async viewMore () {
          if (!this.last) {
            var response = await axios.get(this.next)
            this.cards = this.cards.concat(response.data.results)
            this.next = response.data.next
            this.last = (this.next == null)
          }
        }
      },
      async created () {
        var option = await axios.options('/api/history/')
        this.labels = option.data.actions.POST.label.choices

        // load model metadata
        var response = await axios.get('/api/model/')
        this.models = response.data.results

        // load history
        await this.viewMore()
      }
    })
  </script>
</html>
