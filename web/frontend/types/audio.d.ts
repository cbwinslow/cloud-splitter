declare module '@/services/audio' {
  export interface AudioMetadata {
    duration: number;
    sampleRate: number;
    tempo: number;
    key: number[][];
    spectralFeatures: {
      centroids: number[][];
      rolloff: number[][];
      bandwidth?: number[][];
      contrast?: number[][];
      flatness?: number[][];
    };
  }

  export interface ProcessingResult {
    taskId: string;
    status: string;
    metadata?: AudioMetadata;
    files?: string[];
  }

  export interface ProcessingError extends Error {
    code?: string;
    details?: any;
  }

  export interface ProcessingOptions {
    splitStems?: boolean;
    quality?: 'low' | 'medium' | 'high';
    outputFormat?: 'wav' | 'mp3' | 'flac';
  }

  export class AudioProcessingService {
    processAudio(file: File, options?: ProcessingOptions): Promise<ProcessingResult>;
    getProcessingStatus(taskId: string): Promise<import('@/services/websocket').ProcessingStatus>;
    getAudioMetadata(taskId: string): Promise<AudioMetadata>;
    downloadFile(taskId: string, filename: string): Promise<Blob>;
    cancelProcessing(taskId: string): Promise<void>;
    startVisualization(taskId: string): Promise<void>;
    stopVisualization(taskId: string): void;
    onProcessingUpdate(callback: (status: import('@/services/websocket').ProcessingStatus) => void): () => void;
    onVisualizationUpdate(callback: (data: number[]) => void): () => void;
    onSpectrumUpdate(callback: (data: number[]) => void): () => void;
  }

  export const audioService: AudioProcessingService;
}

