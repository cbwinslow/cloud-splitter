import { useState, useCallback } from 'react';
import axios from 'axios';

interface ProcessingResult {
  task_id: string;
  status: string;
  metadata?: AudioMetadata;
}

interface AudioMetadata {
  duration: number;
  sample_rate: number;
  tempo: number;
  key: number[][];
  spectral_features: {
    centroids: number[][];
    rolloff: number[][];
    bandwidth?: number[][];
    contrast?: number[][];
    flatness?: number[][];
  };
}

interface ProcessingError {
  message: string;
  code?: string;
  details?: any;
}

export const useAudioProcessor = () => {
  const [processingProgress, setProcessingProgress] = useState(0);
  const [processingError, setProcessingError] = useState<ProcessingError | null>(null);
  const [metadata, setMetadata] = useState<AudioMetadata | null>(null);

  const processAudio = useCallback(async (file: File): Promise<ProcessingResult> => {
    try {
      setProcessingProgress(0);
      setProcessingError(null);

      // Create form data
      const formData = new FormData();
      formData.append('file', file);

      // Upload file
      const uploadResponse = await axios.post<ProcessingResult>(
        '/api/v1/audio/upload',
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
          onUploadProgress: (progressEvent) => {
            const progress = progressEvent.total
              ? Math.round((progressEvent.loaded * 100) / progressEvent.total)
              : 0;
            setProcessingProgress(progress);
          },
        }
      );

      const { task_id } = uploadResponse.data;

      // Poll for processing status
      const result = await pollProcessingStatus(task_id);
      
      if (result.metadata) {
        setMetadata(result.metadata);
      }

      return result;
    } catch (error) {
      const processingError: ProcessingError = {
        message: 'Failed to process audio file',
        details: error,
      };

      if (axios.isAxiosError(error)) {
        processingError.code = error.code;
        processingError.message = error.response?.data?.message || error.message;
      }

      setProcessingError(processingError);
      throw processingError;
    }
  }, []);

  const pollProcessingStatus = async (taskId: string): Promise<ProcessingResult> => {
    const poll = async (): Promise<ProcessingResult> => {
      const response = await axios.get<ProcessingResult>(`/api/v1/audio/status/${taskId}`);
      
      if (response.data.status === 'completed') {
        setProcessingProgress(100);
        return response.data;
      }
      
      if (response.data.status === 'failed') {
        throw new Error('Processing failed');
      }
      
      // Update progress based on status response
      if (response.data.status === 'processing') {
        // Assuming the backend provides a progress value
        const progress = Math.min(95, processingProgress + 5);
        setProcessingProgress(progress);
      }

      // Continue polling
      await new Promise(resolve => setTimeout(resolve, 1000));
      return poll();
    };

    return poll();
  };

  const getAudioMetadata = useCallback(async (taskId: string): Promise<AudioMetadata> => {
    try {
      const response = await axios.get<AudioMetadata>(`/api/v1/audio/metadata/${taskId}`);
      setMetadata(response.data);
      return response.data;
    } catch (error) {
      const metadataError: ProcessingError = {
        message: 'Failed to fetch audio metadata',
        details: error,
      };
      setProcessingError(metadataError);
      throw metadataError;
    }
  }, []);

  const downloadProcessedFile = useCallback(async (taskId: string): Promise<Blob> => {
    try {
      const response = await axios.get(`/api/v1/audio/download/${taskId}`, {
        responseType: 'blob',
      });
      return response.data;
    } catch (error) {
      const downloadError: ProcessingError = {
        message: 'Failed to download processed file',
        details: error,
      };
      setProcessingError(downloadError);
      throw downloadError;
    }
  }, []);

  const cancelProcessing = useCallback(async (taskId: string): Promise<void> => {
    try {
      await axios.delete(`/api/v1/audio/${taskId}`);
      setProcessingProgress(0);
      setProcessingError(null);
      setMetadata(null);
    } catch (error) {
      const cancelError: ProcessingError = {
        message: 'Failed to cancel processing',
        details: error,
      };
      setProcessingError(cancelError);
      throw cancelError;
    }
  }, []);

  return {
    processAudio,
    getAudioMetadata,
    downloadProcessedFile,
    cancelProcessing,
    processingProgress,
    processingError,
    metadata,
  };
};

export type {
  ProcessingResult,
  AudioMetadata,
  ProcessingError,
};

