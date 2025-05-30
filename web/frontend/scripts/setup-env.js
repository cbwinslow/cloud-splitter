#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const chalk = require('chalk');
const prompts = require('prompts');

const ENV_FILES = {
  development: '.env.development',
  production: '.env.production',
  local: '.env.local',
};

const DEFAULT_CONFIG = {
  development: {
    NEXT_PUBLIC_API_URL: 'http://localhost:8000/api/v1',
    NEXT_PUBLIC_WS_URL: 'ws://localhost:8000/api/v1/ws',
    NEXT_PUBLIC_MAX_UPLOAD_SIZE: '500000000',
    NEXT_PUBLIC_ALLOWED_AUDIO_TYPES: 'audio/mpeg,audio/wav,audio/x-wav,audio/mp3',
    NEXT_PUBLIC_MAX_PROCESSING_TIME: '300000',
    NEXT_PUBLIC_MATRIX_PRIMARY_COLOR: '#00ff00',
    NEXT_PUBLIC_MATRIX_BACKGROUND_COLOR: '#000000',
    NEXT_PUBLIC_MATRIX_TEXT_COLOR: '#00ff00',
    NEXT_PUBLIC_MATRIX_ACCENT_COLOR: '#33ff33',
    NEXT_PUBLIC_ANIMATION_FRAME_RATE: '60',
    NEXT_PUBLIC_SPECTRUM_BANDS: '10',
    NEXT_PUBLIC_VISUALIZATION_QUALITY: 'high',
    NEXT_PUBLIC_MAX_RECONNECT_ATTEMPTS: '5',
    NEXT_PUBLIC_RECONNECT_INTERVAL: '3000',
    NODE_ENV: 'development',
    DEBUG: 'true',
  },
  production: {
    NEXT_PUBLIC_API_URL: '',
    NEXT_PUBLIC_WS_URL: '',
    NEXT_PUBLIC_MAX_UPLOAD_SIZE: '500000000',
    NEXT_PUBLIC_ALLOWED_AUDIO_TYPES: 'audio/mpeg,audio/wav,audio/x-wav,audio/mp3',
    NEXT_PUBLIC_MAX_PROCESSING_TIME: '300000',
    NEXT_PUBLIC_MATRIX_PRIMARY_COLOR: '#00ff00',
    NEXT_PUBLIC_MATRIX_BACKGROUND_COLOR: '#000000',
    NEXT_PUBLIC_MATRIX_TEXT_COLOR: '#00ff00',
    NEXT_PUBLIC_MATRIX_ACCENT_COLOR: '#33ff33',
    NEXT_PUBLIC_ANIMATION_FRAME_RATE: '60',
    NEXT_PUBLIC_SPECTRUM_BANDS: '10',
    NEXT_PUBLIC_VISUALIZATION_QUALITY: 'high',
    NEXT_PUBLIC_MAX_RECONNECT_ATTEMPTS: '5',
    NEXT_PUBLIC_RECONNECT_INTERVAL: '3000',
    NODE_ENV: 'production',
    DEBUG: 'false',
  },
};

const createEnvFile = async (environment) => {
  const config = DEFAULT_CONFIG[environment];
  const filePath = path.join(process.cwd(), ENV_FILES[environment]);

  if (environment === 'production') {
    const response = await prompts([
      {
        type: 'text',
        name: 'apiUrl',
        message: 'Enter the production API URL:',
        validate: value => value.length > 0 || 'API URL is required',
      },
      {
        type: 'text',
        name: 'wsUrl',
        message: 'Enter the production WebSocket URL:',
        validate: value => value.length > 0 || 'WebSocket URL is required',
      },
    ]);

    config.NEXT_PUBLIC_API_URL = response.apiUrl;
    config.NEXT_PUBLIC_WS_URL = response.wsUrl;
  }

  const envContent = Object.entries(config)
    .map(([key, value]) => `${key}=${value}`)
    .join('\n');

  fs.writeFileSync(filePath, envContent);
  console.log(chalk.green(`Created ${ENV_FILES[environment]} successfully!`));
};

const setup = async () => {
  try {
    console.log(chalk.blue('Setting up environment files...'));

    // Create development environment file
    await createEnvFile('development');

    // Create production environment file
    await createEnvFile('production');

    // Create local environment file (copy of development)
    fs.copyFileSync(
      path.join(process.cwd(), ENV_FILES.development),
      path.join(process.cwd(), ENV_FILES.local)
    );
    console.log(chalk.green(`Created ${ENV_FILES.local} successfully!`));

    console.log(chalk.green('\nEnvironment setup completed successfully!'));
  } catch (error) {
    console.error(chalk.red('Environment setup failed:'), error);
    process.exit(1);
  }
};

setup();

