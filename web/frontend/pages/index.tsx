import { useState, useEffect, useCallback } from 'react';
import type { NextPage } from 'next';
import {
  Box,
  Container,
  Paper,
  Typography,
  Button,
  Alert,
  Fade,
  useTheme,
} from '@mui/material';
import CloudDownloadIcon from '@mui/icons-material/CloudDownload';
import ReplayIcon from '@mui/icons-material/Replay';
import Layout from '@/components/Layout';
import AudioVisualizer from '@/components/AudioVisualizer';
import SpectrumAnalyzer from '@/components/SpectrumAnalyzer';
import FileUpload from '@/components/FileUpload';
import ProcessingStatus from '@/components/ProcessingStatus';
import BackgroundEffect from '@/components/BackgroundEffect';
import { useWebSocket } from '@/hooks/useWebSocket';
import { useAudioProcessor } from '@/hooks/useAudioProcessor';
import { WebSocketMessage } from '@/hooks/useWebSocket';
import { ProcessingResult, AudioMetadata } from '@/hooks/useAudioProcessor';

const Home: NextPage = () => {
  const theme = useTheme();
  const [audioFile, setAudioFile] = useState<File | null>(null);
  const [currentTaskId, setCurrentTaskId] = useState<string | null>(null);
  const [processingStatus, setProcessingStatus] = useState<string>('idle');
  const [visualizationData, setVisualizationData] = useState<number[]>([]);
  const [spectrumData, setSpectrumData] = useState<number[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [downloadReady, setDownloadReady] = useState(false);

  const {
    processAudio,
    getAudioMetadata,
    downloadProcessedFile,
    cancelProcessing,
    processingProgress,
    processingError,
    metadata,
  } = useAudioProcessor();

  // WebSocket connection for real-time updates
  const ws = useWebSocket('ws://localhost:8000/api/v1/ws/audio', {
    onMessage: (message: WebSocketMessage) => handleWebSocketMessage(message),
    onError: () => setError('WebSocket connection failed'),
  });

  // Handle WebSocket messages
  const handleWebSocketMessage = useCallback((message: WebSocketMessage) => {
    switch (message.type) {
      case 'visualization_data':
        setVisualizationData(message.data);
        break;
      case 'spectrum_data':
        setSpectrumData(message.data);
        break;
      case 'processing_status':
        setProcessingStatus(message.data.status);
        if (message.data.status === 'completed') {
          setDownloadReady(true);
        }
        break;
      case 'error':
        setError(message.data.message);
        break;
    }
  }, []);

  // Handle file upload
  const handleFileUpload = async (file: File) => {
    try {
      setAudioFile(file);
      setProcessingStatus('uploading');
      setError(null);
      setDownloadReady(false);

      const result: ProcessingResult = await processAudio(file);
      setCurrentTaskId(result.task_id);

      // Notify WebSocket about new processing task
      ws.sendMessage({
        type: 'processing_start',
        data: { task_id: result.task_id },
      });

    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to process file');
      setProcessingStatus('error');
    }
  };

  // Handle download
  const handleDownload = async () => {
    if (!currentTaskId) return;

    try {
      const blob = await downloadProcessedFile(currentTaskId);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `processed_${audioFile?.name || 'audio'}.wav`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (err) {
      setError('Failed to download processed file');
    }
  };

  // Handle reset
  const handleReset = () => {
    setAudioFile(null);
    setCurrentTaskId(null);
    setProcessingStatus('idle');
    setError(null);
    setDownloadReady(false);
    setVisualizationData([]);
    setSpectrumData([]);
  };

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (currentTaskId) {
        cancelProcessing(currentTaskId).catch(console.error);
      }
    };
  }, [currentTaskId, cancelProcessing]);

  return (
    <Layout>
      <BackgroundEffect spectrumData={spectrumData} />
      
      <Container maxWidth="lg">
        <Box sx={{ py: 4 }}>
          <Paper
            elevation={3}
            sx={{
              p: 4,
              background: 'rgba(0, 0, 0, 0.8)',
              border: `1px solid ${theme.palette.primary.main}`,
              backdropFilter: 'blur(10px)',
            }}
          >
            <Typography
              variant="h2"
              component="h1"
              gutterBottom
              sx={{
                textAlign: 'center',
                color: theme.palette.primary.main,
                textShadow: `0 0 10px ${theme.palette.primary.main}`,
                mb: 4,
              }}
            >
              Audio Processing & Visualization
            </Typography>

            {error && (
              <Fade in={!!error}>
                <Alert
                  severity="error"
                  onClose={() => setError(null)}
                  sx={{ mb: 3 }}
                >
                  {error}
                </Alert>
              </Fade>
            )}

            {processingStatus === 'idle' ? (
              <FileUpload onFileUpload={handleFileUpload} />
            ) : (
              <Box sx={{ mb: 4 }}>
                <ProcessingStatus
                  status={processingStatus}
                  progress={processingProgress}
                />
              </Box>
            )}

            {visualizationData.length > 0 && (
              <Box sx={{ mt: 4 }}>
                <Typography
                  variant="h6"
                  sx={{
                    color: theme.palette.primary.main,
                    mb: 2,
                  }}
                >
                  Waveform Visualization
                </Typography>
                <AudioVisualizer data={visualizationData} />
              </Box>
            )}

            {spectrumData.length > 0 && (
              <Box sx={{ mt: 4 }}>
                <Typography
                  variant="h6"
                  sx={{
                    color: theme.palette.primary.main,
                    mb: 2,
                  }}
                >
                  Spectrum Analysis
                </Typography>
                <SpectrumAnalyzer data={spectrumData} />
              </Box>
            )}

            {(downloadReady || processingStatus === 'completed') && (
              <Box
                sx={{
                  mt: 4,
                  display: 'flex',
                  justifyContent: 'center',
                  gap: 2,
                }}
              >
                <Button
                  variant="contained"
                  startIcon={<CloudDownloadIcon />}
                  onClick={handleDownload}
                  sx={{
                    borderColor: theme.palette.primary.main,
                    color: theme.palette.primary.main,
                  }}
                >
                  Download Processed Audio
                </Button>
                <Button
                  variant="outlined"
                  startIcon={<ReplayIcon />}
                  onClick={handleReset}
                  sx={{
                    borderColor: theme.palette.primary.main,
                    color: theme.palette.primary.main,
                  }}
                >
                  Process New File
                </Button>
              </Box>
            )}

            {metadata && (
              <Box sx={{ mt: 4 }}>
                <Typography
                  variant="h6"
                  sx={{
                    color: theme.palette.primary.main,
                    mb: 2,
                  }}
                >
                  Audio Metadata
                </Typography>
                <Paper
                  sx={{
                    p: 2,
                    backgroundColor: 'rgba(0, 0, 0, 0.6)',
                    border: `1px solid ${theme.palette.primary.main}`,
                  }}
                >
                  <Typography variant="body2">
                    Duration: {metadata.duration.toFixed(2)}s
                  </Typography>
                  <Typography variant="body2">
                    Sample Rate: {metadata.sample_rate}Hz
                  </Typography>
                  <Typography variant="body2">
                    Tempo: {metadata.tempo.toFixed(2)} BPM
                  </Typography>
                </Paper>
              </Box>
            )}
          </Paper>
        </Box>
      </Container>
    </Layout>
  );
};

export default Home;

import { useState, useEffect, useRef } from 'react';
import type { NextPage } from 'next';
import { useTheme } from '@mui/material/styles';
import {
  Box,
  Button,
  Container,
  Typography,
  Paper,
} from '@mui/material';
import Layout from '@/components/Layout';
import AudioVisualizer from '@/components/AudioVisualizer';
import SpectrumAnalyzer from '@/components/SpectrumAnalyzer';
import FileUpload from '@/components/FileUpload';
import ProcessingStatus from '@/components/ProcessingStatus';
import { useWebSocket } from '@/hooks/useWebSocket';
import { useAudioProcessor } from '@/hooks/useAudioProcessor';
import { BackgroundEffect } from '@/components/BackgroundEffect';

const Home: NextPage = () => {
  const theme = useTheme();
  const [audioFile, setAudioFile] = useState<File | null>(null);
  const [processingStatus, setProcessingStatus] = useState<string>('idle');
  const [visualizationData, setVisualizationData] = useState<number[]>([]);
  const [spectrumData, setSpectrumData] = useState<number[]>([]);
  
  const ws = useWebSocket('ws://localhost:8000/api/v1/ws/audio');
  const { processAudio, processingProgress } = useAudioProcessor();

  const handleFileUpload = async (file: File) => {
    setAudioFile(file);
    setProcessingStatus('uploading');
    try {
      const result = await processAudio(file);
      setProcessingStatus('processing');
    } catch (error) {
      console.error('Error uploading file:', error);
      setProcessingStatus('error');
    }
  };

  useEffect(() => {
    if (ws) {
      ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        switch (data.type) {
          case 'visualization_data':
            setVisualizationData(data.data);
            break;
          case 'spectrum_data':
            setSpectrumData(data.data);
            break;
          case 'processing_status':
            setProcessingStatus(data.data.status);
            break;
        }
      };
    }
  }, [ws]);

  return (
    <Layout>
      <BackgroundEffect spectrumData={spectrumData} />
      <Container maxWidth="lg">
        <Box sx={{ mt: 4, mb: 4 }}>
          <Paper
            elevation={3}
            sx={{
              p: 3,
              background: 'rgba(0, 0, 0, 0.8)',
              border: `1px solid ${theme.palette.primary.main}`,
            }}
          >
            <Typography variant="h4" component="h2" gutterBottom>
              Audio Processing & Visualization
            </Typography>
            
            <FileUpload onFileUpload={handleFileUpload} />
            
            {processingStatus !== 'idle' && (
              <ProcessingStatus
                status={processingStatus}
                progress={processingProgress}
              />
            )}
            
            <Box sx={{ mt: 4 }}>
              <AudioVisualizer data={visualizationData} />
            </Box>
            
            <Box sx={{ mt: 4 }}>
              <SpectrumAnalyzer data={spectrumData} />
            </Box>
          </Paper>
        </Box>
      </Container>
    </Layout>
  );
};

export default Home;

