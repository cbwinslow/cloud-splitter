import EventEmitter from 'events';
import TypedEmitter from 'typed-emitter';

type MessageEvents = {
  'visualization-data': (data: number[]) => void;
  'spectrum-data': (data: number[]) => void;
  'processing-status': (status: ProcessingStatus) => void;
  'connection-status': (status: ConnectionStatus) => void;
  'error': (error: Error) => void;
};

type ProcessingStatus = {
  status: 'idle' | 'uploading' | 'processing' | 'completed' | 'error';
  progress?: number;
  message?: string;
  taskId?: string;
};

type ConnectionStatus = {
  connected: boolean;
  reconnecting: boolean;
  attempt: number;
};

type WebSocketMessage = {
  type: string;
  data: any;
  timestamp?: string;
};

class WebSocketService extends (EventEmitter as new () => TypedEmitter<MessageEvents>) {
  private ws: WebSocket | null = null;
  private reconnectTimer: NodeJS.Timeout | null = null;
  private reconnectAttempt = 0;
  private readonly maxReconnectAttempts: number;
  private readonly reconnectInterval: number;
  private isConnected = false;
  private readonly url: string;

  constructor() {
    super();
    this.url = process.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:8000/api/v1/ws';
    this.maxReconnectAttempts = parseInt(process.env.NEXT_PUBLIC_MAX_RECONNECT_ATTEMPTS || '5', 10);
    this.reconnectInterval = parseInt(process.env.NEXT_PUBLIC_RECONNECT_INTERVAL || '3000', 10);

    // Bind methods
    this.connect = this.connect.bind(this);
    this.disconnect = this.disconnect.bind(this);
    this.reconnect = this.reconnect.bind(this);
    this.handleMessage = this.handleMessage.bind(this);
  }

  public connect(): void {
    try {
      this.ws = new WebSocket(this.url);
      this.setupEventListeners();
    } catch (error) {
      this.handleError(new Error('Failed to create WebSocket connection'));
    }
  }

  public disconnect(): void {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
    if (this.reconnectTimer) {
      clearTimeout(this.reconnectTimer);
      this.reconnectTimer = null;
    }
    this.isConnected = false;
    this.emitConnectionStatus();
  }

  public send(message: WebSocketMessage): void {
    if (!this.ws || this.ws.readyState !== WebSocket.OPEN) {
      this.handleError(new Error('WebSocket is not connected'));
      return;
    }

    try {
      this.ws.send(JSON.stringify({
        ...message,
        timestamp: new Date().toISOString(),
      }));
    } catch (error) {
      this.handleError(new Error('Failed to send message'));
    }
  }

  private setupEventListeners(): void {
    if (!this.ws) return;

    this.ws.onopen = () => {
      this.isConnected = true;
      this.reconnectAttempt = 0;
      this.emitConnectionStatus();
    };

    this.ws.onclose = () => {
      this.isConnected = false;
      this.emitConnectionStatus();
      this.reconnect();
    };

    this.ws.onerror = (event) => {
      this.handleError(new Error('WebSocket error occurred'));
    };

    this.ws.onmessage = (event) => {
      try {
        const message: WebSocketMessage = JSON.parse(event.data);
        this.handleMessage(message);
      } catch (error) {
        this.handleError(new Error('Failed to parse WebSocket message'));
      }
    };
  }

  private handleMessage(message: WebSocketMessage): void {
    try {
      switch (message.type) {
        case 'visualization_data':
          this.emit('visualization-data', message.data);
          break;
        case 'spectrum_data':
          this.emit('spectrum-data', message.data);
          break;
        case 'processing_status':
          this.emit('processing-status', {
            status: message.data.status,
            progress: message.data.progress,
            message: message.data.message,
            taskId: message.data.task_id,
          });
          break;
        default:
          console.warn(`Unknown message type: ${message.type}`);
      }
    } catch (error) {
      this.handleError(new Error('Failed to handle WebSocket message'));
    }
  }

  private reconnect(): void {
    if (this.reconnectAttempt >= this.maxReconnectAttempts) {
      this.handleError(new Error('Maximum reconnection attempts reached'));
      return;
    }

    if (this.reconnectTimer) {
      clearTimeout(this.reconnectTimer);
    }

    this.reconnectTimer = setTimeout(() => {
      this.reconnectAttempt++;
      this.emitConnectionStatus();
      this.connect();
    }, this.reconnectInterval);
  }

  private handleError(error: Error): void {
    this.emit('error', error);
  }

  private emitConnectionStatus(): void {
    this.emit('connection-status', {
      connected: this.isConnected,
      reconnecting: !this.isConnected && this.reconnectAttempt > 0,
      attempt: this.reconnectAttempt,
    });
  }

  public getConnectionStatus(): ConnectionStatus {
    return {
      connected: this.isConnected,
      reconnecting: !this.isConnected && this.reconnectAttempt > 0,
      attempt: this.reconnectAttempt,
    };
  }
}

// Create singleton instance
export const websocketService = new WebSocketService();

// Export types
export type {
  MessageEvents,
  ProcessingStatus,
  ConnectionStatus,
  WebSocketMessage,
};

