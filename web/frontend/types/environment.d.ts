declare namespace NodeJS {
  interface ProcessEnv {
    // API Configuration
    NEXT_PUBLIC_API_URL: string;
    NEXT_PUBLIC_WS_URL: string;

    // Audio Processing Configuration
    NEXT_PUBLIC_MAX_UPLOAD_SIZE: string;
    NEXT_PUBLIC_ALLOWED_AUDIO_TYPES: string;
    NEXT_PUBLIC_MAX_PROCESSING_TIME: string;

    // Matrix Theme Configuration
    NEXT_PUBLIC_MATRIX_PRIMARY_COLOR: string;
    NEXT_PUBLIC_MATRIX_BACKGROUND_COLOR: string;
    NEXT_PUBLIC_MATRIX_TEXT_COLOR: string;
    NEXT_PUBLIC_MATRIX_ACCENT_COLOR: string;

    // Performance Configuration
    NEXT_PUBLIC_ANIMATION_FRAME_RATE: string;
    NEXT_PUBLIC_SPECTRUM_BANDS: string;
    NEXT_PUBLIC_VISUALIZATION_QUALITY: 'low' | 'medium' | 'high';

    // Security Configuration
    NEXT_PUBLIC_MAX_RECONNECT_ATTEMPTS: string;
    NEXT_PUBLIC_RECONNECT_INTERVAL: string;

    // Development Configuration
    NODE_ENV: 'development' | 'production' | 'test';
    DEBUG: string;
  }
}

// Audio Processing Types
declare interface AudioProcessingConfig {
  maxUploadSize: number;
  allowedTypes: string[];
  maxProcessingTime: number;
}

// Matrix Theme Types
declare interface MatrixThemeConfig {
  primaryColor: string;
  backgroundColor: string;
  textColor: string;
  accentColor: string;
}

// Performance Types
declare interface PerformanceConfig {
  animationFrameRate: number;
  spectrumBands: number;
  visualizationQuality: 'low' | 'medium' | 'high';
}

// Security Types
declare interface SecurityConfig {
  maxReconnectAttempts: number;
  reconnectInterval: number;
}

