# Use a Node.js image as the base
FROM node:22-alpine

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json (if using npm)
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Build the Next.js application for production (optional, for dev `npm run dev` is used)
# RUN npm run build

# Expose the port Next.js runs on
EXPOSE 3000

# Command to run the application (defined in docker-compose.yml)
# CMD ["npm", "run", "dev"]