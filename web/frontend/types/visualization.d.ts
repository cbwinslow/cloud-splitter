declare module '@/utils/visualization' {
  export interface MatrixSymbol {
    x: number;
    y: number;
    speed: number;
    char: string;
    opacity: number;
  }

  export interface VisualizationConfig {
    width: number;
    height: number;
    quality: 'low' | 'medium' | 'high';
    intensity?: number;
  }

  export interface SpectralData {
    frequencies: Float32Array;
    timeDomain: Float32Array;
    spectralData: Float32Array;
  }

  export class VisualizationService {
    constructor(config?: Partial<VisualizationConfig>);
    initAudioContext(): void;
    createAudioSource(audioElement: HTMLAudioElement): MediaElementAudioSourceNode;
    processAudioData(): SpectralData | null;
    initMatrixRain(): void;
    updateMatrixRain(ctx: CanvasRenderingContext2D, intensity?: number): void;
    drawSpectrum(ctx: CanvasRenderingContext2D, spectralData: Float32Array, intensity?: number): void;
    startAnimation(callback: () => void): void;
    stopAnimation(): void;
    dispose(): void;
    updateConfig(config: Partial<VisualizationConfig>): void;
  }

  export const visualizationService: VisualizationService;
}

