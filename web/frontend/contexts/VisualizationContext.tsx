import React, { createContext, useContext, useEffect, useState, useRef, useCallback } from 'react';
import { visualizationService, type SpectralData, type VisualizationConfig } from '@/utils/visualization';

interface VisualizationContextState {
  isAnimating: boolean;
  spectralData: SpectralData | null;
  visualizationConfig: VisualizationConfig;
  startVisualization: () => void;
  stopVisualization: () => void;
  updateConfig: (config: Partial<VisualizationConfig>) => void;
  canvasRef: React.RefObject<HTMLCanvasElement>;
}

const VisualizationContext = createContext<VisualizationContextState | null>(null);

interface VisualizationProviderProps {
  children: React.ReactNode;
}

export const VisualizationProvider: React.FC<VisualizationProviderProps> = ({ children }) => {
  const [isAnimating, setIsAnimating] = useState(false);
  const [spectralData, setSpectralData] = useState<SpectralData | null>(null);
  const [visualizationConfig, setVisualizationConfig] = useState<VisualizationConfig>({
    width: window.innerWidth,
    height: window.innerHeight,
    quality: 'high',
    intensity: 1,
  });

  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const handleResize = () => {
      const newConfig = {
        ...visualizationConfig,
        width: window.innerWidth,
        height: window.innerHeight,
      };
      setVisualizationConfig(newConfig);
      visualizationService.updateConfig(newConfig);
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, [visualizationConfig]);

  const animate = useCallback(() => {
    if (!canvasRef.current) return;

    const ctx = canvasRef.current.getContext('2d');
    if (!ctx) return;

    // Process audio data
    const data = visualizationService.processAudioData();
    if (data) {
      setSpectralData(data);
      
      // Update visualizations
      visualizationService.updateMatrixRain(ctx, visualizationConfig.intensity);
      visualizationService.drawSpectrum(ctx, data.spectralData, visualizationConfig.intensity);
    }
  }, [visualizationConfig.intensity]);

  const startVisualization = useCallback(() => {
    if (!isAnimating) {
      setIsAnimating(true);
      visualizationService.startAnimation(animate);
    }
  }, [isAnimating, animate]);

  const stopVisualization = useCallback(() => {
    if (isAnimating) {
      setIsAnimating(false);
      visualizationService.stopAnimation();
    }
  }, [isAnimating]);

  const updateConfig = useCallback((config: Partial<VisualizationConfig>) => {
    setVisualizationConfig(prev => {
      const newConfig = { ...prev, ...config };
      visualizationService.updateConfig(newConfig);
      return newConfig;
    });
  }, []);

  useEffect(() => {
    return () => {
      visualizationService.dispose();
    };
  }, []);

  const value = {
    isAnimating,
    spectralData,
    visualizationConfig,
    startVisualization,
    stopVisualization,
    updateConfig,
    canvasRef,
  };

  return <VisualizationContext.Provider value={value}>{children}</VisualizationContext.Provider>;
};

export const useVisualization = () => {
  const context = useContext(VisualizationContext);
  if (!context) {
    throw new Error('useVisualization must be used within a VisualizationProvider');
  }
  return context;
};

