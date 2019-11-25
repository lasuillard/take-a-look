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
                  <v-tab>SVM</v-tab>
                  <v-tab-item>
                    <v-card flat class="mt-2">
                      <v-card-text>
                        <div>
                          <p class="display-1">Support Vector Machine</p>
                          <p class="title">- Description</p>
                          <div class="body-2 pl-3 mb-3">
                            &nbsp;Classification model trained by sklearn.svm.SVC, take input as features extracted by VGG19 pre-trained layers.<br/>
                            its accuracy took about 83% in test.
                          </div>

                          <p class="title">- Visualization</p>
                          <div class="body-2 pl-3 mb-3">
                            -
                          </div>
                        </div>
                      </v-card-text>
                    </v-card>
                  </v-tab-item>
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
              <v-card>
                <v-img
                  class="white--text align-end"
                  :src="card.src"
                  gradient="to bottom, rgba(0, 0, 0, .1), rgba(0, 0, 0, .5)"
                  height="200px"
                >
                  <v-card-title>{{ '#' + card.id }}</v-card-title>
                </v-img>
                <v-card-text>
                  <div class="mb-1"><strong>Model : </strong>{{ card.model }}</div>
                  <div><strong>Prediction / Label : </strong>{{ card.prediction }} / {{ card.label }}</div>
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
        <v-dialog v-model="dialog.open" scrollable max-width="600px">
          <v-card id="history-dialog">
            <v-card-title class="headline">{{ 'History for #' + dialog.id }}</v-card-title>
            <v-card-text>
              Blahblah
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn id="close-dialog" color="red lighten-1" text @click="dialog.open = false">Close</v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
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
        models: [
          { name: 'SVM', text: 'Support Vector Machine' },
          { name: 'CNN', text: 'ConvNet' },
          { name: 'Decision Tree', text: 'Decision Tree Model'}
        ],
        // history
        last: false,
        cards: [
          { id: 1, src: 'https://cdn.vuetifyjs.com/images/cards/house.jpg', model: 'svm', prediction: 'cat', label: 'dog' },
          { id: 2, src: 'https://cdn.vuetifyjs.com/images/cards/road.jpg', model: 'cnn', prediction: 'dog', label: 'dog' },
        ],
        // dialogs
        dialog: {
          open: false,
          id: null,
        },
      }),
      methods: {
        openDialog (id) {
          this.dialog.id = id
          //
          // do ajax thing
          //
          this.dialog.open = true
        },
        viewMore () {
          if (!this.last) {
            this.cards.push({ id: 3, src: 'https://cdn.vuetifyjs.com/images/cards/plane.jpg', model: 'decision tree', prediction: 'cat', label: 'cat' })
            this.last = true
          }
        }
      }
    })
  </script>
</html>
