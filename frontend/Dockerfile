FROM node:20-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies and rebuild esbuild
RUN npm install
RUN npm rebuild esbuild

# Copy the rest of the application
COPY . .

# Expose the port
EXPOSE 5173

# Start the development server
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]