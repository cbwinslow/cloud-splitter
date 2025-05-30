import { useState, useEffect, useCallback, useRef } from 'react';

type WebSocketMessage = {
  type: string;
  data: any;
  timestamp?: string;
};

interface UseWebSocketOptions {
  reconnectAttempts?: number;
  reconnectInterval?: number;
  onMessage?: (message: WebSocketMessage) => void;
  onConnect?: () => void;
  onDisconnect?: () => void;
  onError?: (error: Event) => void;
}

const DEFAULT_OPTIONS: UseWebSocketOptions = {
  reconnectAttempts: 5,
  reconnectInterval: 3000,
};

export const useWebSocket = (url: string, options: UseWebSocketOptions = {}) => {
  const [isConnected, setIsConnected] = useState(false);
  const [error, setError] = useState<Event | null>(null);
  const wsRef = useRef<WebSocket | null>(null);
  const reconnectAttemptsRef = useRef(0);
  const reconnectTimeoutRef = useRef<NodeJS.Timeout>();

  const opts = { ...DEFAULT_OPTIONS, ...options };

  const connect = useCallback(() => {
    try {
      const ws = new WebSocket(url);
      wsRef.current = ws;

      ws.onopen = () => {
        setIsConnected(true);
        setError(null);
        reconnectAttemptsRef.current = 0;
        opts.onConnect?.();
      };

      ws.onclose = () => {
        setIsConnected(false);
        opts.onDisconnect?.();

        // Attempt to reconnect
        if (reconnectAttemptsRef.current < (opts.reconnectAttempts || 0)) {
          reconnectTimeoutRef.current = setTimeout(() => {
            reconnectAttemptsRef.current++;
            connect();
          }, opts.reconnectInterval);
        }
      };

      ws.onerror = (event) => {
        setError(event);
        opts.onError?.(event);
      };

      ws.onmessage = (event) => {
        try {
          const message: WebSocketMessage = JSON.parse(event.data);
          opts.onMessage?.(message);
        } catch (err) {
          console.error('Failed to parse WebSocket message:', err);
        }
      };
    } catch (err) {
      console.error('Failed to create WebSocket connection:', err);
      setError(err as Event);
    }
  }, [url, opts]);

  const disconnect = useCallback(() => {
    if (wsRef.current) {
      wsRef.current.close();
      wsRef.current = null;
    }
    if (reconnectTimeoutRef.current) {
      clearTimeout(reconnectTimeoutRef.current);
    }
    setIsConnected(false);
  }, []);

  const sendMessage = useCallback((message: WebSocketMessage) => {
    if (wsRef.current && isConnected) {
      try {
        wsRef.current.send(JSON.stringify({
          ...message,
          timestamp: new Date().toISOString(),
        }));
      } catch (err) {
        console.error('Failed to send WebSocket message:', err);
      }
    }
  }, [isConnected]);

  useEffect(() => {
    connect();
    return () => {
      disconnect();
    };
  }, [connect, disconnect]);

  return {
    isConnected,
    error,
    sendMessage,
    disconnect,
    reconnect: connect,
  };
};

export type { WebSocketMessage, UseWebSocketOptions };

