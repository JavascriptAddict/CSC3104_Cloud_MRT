# Stage 1: Build the React frontend
FROM node:18 AS build

WORKDIR /app

# Copy package.json and package-lock.json for dependency installation
COPY package.json package-lock.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application files
COPY . .

# Build the React app
RUN npm run build

# Stage 2: Set up Express to serve the frontend and model files
FROM node:18-alpine

WORKDIR /app

# Copy package.json and package-lock.json to install server dependencies
COPY package.json package-lock.json ./

# Install only production dependencies (including express)
RUN npm install --only=production

# Copy the built frontend from the previous stage
COPY --from=build /app/build /app/build

# Copy the Express server setup file
COPY server.js .

# Expose port 80
EXPOSE 80

# Start the Express server
CMD ["node", "server.js"]
