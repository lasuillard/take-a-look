FROM tomcat:8.5.47-jdk8-corretto

# move to tomcat dir
WORKDIR /usr/local/tomcat

# remove default tomcat files
RUN rm conf webapps -r

# copy necessary files
COPY . .

# run tomcat server
CMD sh -c "catalina.sh run"
