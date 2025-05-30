// Constants for visualization
const FRAME_RATE = parseInt(process.env.NEXT_PUBLIC_ANIMATION_FRAME_RATE || '60', 10);
const SPECTRUM_BANDS = parseInt(process.env.NEXT_PUBLIC_SPECTRUM_BANDS || '10', 10);
const MATRIX_CHARACTERS = '0123456789ABCDEF';
const FFT_SIZE = 2048;

interface MatrixSymbol {
  x: number;
  y: number;
  speed: number;
  char: string;
  opacity: number;
}

interface VisualizationConfig {
  width: number;
  height: number;
  quality: 'low' | 'medium' | 'high';
  intensity?: number;
}

interface SpectralData {
  frequencies: Float32Array;
  timeDomain: Float32Array;
  spectralData: Float32Array;
}

class VisualizationService {
  private audioContext: AudioContext | null = null;
  private analyser: AnalyserNode | null = null;
  private matrixSymbols: MatrixSymbol[] = [];
  private frameId: number = 0;
  private lastFrameTime: number = 0;
  private config: VisualizationConfig;

  constructor(config: Partial<VisualizationConfig> = {}) {
    this.config = {
      width: window.innerWidth,
      height: window.innerHeight,
      quality: process.env.NEXT_PUBLIC_VISUALIZATION_QUALITY as 'low' | 'medium' | 'high' || 'medium',
      intensity: 1,
      ...config,
    };
  }

  /**
   * Initializes the audio context and analyzer
   */
  public initAudioContext(): void {
    if (!this.audioContext) {
      this.audioContext = new (window.AudioContext || (window as any).webkitAudioContext)();
      this.analyser = this.audioContext.createAnalyser();
      this.analyser.fftSize = FFT_SIZE;
      this.analyser.smoothingTimeConstant = 0.8;
    }
  }

  /**
   * Creates an audio source from an audio element
   */
  public createAudioSource(audioElement: HTMLAudioElement): MediaElementAudioSourceNode {
    if (!this.audioContext || !this.analyser) {
      this.initAudioContext();
    }
    const source = this.audioContext!.createMediaElementSource(audioElement);
    source.connect(this.analyser!);
    this.analyser!.connect(this.audioContext!.destination);
    return source;
  }

  /**
   * Processes audio data for visualization
   */
  public processAudioData(): SpectralData | null {
    if (!this.analyser) return null;

    const frequencyData = new Float32Array(this.analyser.frequencyBinCount);
    const timeDomainData = new Float32Array(this.analyser.frequencyBinCount);
    const spectralData = new Float32Array(SPECTRUM_BANDS);

    this.analyser.getFloatFrequencyData(frequencyData);
    this.analyser.getFloatTimeDomainData(timeDomainData);

    // Calculate spectrum bands
    const bandSize = Math.floor(frequencyData.length / SPECTRUM_BANDS);
    for (let i = 0; i < SPECTRUM_BANDS; i++) {
      let sum = 0;
      for (let j = 0; j < bandSize; j++) {
        sum += frequencyData[i * bandSize + j];
      }
      spectralData[i] = (sum / bandSize + 140) / 140; // Normalize to 0-1
    }

    return {
      frequencies: frequencyData,
      timeDomain: timeDomainData,
      spectralData,
    };
  }

  /**
   * Initializes matrix rain effect
   */
  public initMatrixRain(): void {
    const symbolCount = Math.floor((this.config.width * this.config.height) / 1000);
    this.matrixSymbols = Array.from({ length: symbolCount }, () => this.createMatrixSymbol());
  }

  /**
   * Creates a new matrix symbol
   */
  private createMatrixSymbol(): MatrixSymbol {
    return {
      x: Math.random() * this.config.width,
      y: Math.random() * this.config.height,
      speed: 1 + Math.random() * 3,
      char: MATRIX_CHARACTERS[Math.floor(Math.random() * MATRIX_CHARACTERS.length)],
      opacity: 0.1 + Math.random() * 0.9,
    };
  }

  /**
   * Updates matrix rain animation
   */
  public updateMatrixRain(ctx: CanvasRenderingContext2D, intensity: number = 1): void {
    const now = performance.now();
    const deltaTime = now - this.lastFrameTime;
    
    if (deltaTime < (1000 / FRAME_RATE)) return;
    
    this.lastFrameTime = now;

    ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
    ctx.fillRect(0, 0, this.config.width, this.config.height);

    ctx.fillStyle = '#00ff00';
    ctx.font = '15px "Share Tech Mono"';

    this.matrixSymbols.forEach(symbol => {
      if (Math.random() < 0.02) {
        symbol.char = MATRIX_CHARACTERS[Math.floor(Math.random() * MATRIX_CHARACTERS.length)];
      }

      const glowIntensity = Math.sin(now / 1000) * 0.5 + 0.5;
      ctx.shadowBlur = 5 * glowIntensity * intensity;
      ctx.shadowColor = '#00ff00';
      
      ctx.globalAlpha = symbol.opacity * intensity;
      ctx.fillText(symbol.char, symbol.x, symbol.y);

      symbol.y += symbol.speed;
      if (symbol.y > this.config.height) {
        Object.assign(symbol, this.createMatrixSymbol(), { y: 0 });
      }
    });

    ctx.globalAlpha = 1;
    ctx.shadowBlur = 0;
  }

  /**
   * Draws spectrum analyzer
   */
  public drawSpectrum(
    ctx: CanvasRenderingContext2D,
    spectralData: Float32Array,
    intensity: number = 1
  ): void {
    const barWidth = this.config.width / SPECTRUM_BANDS;
    const maxHeight = this.config.height * 0.8;

    ctx.clearRect(0, 0, this.config.width, this.config.height);

    spectralData.forEach((value, i) => {
      const height = value * maxHeight * intensity;
      const x = i * barWidth;
      const y = this.config.height - height;

      const gradient = ctx.createLinearGradient(x, y, x, this.config.height);
      gradient.addColorStop(0, 'rgba(0, 255, 0, 0.8)');
      gradient.addColorStop(1, 'rgba(0, 255, 0, 0.2)');

      ctx.fillStyle = gradient;
      ctx.fillRect(x, y, barWidth - 2, height);

      // Add glow effect
      ctx.shadowBlur = 15;
      ctx.shadowColor = '#00ff00';
      ctx.fillRect(x, y, barWidth - 2, height);
      ctx.shadowBlur = 0;
    });
  }

  /**
   * Starts animation loop
   */
  public startAnimation(callback: () => void): void {
    const animate = () => {
      callback();
      this.frameId = requestAnimationFrame(animate);
    };
    this.frameId = requestAnimationFrame(animate);
  }

  /**
   * Stops animation loop
   */
  public stopAnimation(): void {
    if (this.frameId) {
      cancelAnimationFrame(this.frameId);
    }
  }

  /**
   * Cleans up resources
   */
  public dispose(): void {
    this.stopAnimation();
    if (this.audioContext) {
      this.audioContext.close();
      this.audioContext = null;
      this.analyser = null;
    }
  }

  /**
   * Updates configuration
   */
  public updateConfig(config: Partial<VisualizationConfig>): void {
    this.config = {
      ...this.config,
      ...config,
    };
    this.initMatrixRain();
  }
}

// Create singleton instance
export const visualizationService = new VisualizationService();

// Export types
export type {
  VisualizationConfig,
  SpectralData,
  MatrixSymbol,
};

