# Cloud Splitter Web Frontend

A modern web application for audio processing and visualization, featuring real-time spectrum analysis and matrix-style visual effects.

[![TypeScript](https://img.shields.io/badge/TypeScript-4.7.4-blue.svg)](https://www.typescriptlang.org/)
[![Next.js](https://img.shields.io/badge/Next.js-12.2.0-black.svg)](https://nextjs.org/)
[![Material-UI](https://img.shields.io/badge/MUI-5.8.7-blue.svg)](https://mui.com/)
[![WebAudio API](https://img.shields.io/badge/WebAudio-API-green.svg)](https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API)

## Features

- 🎵 Real-time audio processing and visualization
- 📊 10-band spectrum analyzer with Matrix theme
- 🌟 Music-reactive background effects
- 💾 Audio stem separation and processing
- 🔄 Real-time WebSocket updates
- 📱 Responsive design for all devices
- 🎨 Matrix-inspired visual theme

## Prerequisites

- Node.js 16.x or higher
- npm 8.x or higher
- Modern web browser with WebAudio API support

## Quick Start

1. Clone the repository:
   ```bash
   git clone https://github.com/cbwinslow/cloud-splitter.git
   cd cloud-splitter/web/frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Set up environment:
   ```bash
   npm run setup-env
   ```

4. Start development server:
   ```bash
   npm run dev
   ```

Visit `http://localhost:3000` to see the application.

## Project Structure

```
frontend/
├── components/     # React components
├── contexts/      # React context providers
├── hooks/         # Custom React hooks
├── pages/         # Next.js pages
├── public/        # Static assets
├── scripts/       # Build and setup scripts
├── services/      # Core services
├── styles/        # Global styles and theme
├── types/         # TypeScript type definitions
└── utils/         # Utility functions
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build production application
- `npm run start` - Start production server
- `npm run lint` - Run ESLint
- `npm run type-check` - Run TypeScript checks
- `npm run setup-env` - Set up environment files
- `npm test` - Run tests
- `npm run format` - Format code with Prettier

## Development

### Environment Setup

The application uses multiple environment configurations:

1. `.env.development` - Development settings
2. `.env.production` - Production settings
3. `.env.local` - Local overrides (not committed)

Run `npm run setup-env` to create these files.

### Core Technologies

- **Next.js** - React framework
- **TypeScript** - Type safety
- **Material-UI** - UI components
- **Web Audio API** - Audio processing
- **WebSocket** - Real-time updates

### Development Mode

```bash
# Start development server
npm run dev

# Run with type checking
npm run dev:type-check

# Run with debugging
DEBUG=true npm run dev
```

## Production Deployment

1. Build the application:
   ```bash
   npm run build
   ```

2. Start the production server:
   ```bash
   npm run start
   ```

### Docker Deployment

```bash
# Build Docker image
docker build -t cloud-splitter-frontend .

# Run container
docker run -p 3000:3000 cloud-splitter-frontend
```

## Architecture

### Core Services

1. **AudioService**
   - Audio file processing
   - Stem separation
   - Metadata extraction

2. **VisualizationService**
   - Spectrum analysis
   - Matrix rain effect
   - Background animations

3. **WebSocketService**
   - Real-time updates
   - Connection management
   - Event handling

### Context Providers

1. **AudioContext**
   - Audio state management
   - Processing control
   - File handling

2. **VisualizationContext**
   - Animation state
   - Canvas management
   - Effect configuration

3. **WebSocketContext**
   - Connection state
   - Message handling
   - Real-time updates

## Configuration

### Development Configuration
- Located in `dev.config.js`
- Includes hot reloading
- Source maps enabled
- Proxy settings for API

### Production Configuration
- Located in `prod.config.js`
- Optimized builds
- Compression enabled
- Security headers

## Performance Optimization

- Code splitting
- Image optimization
- Lazy loading
- Caching strategies
- Compression

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and lint checks
5. Submit a pull request

## Troubleshooting

### Common Issues

1. **WebSocket Connection Failed**
   - Check backend server status
   - Verify WebSocket URL
   - Check network connectivity

2. **Audio Processing Errors**
   - Verify file format
   - Check file size limits
   - Ensure backend services are running

3. **Visualization Issues**
   - Check WebAudio API support
   - Verify canvas context
   - Check browser compatibility

### Debug Mode

Enable debug logging:
```bash
DEBUG=true npm run dev
```

## License

MIT License - see LICENSE file for details

## Support

- GitHub Issues: [Report Bug](https://github.com/cbwinslow/cloud-splitter/issues)
- Documentation: [Wiki](https://github.com/cbwinslow/cloud-splitter/wiki)
- Discord: [Join Community](https://discord.gg/cloud-splitter)

## Credits

- Matrix theme inspiration
- Open source audio processing libraries
- Community contributors

