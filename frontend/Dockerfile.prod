#Base image
FROM node:lts-alpine as build-stage

# Set the working directory
WORKDIR /app

# Copy the package.json
COPY ./app/package.json /app/package.json

# install project dependencies
RUN npm install

# copy the rest of the project files to the container
COPY ./app/ .

# build the Vue.js application to the production mode to dist folder
RUN npm run build

FROM nginx:stable-alpine as production-stage

# Copy the build applicationi from the previous state to the Nginx container
COPY --from=build-stage /app/dist /usr/share/nginx/html

# Copy the nginx configuration file
COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf

# Expose a port
EXPOSE 80

# Executables
CMD [ "nginx", "-g", "daemon off;" ]
