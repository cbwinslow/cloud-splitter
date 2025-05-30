declare module 'typed-emitter' {
  import { EventEmitter } from 'events';

  type EventMap = {
    [key: string]: (...args: any[]) => void;
  };

  type TypedEventEmitter<Events extends EventMap> = {
    on<E extends keyof Events>(event: E, listener: Events[E]): TypedEventEmitter<Events>;
    once<E extends keyof Events>(event: E, listener: Events[E]): TypedEventEmitter<Events>;
    emit<E extends keyof Events>(event: E, ...args: Parameters<Events[E]>): boolean;
    off<E extends keyof Events>(event: E, listener: Events[E]): TypedEventEmitter<Events>;
    removeListener<E extends keyof Events>(event: E, listener: Events[E]): TypedEventEmitter<Events>;
    removeAllListeners(event?: keyof Events): TypedEventEmitter<Events>;
    listeners<E extends keyof Events>(event: E): Events[E][];
    rawListeners<E extends keyof Events>(event: E): Events[E][];
    listenerCount<E extends keyof Events>(event: E): number;
    prependListener<E extends keyof Events>(event: E, listener: Events[E]): TypedEventEmitter<Events>;
    prependOnceListener<E extends keyof Events>(event: E, listener: Events[E]): TypedEventEmitter<Events>;
    eventNames(): (keyof Events)[];
  };

  interface TypedEventEmitterClass {
    new <T extends EventMap>(): TypedEventEmitter<T>;
  }

  const TypedEventEmitter: TypedEventEmitterClass;
  export = TypedEventEmitter;
}

declare module '@/services/websocket' {
  export interface ProcessingStatus {
    status: 'idle' | 'uploading' | 'processing' | 'completed' | 'error';
    progress?: number;
    message?: string;
    taskId?: string;
  }

  export interface ConnectionStatus {
    connected: boolean;
    reconnecting: boolean;
    attempt: number;
  }

  export interface WebSocketMessage {
    type: string;
    data: any;
    timestamp?: string;
  }

  export interface MessageEvents {
    'visualization-data': (data: number[]) => void;
    'spectrum-data': (data: number[]) => void;
    'processing-status': (status: ProcessingStatus) => void;
    'connection-status': (status: ConnectionStatus) => void;
    'error': (error: Error) => void;
  }

  export class WebSocketService {
    connect(): void;
    disconnect(): void;
    send(message: WebSocketMessage): void;
    getConnectionStatus(): ConnectionStatus;
    on<E extends keyof MessageEvents>(event: E, listener: MessageEvents[E]): this;
    off<E extends keyof MessageEvents>(event: E, listener: MessageEvents[E]): this;
    once<E extends keyof MessageEvents>(event: E, listener: MessageEvents[E]): this;
  }

  export const websocketService: WebSocketService;
}

