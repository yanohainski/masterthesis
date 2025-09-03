---
description: New prompt created from chat session
mode: ask
model: Claude Sonnet 4
---
<user>
Please go thru the code inside this project and describe what it does. I want a detailed explanation to understand the codebase and which part does what for the product. 
Please also explain how the backend is structured regarding the structure of docker containers and docker compose 

</user>
<assistant>
# Notisent Project Overview

Based on the codebase analysis, **Notisent** is an AI-powered productivity platform designed to reduce information overload and streamline workflows through intelligent email management and prioritization. The project consists of two main components: a Django backend and a React-based Microsoft Outlook add-in.

## Project Architecture

### High-Level Structure
The project is split into two main directories:
- **bknd** - Backend services and API
- **ftnd** - Frontend Outlook add-in

## Backend Architecture (backend)

### Core Technology Stack
- **Framework**: Django with Django REST Framework
- **Database**: PostgreSQL 16 with ParadeDB extensions for enhanced search
- **Task Queue**: Celery with Redis as message broker
- **API Server**: Uvicorn (ASGI server)
- **Containerization**: Docker with multi-service orchestration

### Key Backend Components

#### 1. **Core Django Apps**

**Authentication & User Management** (`accounts/`)
- User authentication and authorization
- JWT token management via `internal_jwt.py`
- Multi-tenancy support through `tenancy.py`
- Custom middleware for request processing

**Email Management** (`mail/`)
- AI-powered priority evaluation (`ai_prio/`)
- Intelligent reply suggestions (`ai_reply/`)
- AI writing assistance (`ai_writing/`)
- Email processing via Django Mailbox integration

**Contact Management** (`contacts/`)
- Professional contact database
- Relationship tracking and insights
- Integration with Microsoft Graph API

**Microsoft Integration** (`microsoft/`)
- Microsoft Graph API client (`graph_client.py`)
- OAuth authentication flow
- Webhook handling for real-time updates
- Email synchronization and calendar integration

**Search System** (`search/`)
- Hybrid search combining BM25 full-text and vector similarity
- Configurable search sources and field weights
- Automatic source discovery and registration
- Support for multiple data models

#### 2. **AI Agent System** (`agent/`)

**LLM Integration** (`agent/llm/`)
- Language model integration for various AI tasks
- Priority evaluation using contextual factors
- Natural language rule processing

**Chat Functionality** (`agent/chat/`)
- AI assistant for email and productivity tasks
- Context-aware conversation management

**AI Tools** (`agent/tools/`)
- Specialized tools for email processing and analysis

#### 3. **Advanced Features**

**Priority Evaluation Service**
Based on the priority evaluation documentation, this service:
- Evaluates email priority using contextual factors
- Implements a sophisticated flow: `Email Input → Factor Selection → Context Determination → Context Gathering → Factor Evaluation → Classification`
- Uses Time Management Matrix for classification
- Integrates with multiple data sources for context

**Natural Language Rule Management**
According to the NLRMS documentation:
- Extracts user preference rules from feedback
- Applies learned rules to future email prioritization
- Provides conflict resolution for competing rules
- Integrates with the search system for rule discovery

## Docker Container Architecture

### Development Environment (`docker-compose.dev.yml`)

The backend runs as a multi-container setup:

#### Core Application Services
- **`backend`**: Main Django application
  - Image: `ghcr.io/notisent/backend:main`
  - Handles API requests and business logic
  - Exposed via nginx reverse proxy

- **`celery_worker`**: Background task processing
  - Handles asynchronous operations (email processing, AI tasks)
  - Same image as backend but different command

- **`celery_beat`**: Scheduled task management
  - Manages periodic tasks and cron jobs

#### Data Services
- **`pg_search`**: PostgreSQL database with ParadeDB
  - Enhanced with full-text search capabilities
  - Port 5433 exposed for external access

- **`redis`**: Message broker and cache
  - Used by Celery for task queuing
  - Session storage and caching

#### Infrastructure Services
- **`nginx-proxy`**: Reverse proxy with SSL termination
  - Handles domain routing and HTTPS certificates
  - Uses Let's Encrypt for automatic SSL

- **`pgadmin`**: Database administration interface
  - Web-based PostgreSQL management

- **`infinity_vectorizer`**: Vector embedding service
  - Provides text vectorization for semantic search
  - Uses BGE and MXBai models

#### Additional Services
- **`outlook-addin`**: Frontend Outlook add-in
- **`payload`**: CMS/website backend
- **`mongo`**: MongoDB for CMS data
- **`voice-stt`**: Speech-to-text service

### Network Architecture
- **`proxy_net`**: External network for public-facing services
- **`backend_net`**: Internal network for backend services
- **`website_internal`**: Isolated network for CMS components

## Frontend: Outlook Add-in (notisent-outlook-react)

### Technology Stack
- **Framework**: React with TypeScript
- **Build Tool**: Webpack
- **Authentication**: Microsoft Graph OAuth
- **Deployment**: Nginx in Docker container

### Key Components

**Core Application** (`src/taskpane/components/`)
- **`App.tsx`**: Main application router
- **`Priority.tsx`**: Email priority display and feedback
- **`TabBar.tsx`**: Navigation interface

**Authentication System** (`src/taskpane/contexts/`)
- **`MSAuth.tsx`**: Microsoft authentication state management
- **`useAuth.ts`**: Authentication hook wrapper

**Feature Modules**
- **Chat Assistant** (`components/chat/`): AI-powered email assistance
- **Related Content** (`components/related/`): Related email discovery
- **Settings** (`components/settings/`): User preferences and profile management

## Key Product Features

### 1. **Intelligent Email Prioritization**
- AI analyzes emails using contextual factors (sender relationship, deadline urgency, project relevance)
- Machine learning-based classification using Time Management Matrix
- User feedback integration for continuous improvement

### 2. **Smart Search & Discovery**
- Hybrid search combining keyword and semantic similarity
- Cross-reference emails with contacts, companies, and user goals
- Context-aware content recommendations

### 3. **AI Assistant Integration**
- Chat-based interface for email management
- Natural language rule creation and management
- Intelligent reply suggestions and writing assistance

### 4. **Microsoft Ecosystem Integration**
- Deep Outlook add-in integration
- Graph API connectivity for calendar and contacts
- Real-time synchronization via webhooks

### 5. **Enterprise Features**
- Multi-tenant architecture
- Comprehensive logging and monitoring
- Security-first design with CSRF, XSS protection
- Scalable containerized deployment

## Development Workflow

### Local Development
The project supports both native Python development and Docker-based development via `docker-compose.local.yml` for easier setup.

### Production Deployment
Uses `docker-compose.dev.yml` with:
- Automated SSL certificate management
- Load balancing and reverse proxy
- Separate networks for security isolation
- Health monitoring and logging

This architecture enables Notisent to provide intelligent, context-aware email management while maintaining enterprise-grade security and scalability.
</assistant>
<user>
can you visualize the structure of this project?
</user>
<assistant>
# Notisent Project Structure Visualization

## 🏗️ Overall Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        NOTISENT PLATFORM                        │
├─────────────────────────────────────────────────────────────────┤
│  Frontend (ftnd/)          │         Backend (bknd/)            │
│  ┌─────────────────────┐    │    ┌─────────────────────────────┐ │
│  │   Outlook Add-in    │◄───┼───►│      Django API Server      │ │
│  │   (React/TypeScript)│    │    │      (REST + WebSocket)     │ │
│  └─────────────────────┘    │    └─────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## 🎯 Frontend Structure (notisent-outlook-react)

```
📱 Outlook Add-in (React App)
├── 🔧 Configuration
│   ├── .env.development/.env.production    # Environment configs
│   ├── manifest.xml/manifest-dev.xml       # Outlook add-in manifests
│   ├── webpack.config.js                   # Build configuration
│   └── Dockerfile                          # Container setup
│
├── 📂 Source Code (src/)
│   ├── 🎮 Commands (commands/)
│   │   └── commands.ts                     # Outlook command handlers
│   │
│   └── 🖼️ Task Pane (taskpane/)
│       ├── 🧩 Components
│       │   ├── App.tsx                     # Main app router
│       │   ├── Priority.tsx                # Email priority display
│       │   ├── TabBar.tsx                  # Navigation tabs
│       │   ├── 💬 chat/
│       │   │   └── AssistantWidget.tsx     # AI chat interface
│       │   ├── 🔗 related/
│       │   │   ├── Related.tsx             # Related content finder
│       │   │   └── EmailDialog.tsx         # Email detail dialogs
│       │   └── ⚙️ settings/
│       │       ├── Settings.tsx            # User preferences
│       │       └── profile/                # Profile management
│       │
│       ├── 🎭 Contexts
│       │   ├── MSAuth.tsx                  # Microsoft auth state
│       │   └── NotificationContext.tsx     # App notifications
│       │
│       ├── 🪝 Hooks
│       │   └── useAuth.ts                  # Authentication logic
│       │
│       └── 🔧 Services
│           └── auth.ts                     # Auth API calls
│
└── 📦 Assets (assets/)
    └── 🎨 Icons, logos, and static files
```

## 🏢 Backend Structure (backend)

```
🏗️ Django Backend
├── 🐳 Docker Configuration
│   ├── docker-compose.dev.yml              # Development orchestration
│   ├── docker-compose.local.yml            # Local development
│   └── Dockerfile                          # Backend container
│
├── 🧠 Core Backend (backend/)
│   ├── 🌐 Django Apps
│   │   ├── 👥 accounts/                    # User management & auth
│   │   │   ├── auth.py                     # Authentication logic
│   │   │   ├── internal_jwt.py             # JWT token handling
│   │   │   ├── tenancy.py                  # Multi-tenant support
│   │   │   └── middleware.py               # Request middleware
│   │   │
│   │   ├── 📧 mail/                        # Email processing
│   │   │   ├── ai_prio/                    # AI priority evaluation
│   │   │   ├── ai_reply/                   # Smart reply suggestions
│   │   │   ├── ai_writing/                 # Writing assistance
│   │   │   └── django_mailbox/             # Email integration
│   │   │
│   │   ├── 👤 contacts/                    # Contact management
│   │   │   ├── models.py                   # Contact data models
│   │   │   ├── services.py                 # Business logic
│   │   │   └── serializers.py              # API serialization
│   │   │
│   │   ├── 🏢 crm/                         # CRM functionality
│   │   │   ├── models.py                   # CRM data models
│   │   │   └── services/                   # CRM business logic
│   │   │
│   │   ├── 🔍 search/                      # Advanced search system
│   │   │   ├── vectorization.py            # Vector embeddings
│   │   │   ├── registry.py                 # Search source registry
│   │   │   └── services.py                 # Search algorithms
│   │   │
│   │   ├── 🤖 agent/                       # AI Agent system
│   │   │   ├── llm/                        # LLM integration
│   │   │   ├── chat/                       # Chat functionality
│   │   │   └── tools/                      # AI tools & utilities
│   │   │
│   │   ├── 🔗 microsoft/                   # Microsoft integration
│   │   │   ├── graph_client.py             # Graph API client
│   │   │   ├── webhook.py                  # Real-time updates
│   │   │   ├── tasks.py                    # Background tasks
│   │   │   └── services/                   # Integration services
│   │   │
│   │   ├── 👨‍💼 usermanagement/             # User profiles
│   │   └── 🎤 voice/                       # Voice processing
│   │
│   └── 🔧 Core Configuration
│       ├── settings.py                     # Django settings
│       ├── urls.py                         # URL routing
│       ├── celery.py                       # Task queue config
│       └── asgi.py                         # ASGI server setup
│
└── 📚 Documentation (docs/)
    ├── microsoft_oauth_authentication.md   # Auth setup guide
    ├── tenant_onboarding_guide.md          # Multi-tenancy guide
    └── llm_agent_search_integration_*.md   # AI integration docs
```

## 🐳 Docker Container Architecture

```
🌐 Production Environment (docker-compose.dev.yml)

┌─────────────────────────────────────────────────────────────────┐
│                      PROXY NETWORK                              │
├─────────────────────────────────────────────────────────────────┤
│  🌍 nginx-proxy          🔒 acme-companion    🔧 nginx-gen      │
│  (Load Balancer)         (SSL Certificates)   (Config Gen)      │
│        │                        │                   │           │
│        ▼                        ▼                   ▼           │
│  ┌─────────────┐        ┌─────────────┐    ┌─────────────┐     │
│  │ api.dev.*   │        │ dev.notisent│    │ addin.dev.* │     │
│  │ (Backend)   │        │ (PgAdmin)   │    │ (Add-in)    │     │
│  └─────────────┘        └─────────────┘    └─────────────┘     │
└─────────────────────────────────────────────────────────────────┘
                               │
┌─────────────────────────────────────────────────────────────────┐
│                     BACKEND NETWORK                             │
├─────────────────────────────────────────────────────────────────┤
│  🐍 Django Backend    📊 Task Processing    💾 Data Layer       │
│  ┌─────────────┐    ┌─────────────────┐    ┌─────────────┐     │
│  │   backend   │    │ celery_worker   │    │ pg_search   │     │
│  │ (API Server)│◄──►│ celery_beat     │◄──►│(PostgreSQL) │     │
│  └─────────────┘    └─────────────────┘    └─────────────┘     │
│         │                    │                     │           │
│         ▼                    ▼                     ▼           │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────────┐     │
│  │🤖 infinity  │    │    redis    │    │    pgadmin      │     │
│  │(Vectorizer) │    │ (Message    │    │ (DB Admin)      │     │
│  │             │    │  Broker)    │    │                 │     │
│  └─────────────┘    └─────────────┘    └─────────────────┘     │
│         │                                        │             │
│         ▼                                        ▼             │
│  ┌─────────────┐                        ┌─────────────┐       │
│  │ voice-stt   │                        │ Voice STT   │       │
│  │ (Speech)    │                        │ Service     │       │
│  └─────────────┘                        └─────────────┘       │
└─────────────────────────────────────────────────────────────────┘
                               │
┌─────────────────────────────────────────────────────────────────┐
│                   WEBSITE INTERNAL NETWORK                      │
├─────────────────────────────────────────────────────────────────┤
│  🌐 Website Services                                            │
│  ┌─────────────┐                        ┌─────────────┐       │
│  │   payload   │◄──────────────────────►│    mongo    │       │
│  │ (CMS/Site)  │                        │ (MongoDB)   │       │
│  └─────────────┘                        └─────────────┘       │
└─────────────────────────────────────────────────────────────────┘
```

## 🔄 Data Flow Architecture

```
📧 Email Processing Pipeline

User's Outlook
      │
      ▼
┌─────────────┐    📡 Graph API    ┌─────────────┐    🧠 AI Analysis
│ Outlook     │◄─────────────────►│ Microsoft   │◄─────────────────┐
│ Add-in      │                   │ Services    │                  │
└─────────────┘                   └─────────────┘                  │
      │                                   │                        │
      ▼                                   ▼                        │
┌─────────────┐    📨 REST API    ┌─────────────┐    🤖 Processing │
│ React UI    │◄─────────────────►│ Django      │◄─────────────────┤
│ Components  │                   │ Backend     │                  │
└─────────────┘                   └─────────────┘                  │
                                          │                        │
                                          ▼                        │
                                  ┌─────────────┐                  │
                                  │ Celery      │                  │
                                  │ Workers     │──────────────────┘
                                  └─────────────┘
                                          │
                                          ▼
                                  ┌─────────────┐
                                  │ PostgreSQL  │
                                  │ + Vector DB │
                                  └─────────────┘
```

## 🎯 Feature Flow Visualization

```
🔍 AI-Powered Email Intelligence

┌─────────────────────────────────────────────────────────────────┐
│                    Email Arrives in Outlook                     │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│              📊 Priority Evaluation Engine                      │
├─────────────────────────────────────────────────────────────────┤
│ Factor Selection → Context Determination → Context Gathering    │
│        ▼                    ▼                    ▼             │
│ ┌─────────────┐   ┌─────────────┐   ┌─────────────┐           │
│ │ Sender      │   │ Content     │   │ User Goals  │           │
│ │ Relationship│   │ Analysis    │   │ & Rules     │           │
│ └─────────────┘   └─────────────┘   └─────────────┘           │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│              🎯 Time Management Matrix Classification           │
├─────────────────────────────────────────────────────────────────┤
│ Urgent & Important │ Important Not Urgent │ Not Important      │
│      (Priority 1)  │     (Priority 2)     │   (Priority 3+)    │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│              💡 Smart Recommendations                          │
├─────────────────────────────────────────────────────────────────┤
│ • Related Emails    • Suggested Replies   • Action Items      │
│ • Contact Info      • Calendar Events     • Writing Help      │
└─────────────────────────────────────────────────────────────────┘
```

This visualization shows how Notisent creates a comprehensive email intelligence platform by combining React-based Outlook integration with a sophisticated Django backend, all orchestrated through Docker containers for scalability and reliability.
</assistant>