# Use Node.js as the base image
FROM node:18

# Set the working directory in the container
WORKDIR /src

# Copy package.json and package-lock.json to the container
COPY package.json package-lock.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Expose the default development server port
EXPOSE 3000

# Start the React app
CMD ["npm", "start"]
