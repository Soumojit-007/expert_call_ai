# ==========================================
# Stage 1: Build React application
# ==========================================

FROM node:22-alpine AS builder

WORKDIR /app

# Copy package files first for better layer caching
COPY package*.json ./

RUN npm ci

# Copy frontend source
COPY . .


# Frontend will call the same host using relative API paths
ENV VITE_API_BASE_URL=""

# Build the Vite application
RUN npm run build


# ==========================================
# Stage 2: Serve with Nginx
# ==========================================

FROM nginx:alpine

# Remove default Nginx files
RUN rm -rf /usr/share/nginx/html/*

# Copy React production build
COPY --from=builder /app/dist /usr/share/nginx/html

# Expose HTTP port
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]