import React, { createContext, useContext, useEffect, useState, useCallback } from 'react';
import { audioService, type ProcessingResult, type AudioMetadata, type ProcessingError } from '@/services/audio';

interface AudioContextState {
  isProcessing: boolean;
  currentTaskId: string | null;
  progress: number;
  metadata: AudioMetadata | null;
  error: ProcessingError | null;
  processAudio: (file: File) => Promise<void>;
  cancelProcessing: () => Promise<void>;
  downloadProcessedFile: (filename: string) => Promise<void>;
}

const AudioContext = createContext<AudioContextState | null>(null);

interface AudioProviderProps {
  children: React.ReactNode;
}

export const AudioProvider: React.FC<AudioProviderProps> = ({ children }) => {
  const [isProcessing, setIsProcessing] = useState(false);
  const [currentTaskId, setCurrentTaskId] = useState<string | null>(null);
  const [progress, setProgress] = useState(0);
  const [metadata, setMetadata] = useState<AudioMetadata | null>(null);
  const [error, setError] = useState<ProcessingError | null>(null);

  useEffect(() => {
    // Subscribe to processing updates
    const unsubscribe = audioService.onProcessingUpdate((status) => {
      setProgress(status.progress || 0);
      if (status.status === 'completed') {
        setIsProcessing(false);
      }
    });

    return () => unsubscribe();
  }, []);

  const processAudio = useCallback(async (file: File) => {
    try {
      setError(null);
      setIsProcessing(true);
      setProgress(0);

      const result = await audioService.processAudio(file);
      setCurrentTaskId(result.taskId);

      if (result.metadata) {
        setMetadata(result.metadata);
      }
    } catch (err) {
      setError(err as ProcessingError);
      setIsProcessing(false);
    }
  }, []);

  const cancelProcessing = useCallback(async () => {
    if (currentTaskId) {
      try {
        await audioService.cancelProcessing(currentTaskId);
        setIsProcessing(false);
        setCurrentTaskId(null);
        setProgress(0);
      } catch (err) {
        setError(err as ProcessingError);
      }
    }
  }, [currentTaskId]);

  const downloadProcessedFile = useCallback(async (filename: string) => {
    if (!currentTaskId) return;

    try {
      const blob = await audioService.downloadFile(currentTaskId, filename);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (err) {
      setError(err as ProcessingError);
    }
  }, [currentTaskId]);

  const value = {
    isProcessing,
    currentTaskId,
    progress,
    metadata,
    error,
    processAudio,
    cancelProcessing,
    downloadProcessedFile,
  };

  return <AudioContext.Provider value={value}>{children}</AudioContext.Provider>;
};

export const useAudio = () => {
  const context = useContext(AudioContext);
  if (!context) {
    throw new Error('useAudio must be used within an AudioProvider');
  }
  return context;
};

