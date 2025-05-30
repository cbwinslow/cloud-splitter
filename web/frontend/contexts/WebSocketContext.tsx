import React, { createContext, useContext, useEffect, useState, useCallback } from 'react';
import { websocketService, type WebSocketMessage, type ConnectionStatus } from '@/services/websocket';

interface WebSocketContextState {
  isConnected: boolean;
  connectionStatus: ConnectionStatus;
  sendMessage: (message: WebSocketMessage) => void;
  connect: () => void;
  disconnect: () => void;
  error: Error | null;
}

const WebSocketContext = createContext<WebSocketContextState | null>(null);

interface WebSocketProviderProps {
  children: React.ReactNode;
  autoConnect?: boolean;
}

export const WebSocketProvider: React.FC<WebSocketProviderProps> = ({
  children,
  autoConnect = true,
}) => {
  const [isConnected, setIsConnected] = useState(false);
  const [connectionStatus, setConnectionStatus] = useState<ConnectionStatus>({
    connected: false,
    reconnecting: false,
    attempt: 0,
  });
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    const handleConnectionStatus = (status: ConnectionStatus) => {
      setIsConnected(status.connected);
      setConnectionStatus(status);
    };

    const handleError = (err: Error) => {
      setError(err);
    };

    websocketService.on('connection-status', handleConnectionStatus);
    websocketService.on('error', handleError);

    if (autoConnect) {
      websocketService.connect();
    }

    return () => {
      websocketService.off('connection-status', handleConnectionStatus);
      websocketService.off('error', handleError);
      websocketService.disconnect();
    };
  }, [autoConnect]);

  const connect = useCallback(() => {
    setError(null);
    websocketService.connect();
  }, []);

  const disconnect = useCallback(() => {
    websocketService.disconnect();
  }, []);

  const sendMessage = useCallback((message: WebSocketMessage) => {
    try {
      websocketService.send(message);
    } catch (err) {
      setError(err as Error);
    }
  }, []);

  const value = {
    isConnected,
    connectionStatus,
    sendMessage,
    connect,
    disconnect,
    error,
  };

  return <WebSocketContext.Provider value={value}>{children}</WebSocketContext.Provider>;
};

export const useWebSocket = () => {
  const context = useContext(WebSocketContext);
  if (!context) {
    throw new Error('useWebSocket must be used within a WebSocketProvider');
  }
  return context;
};

interface WebSocketErrorBoundaryProps {
  children: React.ReactNode;
  fallback?: React.ReactNode;
}

export class WebSocketErrorBoundary extends React.Component<
  WebSocketErrorBoundaryProps,
  { hasError: boolean }
> {
  constructor(props: WebSocketErrorBoundaryProps) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error('WebSocket Error:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback || <div>Error connecting to WebSocket server</div>;
    }

    return this.props.children;
  }
}

