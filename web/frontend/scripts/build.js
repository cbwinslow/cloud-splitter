#!/usr/bin/env node
const { execSync } = require('child_process');
const path = require('path');
const fs = require('fs');
const chalk = require('chalk');

const projectRoot = path.join(__dirname, '..');

// Validation functions
const validateDependencies = () => {
  console.log(chalk.blue('Validating dependencies...'));
  try {
    execSync('npm list --json', { stdio: 'ignore' });
  } catch (error) {
    console.error(chalk.red('Dependency validation failed. Please run npm install.'));
    process.exit(1);
  }
};

const validateEnvironment = () => {
  console.log(chalk.blue('Validating environment...'));
  const requiredEnvVars = [
    'NEXT_PUBLIC_API_URL',
    'NEXT_PUBLIC_WS_URL',
    'NEXT_PUBLIC_MAX_UPLOAD_SIZE',
  ];

  const missingVars = requiredEnvVars.filter(varName => !process.env[varName]);
  if (missingVars.length > 0) {
    console.error(chalk.red(`Missing required environment variables: ${missingVars.join(', ')}`));
    process.exit(1);
  }
};

const build = async () => {
  try {
    console.log(chalk.green('Starting build process...'));

    // Validate environment and dependencies
    validateEnvironment();
    validateDependencies();

    // Clean previous build
    console.log(chalk.blue('Cleaning previous build...'));
    execSync('rm -rf .next', { stdio: 'inherit', cwd: projectRoot });

    // Type checking
    console.log(chalk.blue('Running type check...'));
    execSync('tsc --noEmit', { stdio: 'inherit', cwd: projectRoot });

    // Lint checking
    console.log(chalk.blue('Running lint check...'));
    execSync('npm run lint', { stdio: 'inherit', cwd: projectRoot });

    // Build application
    console.log(chalk.blue('Building application...'));
    execSync('next build', { stdio: 'inherit', cwd: projectRoot });

    // Generate static files if needed
    if (process.env.GENERATE_STATIC === 'true') {
      console.log(chalk.blue('Generating static files...'));
      execSync('next export', { stdio: 'inherit', cwd: projectRoot });
    }

    console.log(chalk.green('Build completed successfully!'));
  } catch (error) {
    console.error(chalk.red('Build failed:'), error);
    process.exit(1);
  }
};

build();

