import { createTheme, ThemeOptions } from '@mui/material/styles';
import { keyframes } from '@emotion/react';

// Define Matrix theme colors
const matrixColors = {
  green: {
    main: '#00ff00',
    light: '#33ff33',
    dark: '#00cc00',
    contrastText: '#000000',
  },
  black: {
    main: '#000000',
    light: '#121212',
    dark: '#000000',
    contrastText: '#00ff00',
  },
  background: {
    default: '#000000',
    paper: 'rgba(0, 0, 0, 0.8)',
  },
};

// Define animations
const glowKeyframes = keyframes`
  0% { text-shadow: 0 0 5px rgba(0, 255, 0, 0.5); }
  50% { text-shadow: 0 0 20px rgba(0, 255, 0, 0.8); }
  100% { text-shadow: 0 0 5px rgba(0, 255, 0, 0.5); }
`;

const pulseKeyframes = keyframes`
  0% { opacity: 1; }
  50% { opacity: 0.5; }
  100% { opacity: 1; }
`;

// Theme customization
const themeOptions: ThemeOptions = {
  palette: {
    mode: 'dark',
    primary: matrixColors.green,
    secondary: matrixColors.black,
    background: matrixColors.background,
    text: {
      primary: matrixColors.green.main,
      secondary: matrixColors.green.light,
    },
    action: {
      active: matrixColors.green.main,
      hover: matrixColors.green.light,
      selected: matrixColors.green.dark,
      disabled: 'rgba(0, 255, 0, 0.3)',
      disabledBackground: 'rgba(0, 255, 0, 0.12)',
    },
    divider: 'rgba(0, 255, 0, 0.12)',
  },

  typography: {
    fontFamily: '"Share Tech Mono", "Roboto Mono", monospace',
    h1: {
      fontSize: '2.5rem',
      fontWeight: 400,
      letterSpacing: '0.2rem',
      textShadow: '0 0 10px rgba(0, 255, 0, 0.5)',
    },
    h2: {
      fontSize: '2rem',
      fontWeight: 400,
      letterSpacing: '0.15rem',
    },
    h3: {
      fontSize: '1.75rem',
      fontWeight: 400,
      letterSpacing: '0.1rem',
    },
    h4: {
      fontSize: '1.5rem',
      fontWeight: 400,
      letterSpacing: '0.08rem',
    },
    h5: {
      fontSize: '1.25rem',
      fontWeight: 400,
      letterSpacing: '0.05rem',
    },
    h6: {
      fontSize: '1rem',
      fontWeight: 400,
      letterSpacing: '0.03rem',
    },
    body1: {
      fontSize: '1rem',
      letterSpacing: '0.02rem',
    },
    body2: {
      fontSize: '0.875rem',
      letterSpacing: '0.01rem',
    },
  },

  components: {
    MuiCssBaseline: {
      styleOverrides: {
        '@global': {
          '@font-face': [
            {
              fontFamily: 'Share Tech Mono',
              fontStyle: 'normal',
              fontWeight: 400,
              src: `url('/fonts/ShareTechMono-Regular.ttf') format('truetype')`,
            },
          ],
          body: {
            backgroundColor: '#000000',
            color: '#00ff00',
            fontFamily: '"Share Tech Mono", monospace',
            '&::-webkit-scrollbar': {
              width: '8px',
            },
            '&::-webkit-scrollbar-track': {
              background: '#000000',
            },
            '&::-webkit-scrollbar-thumb': {
              background: '#00ff00',
              borderRadius: '4px',
            },
          },
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: '4px',
          textTransform: 'none',
          transition: 'all 0.3s ease',
          '&:hover': {
            boxShadow: '0 0 15px rgba(0, 255, 0, 0.5)',
          },
        },
        contained: {
          backgroundColor: 'rgba(0, 255, 0, 0.1)',
          border: '1px solid #00ff00',
          '&:hover': {
            backgroundColor: 'rgba(0, 255, 0, 0.2)',
          },
        },
        outlined: {
          borderColor: '#00ff00',
          '&:hover': {
            borderColor: '#33ff33',
            backgroundColor: 'rgba(0, 255, 0, 0.1)',
          },
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          backgroundColor: 'rgba(0, 0, 0, 0.8)',
          backdropFilter: 'blur(10px)',
          border: '1px solid rgba(0, 255, 0, 0.1)',
          transition: 'all 0.3s ease',
          '&:hover': {
            boxShadow: '0 0 20px rgba(0, 255, 0, 0.2)',
          },
        },
      },
    },
    MuiTextField: {
      styleOverrides: {
        root: {
          '& .MuiOutlinedInput-root': {
            '& fieldset': {
              borderColor: 'rgba(0, 255, 0, 0.3)',
            },
            '&:hover fieldset': {
              borderColor: 'rgba(0, 255, 0, 0.5)',
            },
            '&.Mui-focused fieldset': {
              borderColor: '#00ff00',
            },
          },
        },
      },
    },
    MuiLinearProgress: {
      styleOverrides: {
        root: {
          backgroundColor: 'rgba(0, 255, 0, 0.1)',
          '& .MuiLinearProgress-bar': {
            backgroundColor: '#00ff00',
          },
        },
      },
    },
    MuiCircularProgress: {
      styleOverrides: {
        root: {
          color: '#00ff00',
        },
      },
    },
  },

  transitions: {
    duration: {
      shortest: 150,
      shorter: 200,
      short: 250,
      standard: 300,
      complex: 375,
      enteringScreen: 225,
      leavingScreen: 195,
    },
    easing: {
      easeInOut: 'cubic-bezier(0.4, 0, 0.2, 1)',
      easeOut: 'cubic-bezier(0.0, 0, 0.2, 1)',
      easeIn: 'cubic-bezier(0.4, 0, 1, 1)',
      sharp: 'cubic-bezier(0.4, 0, 0.6, 1)',
    },
  },

  shape: {
    borderRadius: 4,
  },
};

// Create custom animations
const animations = {
  glow: glowKeyframes,
  pulse: pulseKeyframes,
};

// Create and export theme
export const theme = createTheme(themeOptions);
export { animations };

// Export types for custom theme
declare module '@mui/material/styles' {
  interface Theme {
    animations: typeof animations;
  }
  interface ThemeOptions {
    animations?: typeof animations;
  }
}

