import React from 'react';
import { Box, Typography, LinearProgress } from '@mui/material';
import { useTheme } from '@mui/material/styles';
import { Motion, spring } from 'react-motion';

interface ProcessingStatusProps {
  status: string;
  progress?: number;
}

const ProcessingStatus: React.FC<ProcessingStatusProps> = ({ status, progress = 0 }) => {
  const theme = useTheme();

  const getStatusColor = () => {
    switch (status) {
      case 'processing':
        return theme.palette.primary.main;
      case 'completed':
        return theme.palette.success.main;
      case 'error':
        return theme.palette.error.main;
      default:
        return theme.palette.primary.main;
    }
  };

  const getStatusMessage = () => {
    switch (status) {
      case 'uploading':
        return 'Uploading audio file...';
      case 'processing':
        return 'Processing audio...';
      case 'completed':
        return 'Processing completed';
      case 'error':
        return 'Error processing file';
      default:
        return 'Preparing...';
    }
  };

  return (
    <Box
      className="processing-status"
      sx={{
        p: 3,
        borderRadius: 2,
        backgroundColor: 'rgba(0, 0, 0, 0.6)',
        border: `1px solid ${getStatusColor()}`,
        boxShadow: `0 0 10px ${getStatusColor()}`,
      }}
    >
      <Typography
        variant="h6"
        sx={{
          color: getStatusColor(),
          mb: 2,
          textShadow: `0 0 10px ${getStatusColor()}`,
        }}
      >
        {getStatusMessage()}
      </Typography>

      {status === 'processing' && (
        <Motion defaultStyle={{ width: 0 }} style={{ width: spring(progress) }}>
          {interpolated => (
            <>
              <LinearProgress
                variant="determinate"
                value={interpolated.width}
                sx={{
                  height: 8,
                  borderRadius: 4,
                  backgroundColor: 'rgba(0, 255, 0, 0.2)',
                  '& .MuiLinearProgress-bar': {
                    backgroundColor: theme.palette.primary.main,
                    boxShadow: `0 0 10px ${theme.palette.primary.main}`,
                  },
                }}
              />
              <Typography
                variant="body2"
                sx={{
                  color: theme.palette.primary.main,
                  mt: 1,
                  textAlign: 'right',
                }}
              >
                {Math.round(interpolated.width)}%
              </Typography>
            </>
          )}
        </Motion>
      )}

      {status === 'error' && (
        <Typography
          color="error"
          variant="body2"
          sx={{
            mt: 1,
            textShadow: '0 0 10px rgba(255, 0, 0, 0.5)',
          }}
        >
          Please try again or contact support if the problem persists.
        </Typography>
      )}
    </Box>
  );
};

export default ProcessingStatus;

