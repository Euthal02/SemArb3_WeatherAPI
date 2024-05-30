#Base image
FROM node:lts-alpine3.17

# Set the working directory
WORKDIR /app

# Copy the package.json
COPY ./app/package.json /app/package.json

# install project dependencies
RUN npm install

# Expose a port
EXPOSE 3000
EXPOSE 5173

# Executables
CMD [ "npm", "run", "dev", "--host=0.0.0.0" ]
