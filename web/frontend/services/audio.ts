import axios, { AxiosError } from 'axios';
import { websocketService } from './websocket';
import type { ProcessingStatus, WebSocketMessage } from './websocket';

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

class AudioProcessingService {
  private readonly apiUrl: string;
  private readonly maxUploadSize: number;
  private readonly allowedTypes: string[];
  private readonly maxProcessingTime: number;

  constructor() {
    this.apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';
    this.maxUploadSize = parseInt(process.env.NEXT_PUBLIC_MAX_UPLOAD_SIZE || '500000000', 10);
    this.allowedTypes = (process.env.NEXT_PUBLIC_ALLOWED_AUDIO_TYPES || '').split(',');
    this.maxProcessingTime = parseInt(process.env.NEXT_PUBLIC_MAX_PROCESSING_TIME || '300000', 10);
  }

  /**
   * Validates the audio file before upload
   */
  private validateFile(file: File): void {
    if (file.size > this.maxUploadSize) {
      throw new Error(`File size exceeds maximum allowed size of ${this.maxUploadSize / 1024 / 1024}MB`);
    }

    if (!this.allowedTypes.includes(file.type)) {
      throw new Error(`File type ${file.type} not supported. Supported types: ${this.allowedTypes.join(', ')}`);
    }
  }

  /**
   * Processes an audio file
   */
  public async processAudio(file: File, options: ProcessingOptions = {}): Promise<ProcessingResult> {
    try {
      this.validateFile(file);

      const formData = new FormData();
      formData.append('file', file);
      formData.append('options', JSON.stringify(options));

      const response = await axios.post<ProcessingResult>(`${this.apiUrl}/audio/process`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        timeout: this.maxProcessingTime,
      });

      // Notify WebSocket about new processing task
      websocketService.send({
        type: 'processing_start',
        data: { task_id: response.data.taskId },
      });

      return response.data;
    } catch (error) {
      this.handleError(error);
      throw error;
    }
  }

  /**
   * Gets the status of a processing task
   */
  public async getProcessingStatus(taskId: string): Promise<ProcessingStatus> {
    try {
      const response = await axios.get<ProcessingStatus>(`${this.apiUrl}/audio/status/${taskId}`);
      return response.data;
    } catch (error) {
      this.handleError(error);
      throw error;
    }
  }

  /**
   * Gets metadata for a processed audio file
   */
  public async getAudioMetadata(taskId: string): Promise<AudioMetadata> {
    try {
      const response = await axios.get<AudioMetadata>(`${this.apiUrl}/audio/metadata/${taskId}`);
      return response.data;
    } catch (error) {
      this.handleError(error);
      throw error;
    }
  }

  /**
   * Downloads a processed audio file
   */
  public async downloadFile(taskId: string, filename: string): Promise<Blob> {
    try {
      const response = await axios.get(`${this.apiUrl}/audio/download/${taskId}/${filename}`, {
        responseType: 'blob',
      });
      return response.data;
    } catch (error) {
      this.handleError(error);
      throw error;
    }
  }

  /**
   * Cancels a processing task
   */
  public async cancelProcessing(taskId: string): Promise<void> {
    try {
      await axios.delete(`${this.apiUrl}/audio/process/${taskId}`);
      websocketService.send({
        type: 'processing_cancel',
        data: { task_id: taskId },
      });
    } catch (error) {
      this.handleError(error);
      throw error;
    }
  }

  /**
   * Starts real-time visualization for an audio file
   */
  public async startVisualization(taskId: string): Promise<void> {
    websocketService.send({
      type: 'visualization_start',
      data: { task_id: taskId },
    });
  }

  /**
   * Stops real-time visualization
   */
  public stopVisualization(taskId: string): void {
    websocketService.send({
      type: 'visualization_stop',
      data: { task_id: taskId },
    });
  }

  /**
   * Handles API errors
   */
  private handleError(error: unknown): never {
    if (axios.isAxiosError(error)) {
      const axiosError = error as AxiosError;
      const processingError: ProcessingError = new Error(
        axiosError.response?.data?.message || axiosError.message
      );
      processingError.code = axiosError.code;
      processingError.details = axiosError.response?.data;
      throw processingError;
    }
    throw error;
  }

  /**
   * Subscribes to processing updates
   */
  public onProcessingUpdate(callback: (status: ProcessingStatus) => void): () => void {
    websocketService.on('processing-status', callback);
    return () => websocketService.off('processing-status', callback);
  }

  /**
   * Subscribes to visualization updates
   */
  public onVisualizationUpdate(callback: (data: number[]) => void): () => void {
    websocketService.on('visualization-data', callback);
    return () => websocketService.off('visualization-data', callback);
  }

  /**
   * Subscribes to spectrum updates
   */
  public onSpectrumUpdate(callback: (data: number[]) => void): () => void {
    websocketService.on('spectrum-data', callback);
    return () => websocketService.off('spectrum-data', callback);
  }
}

// Create singleton instance
export const audioService = new AudioProcessingService();

// Export types
export type {
  ProcessingOptions,
  ProcessingResult,
  ProcessingError,
};

