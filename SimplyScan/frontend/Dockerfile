# Use Node.js to build the frontend
FROM node:18 AS build

WORKDIR /app

# Copy package.json and package-lock.json first to leverage Docker cache
COPY package.json package-lock.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application files
COPY . .

# Build the React app
RUN npm run build

# Use a lightweight Node.js image to serve the app with 'serve'
FROM node:18-alpine

# Install 'serve' globally
RUN npm install -g serve

# Set the working directory
WORKDIR /app

# Copy the build output from the previous stage
COPY --from=build /app/build /app/build

# Expose port 80
EXPOSE 80

# Serve the app in production mode
CMD ["serve", "-s", "build", "-l", "80"]
