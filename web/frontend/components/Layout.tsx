import React, { ReactNode, useEffect } from 'react';
import Head from 'next/head';
import { Box, Container, AppBar, Toolbar, Typography, useScrollTrigger, Fade } from '@mui/material';
import { ThemeProvider, CssBaseline, styled } from '@mui/material/styles';
import { theme, animations } from '@/styles/theme';

interface LayoutProps {
  children: ReactNode;
  title?: string;
  description?: string;
}

// Styled components
const StyledMain = styled('main')(({ theme }) => ({
  minHeight: '100vh',
  display: 'flex',
  flexDirection: 'column',
  background: theme.palette.background.default,
  position: 'relative',
  overflow: 'hidden',
}));

const MatrixBackground = styled(Box)(({ theme }) => ({
  position: 'fixed',
  top: 0,
  left: 0,
  width: '100%',
  height: '100%',
  zIndex: -1,
  background: 'linear-gradient(180deg, rgba(0,0,0,0.9) 0%, rgba(0,0,0,1) 100%)',
  '&::before': {
    content: '""',
    position: 'absolute',
    top: 0,
    left: 0,
    width: '100%',
    height: '100%',
    background: `repeating-linear-gradient(
      0deg,
      rgba(0, 255, 0, 0.03) 0px,
      rgba(0, 255, 0, 0.03) 1px,
      transparent 1px,
      transparent 2px
    )`,
    animation: `${animations.pulse} 2s infinite ease-in-out`,
    pointerEvents: 'none',
  },
}));

const StyledAppBar = styled(AppBar)(({ theme }) => ({
  background: 'rgba(0, 0, 0, 0.8)',
  backdropFilter: 'blur(10px)',
  borderBottom: `1px solid ${theme.palette.primary.main}`,
  boxShadow: `0 0 10px ${theme.palette.primary.main}`,
}));

const StyledToolbar = styled(Toolbar)(({ theme }) => ({
  justifyContent: 'space-between',
  [theme.breakpoints.up('sm')]: {
    padding: theme.spacing(0, 4),
  },
}));

const Footer = styled('footer')(({ theme }) => ({
  marginTop: 'auto',
  padding: theme.spacing(3),
  background: 'rgba(0, 0, 0, 0.8)',
  backdropFilter: 'blur(10px)',
  borderTop: `1px solid ${theme.palette.primary.main}`,
  textAlign: 'center',
  color: theme.palette.primary.main,
}));

const Layout: React.FC<LayoutProps> = ({
  children,
  title = 'Cloud Splitter - Audio Processing & Visualization',
  description = 'Advanced audio processing and visualization with real-time spectrum analysis',
}) => {
  const trigger = useScrollTrigger({
    disableHysteresis: true,
    threshold: 0,
  });

  // Load matrix font
  useEffect(() => {
    const loadFont = async () => {
      const font = new FontFace(
        'Share Tech Mono',
        `url('/fonts/ShareTechMono-Regular.ttf') format('truetype')`
      );
      await font.load();
      document.fonts.add(font);
    };
    loadFont().catch(console.error);
  }, []);

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Head>
        <title>{title}</title>
        <meta name="description" content={description} />
        <meta name="viewport" content="initial-scale=1.0, width=device-width" />
        <link rel="icon" href="/favicon.ico" />
        <meta name="theme-color" content="#000000" />
        <meta name="apple-mobile-web-app-capable" content="yes" />
        <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent" />
      </Head>

      <StyledMain>
        <MatrixBackground />
        
        <Fade in={!trigger}>
          <StyledAppBar position="fixed" elevation={0}>
            <StyledToolbar>
              <Typography
                variant="h6"
                component="h1"
                sx={{
                  fontFamily: '"Share Tech Mono", monospace',
                  letterSpacing: '0.1em',
                  textShadow: `0 0 10px ${theme.palette.primary.main}`,
                  animation: `${animations.glow} 2s infinite ease-in-out`,
                }}
              >
                CLOUD SPLITTER
              </Typography>
            </StyledToolbar>
          </StyledAppBar>
        </Fade>

        <Box
          component="div"
          sx={{
            flexGrow: 1,
            pt: { xs: 8, sm: 9 },
            pb: { xs: 4, sm: 5 },
          }}
        >
          <Container
            maxWidth="xl"
            sx={{
              height: '100%',
              display: 'flex',
              flexDirection: 'column',
            }}
          >
            {children}
          </Container>
        </Box>

        <Footer>
          <Typography
            variant="body2"
            sx={{
              fontFamily: '"Share Tech Mono", monospace',
              opacity: 0.8,
              '&:hover': {
                opacity: 1,
                textShadow: `0 0 10px ${theme.palette.primary.main}`,
              },
              transition: 'all 0.3s ease',
            }}
          >
            © {new Date().getFullYear()} Cloud Splitter | Matrix Audio Processing System
          </Typography>
        </Footer>
      </StyledMain>
    </ThemeProvider>
  );
};

export default Layout;

import React, { ReactNode } from 'react';
import Head from 'next/head';
import { ThemeProvider, CssBaseline } from '@mui/material';
import { theme } from '@/styles/theme';

interface LayoutProps {
  children: ReactNode;
  title?: string;
}

const Layout: React.FC<LayoutProps> = ({ 
  children, 
  title = 'Cloud Splitter - Audio Processing'
}) => {
  return (
    <>
      <Head>
        <title>{title}</title>
        <meta charSet="utf-8" />
        <meta name="viewport" content="initial-scale=1.0, width=device-width" />
        <meta name="description" content="Advanced audio processing and visualization" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <div className="app-container">
          <header className="app-header">
            <h1>{title}</h1>
          </header>
          <main className="app-main">
            {children}
          </main>
          <footer className="app-footer">
            <p>© {new Date().getFullYear()} Cloud Splitter</p>
          </footer>
        </div>
      </ThemeProvider>
    </>
  );
};

export default Layout;

