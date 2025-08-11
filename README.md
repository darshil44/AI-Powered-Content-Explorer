
# Rapid Innovation | AI-Powered Content & Image Explorer

A full-stack AI-powered content exploration platform enabling users to perform real-time web searches, generate AI images from text prompts, save and manage their content history, and securely access personalized dashboards. Built with modern technologies to ensure scalability, security, and excellent user experience.

----------

## Table of Contents

-   [Project Overview](#project-overview)
    
-   [Key Features](#key-features)
    
-   [Tech Stack](#tech-stack)
    
-   [Architecture & Design](#architecture--design)
    
-   [Setup & Installation](#setup--installation)
    
    -   [Backend Setup](#backend-setup)
        
    -   [Frontend Setup](#frontend-setup)
        
-   [Running the Application](#running-the-application)
    
-   [Testing](#testing)
    
-   [Folder Structure](#folder-structure)
    
-   [API Endpoints](#api-endpoints)
    
-   [Contributing](#contributing)
    

----------

## Project Overview

AI Content Explorer is designed to empower authenticated users with AI-driven capabilities to:

-   Search the internet with AI-enhanced real-time web searches via Tavily MCP server
    
-   Generate creative images based on textual prompts using Flux ImageGen MCP server
    
-   Persist and manage their search and image generation history with powerful filtering and editing tools
    
-   Authenticate and authorize users securely using JWT and role-based access control
    

----------

## Key Features

-   **User Authentication**: Secure registration and login with password hashing using Argon2, JWT stored in HTTP-only cookies
    
-   **AI-Powered Search**: Real-time web searches integrated with Tavily MCP
    
-   **AI Image Generation**: Generate and save images from text prompts via Flux ImageGen MCP
    
-   **Dashboard**: Full CRUD capabilities on saved entries with filtering, inline editing, and deletion
    
-   **Modern UI/UX**: Responsive React frontend styled with Tailwind CSS, enhanced by toast notifications for seamless feedback
    
-   **Comprehensive Testing**: Unit and integration tests on backend, planned E2E testing for frontend-to-backend flows
    

----------

## Tech Stack


| Layer            | Technology                                                    |
| ---------------- | ------------------------------------------------------------- |
| Frontend         | React, Tailwind CSS, React Router, React Toastify             |
| Backend          | Python, FastAPI, Pydantic, JWT, Argon2                        |
| Database         | PostgreSQL                                                    |
| Cache & Sessions | Redis                                                         |
| AI Integration   | MCP protocol servers (Tavily MCP, Flux ImageGen MCP)          |
| Testing          | Pytest (backend), React Testing Library, Playwright (planned) |
| Deployment       | Uvicorn, PostgreSQL, Redis (local or cloud)                   |


----------

## Architecture & Design

The application follows a modular layered architecture:

-   **Backend**: FastAPI serves RESTful APIs organized in routers by domain:  `/auth`,  `/search`,  `/image`,  `/dashboard`. Authentication uses JWT with HTTP-only cookies. Redis is used for caching and session management to optimize performance.
    
-   **Frontend**: React SPA with route protection via context/provider pattern. Tailwind CSS for utility-first styling ensures responsive, modern design. API interaction uses Axios with centralized instance managing auth headers.
    
-   **Data Flow**: Frontend securely calls backend APIs which proxy requests to MCP servers for search/image generation. Results and user data are persisted in PostgreSQL.
    
-   **Security**: Passwords hashed with Argon2, JWT tokens with short expiry and refresh mechanism, HTTP-only cookies prevent XSS, role-based access restricts sensitive operations.
    

----------

## Setup & Installation

### Backend Setup

1.  **Prerequisites**
    
    -   Python 3.10+
        
    -   PostgreSQL (running locally or remote)
        
    -   Redis server running locally or remote
        
2.  **Clone the repo**
    
    ```bash
    git clone https://github.com/darshil44/AI-Powered-Content-Explorer.git
    cd backend
    
    ```
    
3.  **Create and activate virtual environment**
    
    ```bash
    python -m venv venv
    source venv/bin/activate   # macOS/Linux
    venv\Scripts\activate      # Windows
    
    ```
    
4.  **Install dependencies**
    
    ```bash
    pip install -r requirements.txt
    
    ```
    
5.  **Configure environment variables**  
    Copy  `.env.example`  to  `.env`  and fill in all required values including database URL, MCP API keys, Redis URL, JWT secrets.
    
6.  **Database Setup**
    
    -   Create the PostgreSQL database manually or via tools like  `psql`  or pgAdmin.
        
    -   Run migrations (if applicable).
        
7.  **Run FastAPI server**
    
    ```bash
    uvicorn app.main:app --reload
    
    ```
    
    Access API docs at  `http://localhost:8000/docs`
    

----------

### Frontend Setup

1.  **Navigate to frontend folder**
    
    ```bash
    cd ../frontend
    
    ```
    
2.  **Install Node.js dependencies**
    
    ```bash
    npm install
    
    ```
    
3.  **Configure environment variables**  
    Create  `.env.local`  and set API base URL (e.g.,  `VITE_API_BASE_URL=http://localhost:8000`)
    
4.  **Run React development server**
    
    ```bash
    npm run dev
    
    ```
    
    Open  `http://localhost:3000`  in your browser.
    

----------

## Running the Application

1.  Start backend server (FastAPI with Uvicorn)
    
2.  Start frontend React app
    
3.  Visit frontend URL, register a user, login, and explore features: search, image generation, save and manage your content.
    

----------

## Testing

-   **Backend**  
    Run all tests with pytest inside backend folder:
    
    ```bash
    pytest tests/
    
    ```
    
-   **Frontend**  
    Run React unit tests (if added):
    
    ```bash
    npm test
    
    ```

----------

## Folder Structure

### Backend

```
backend/
│
├── app/
│   ├── api/
│   │   ├── api_v1/
│   │   │   ├── routers/
│   │   │   │   ├── auth.py
│   │   │   │   ├── search.py
│   │   │   │   ├── image.py
│   │   │   │   └── dashboard.py
│   │   │   └── api.py
│   │   └── deps.py
│   ├── core/
│   ├── db/
│   ├── models/
│   ├── schemas/
│   ├── tests/
│   ├── main.py
│   └── ...
├── requirements.txt
├── .env
└── ...

```

### Frontend

```
frontend/
│
├── public/
├── src/
│   ├── api/
│   │   └── axios.js
│   ├── components/
│   ├── context/
│   │   └── AuthContext.jsx
│   ├── pages/
│   │   ├── Login.jsx
│   │   ├── Register.jsx
│   │   ├── Search.jsx
│   │   ├── ImageGen.jsx
│   │   ├── Dashboard.jsx
│   ├── App.jsx
│   ├── main.jsx
│   └── index.css
├── package.json
├── tailwind.config.js
└── ...

```

----------

## API Endpoints Overview


| Route             | Method | Description                        |
| ----------------- | ------ | ---------------------------------- |
| `/auth/register`  | POST   | Register a new user                |
| `/auth/login`     | POST   | User login, returns JWT cookie     |
| `/auth/refresh`   | POST   | Refresh access token               |
| `/search`         | POST   | Query Tavily MCP for web search    |
| `/image`          | POST   | Generate image via Flux MCP        |
| `/dashboard`      | GET    | Get saved search and image entries |
| `/dashboard`      | POST   | Save a new entry                   |
| `/dashboard/{id}` | PUT    | Update a saved entry               |
| `/dashboard/{id}` | DELETE | Delete a saved entry               |


----------

## Contributing

Contributions are welcome. Please fork the repo and open pull requests with clear descriptions and test coverage. For major changes, open an issue first to discuss your plans.

----------
