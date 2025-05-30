import { AppProps } from 'next/app';
import Head from 'next/head';
import { ThemeProvider } from '@mui/material/styles';
import { CssBaseline } from '@mui/material';
import { ErrorBoundary } from 'react-error-boundary';
import { theme } from '@/styles/theme';
import { AudioProvider } from '@/contexts/AudioContext';
import { VisualizationProvider } from '@/contexts/VisualizationContext';
import { WebSocketProvider, WebSocketErrorBoundary } from '@/contexts/WebSocketContext';

// Error Fallback component
const ErrorFallback = ({ error, resetErrorBoundary }: {
  error: Error;
  resetErrorBoundary: () => void;
}) => {
  return (
    <div
      style={{
        height: '100vh',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        background: '#000',
        color: '#00ff00',
        fontFamily: '"Share Tech Mono", monospace',
      }}
    >
      <h1>Something went wrong</h1>
      <pre style={{ margin: '1rem 0', padding: '1rem', background: 'rgba(0,255,0,0.1)' }}>
        {error.message}
      </pre>
      <button
        onClick={resetErrorBoundary}
        style={{
          background: 'transparent',
          border: '1px solid #00ff00',
          color: '#00ff00',
          padding: '0.5rem 1rem',
          cursor: 'pointer',
          fontFamily: 'inherit',
          '&:hover': {
            background: 'rgba(0,255,0,0.1)',
          },
        }}
      >
        Try again
      </button>
    </div>
  );
};

const MyApp = ({ Component, pageProps }: AppProps) => {
  return (
    <>
      <Head>
        <meta name="viewport" content="initial-scale=1, width=device-width" />
        <meta name="theme-color" content="#000000" />
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link
          href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap"
          rel="stylesheet"
        />
      </Head>

      <ErrorBoundary
        FallbackComponent={ErrorFallback}
        onReset={() => {
          // Reset application state here
          window.location.reload();
        }}
      >
        <ThemeProvider theme={theme}>
          <CssBaseline />
          <WebSocketErrorBoundary
            fallback={
              <div
                style={{
                  padding: '1rem',
                  background: 'rgba(255,0,0,0.1)',
                  color: '#00ff00',
                  textAlign: 'center',
                  fontFamily: '"Share Tech Mono", monospace',
                }}
              >
                WebSocket connection failed. Please check your connection and refresh the page.
              </div>
            }
          >
            <WebSocketProvider>
              <AudioProvider>
                <VisualizationProvider>
                  <Component {...pageProps} />
                </VisualizationProvider>
              </AudioProvider>
            </WebSocketProvider>
          </WebSocketErrorBoundary>
        </ThemeProvider>
      </ErrorBoundary>

      <style jsx global>{`
        :root {
          --matrix-primary: #00ff00;
          --matrix-background: #000000;
        }

        * {
          box-sizing: border-box;
          margin: 0;
          padding: 0;
        }

        html,
        body {
          padding: 0;
          margin: 0;
          font-family: 'Share Tech Mono', monospace;
          background: var(--matrix-background);
          color: var(--matrix-primary);
          overflow-x: hidden;
        }

        body {
          position: relative;
        }

        body::before {
          content: '';
          position: fixed;
          top: 0;
          left: 0;
          width: 100%;
          height: 100%;
          pointer-events: none;
          background: linear-gradient(
            0deg,
            rgba(0, 255, 0, 0.03) 0%,
            rgba(0, 0, 0, 0) 100%
          );
          z-index: 1;
        }

        /* Scrollbar styling */
        ::-webkit-scrollbar {
          width: 8px;
          height: 8px;
        }

        ::-webkit-scrollbar-track {
          background: var(--matrix-background);
        }

        ::-webkit-scrollbar-thumb {
          background: var(--matrix-primary);
          border-radius: 4px;
        }

        ::-webkit-scrollbar-thumb:hover {
          background: rgba(0, 255, 0, 0.8);
        }

        /* Selection styling */
        ::selection {
          background: rgba(0, 255, 0, 0.2);
          color: var(--matrix-primary);
        }

        /* Focus outline */
        :focus {
          outline: 2px solid var(--matrix-primary);
          outline-offset: 2px;
        }

        /* Animation keyframes */
        @keyframes glow {
          0% { text-shadow: 0 0 5px rgba(0, 255, 0, 0.5); }
          50% { text-shadow: 0 0 20px rgba(0, 255, 0, 0.8); }
          100% { text-shadow: 0 0 5px rgba(0, 255, 0, 0.5); }
        }

        @keyframes pulse {
          0% { opacity: 1; }
          50% { opacity: 0.5; }
          100% { opacity: 1; }
        }
      `}</style>
    </>
  );
};

export default MyApp;

