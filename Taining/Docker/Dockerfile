# Use official Node.js image from Docker Hub
FROM node:18

# Set working directory inside container
WORKDIR /usr/src/app/ravi

# Copy package.json and install dependencies
COPY package*.json ./
RUN npm install

# Copy app code into container
COPY . .

# Expose port 3000
EXPOSE 3000

# Run the app
CMD ["npm", "start"]
