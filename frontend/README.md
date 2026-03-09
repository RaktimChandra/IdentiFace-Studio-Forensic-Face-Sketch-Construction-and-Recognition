# IdentiFace Studio - Frontend

Modern React + TypeScript frontend for forensic face sketch construction and recognition.

## Tech Stack

- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool
- **TailwindCSS** - Styling
- **React Router** - Routing
- **TanStack Query** - Data fetching
- **Zustand** - State management
- **Fabric.js** - Canvas manipulation
- **Axios** - HTTP client

## Getting Started

### Install Dependencies

```bash
npm install
```

### Development Server

```bash
npm run dev
```

App runs on: http://localhost:5173

### Build for Production

```bash
npm run build
```

### Preview Production Build

```bash
npm run preview
```

## Project Structure

```
src/
├── components/       # Reusable components
├── pages/           # Page components
├── stores/          # Zustand stores
├── services/        # API services
├── hooks/           # Custom hooks
├── utils/           # Utility functions
├── types/           # TypeScript types
└── assets/          # Static assets
```

## Features

- **Sketch Builder** - Drag-and-drop face composition
- **Suspect Database** - Manage suspects with photos
- **Case Management** - Track investigation cases
- **Face Recognition** - AI-powered matching
- **Real-time Updates** - Live data synchronization
- **Responsive Design** - Works on all devices

## Environment Variables

Create `.env` file:

```env
VITE_API_URL=http://localhost:8000
```

## Code Style

- ESLint for linting
- Prettier for formatting
- TypeScript strict mode enabled

## Testing

```bash
npm run test
```

## License

MIT License
