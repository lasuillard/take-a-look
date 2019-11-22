<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
  <head>
    <%@ include file="/WEB-INF/jsp/static.jsp" %>
    <%@ include file="/WEB-INF/jsp/meta.jsp" %>
    <title>Take a Look &mdash; History</title>
  </head>
  <body>
    <v-app id="app">
      <v-content>

      </v-content>
      <%@ include file="/WEB-INF/jsp/components/bottom-nav-bar.jsp" %>
    </v-app>
  </body>
  <script>
    new Vue({
      el: '#app',
      vuetify: new Vuetify(),
      data: () => ({
        meta: {
          context: 'history'
        },
      }),
    })
  </script>
</html>
