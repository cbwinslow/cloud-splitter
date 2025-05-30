import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { Box, Typography, CircularProgress } from '@mui/material';
import { useTheme } from '@mui/material/styles';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';

interface FileUploadProps {
  onFileUpload: (file: File) => void;
}

const FileUpload: React.FC<FileUploadProps> = ({ onFileUpload }) => {
  const theme = useTheme();
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    if (acceptedFiles.length === 0) return;

    const file = acceptedFiles[0];
    setError(null);
    setIsUploading(true);

    try {
      await onFileUpload(file);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Upload failed');
    } finally {
      setIsUploading(false);
    }
  }, [onFileUpload]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'audio/*': ['.mp3', '.wav', '.flac', '.ogg']
    },
    multiple: false,
  });

  return (
    <Box
      {...getRootProps()}
      className={`upload-zone ${isDragActive ? 'dragging' : ''}`}
      sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        p: 4,
        border: `2px dashed ${theme.palette.primary.main}`,
        borderRadius: 2,
        cursor: 'pointer',
        transition: 'all 0.3s ease',
        '&:hover': {
          borderColor: theme.palette.primary.light,
          backgroundColor: 'rgba(0, 255, 0, 0.05)',
        },
      }}
    >
      <input {...getInputProps()} />
      
      {isUploading ? (
        <CircularProgress
          size={50}
          sx={{
            color: theme.palette.primary.main,
            filter: 'drop-shadow(0 0 10px rgba(0, 255, 0, 0.5))',
          }}
        />
      ) : (
        <>
          <CloudUploadIcon
            sx={{
              fontSize: 60,
              color: theme.palette.primary.main,
              mb: 2,
              filter: 'drop-shadow(0 0 10px rgba(0, 255, 0, 0.5))',
            }}
          />
          <Typography
            variant="h6"
            sx={{
              color: theme.palette.primary.main,
              textAlign: 'center',
              mb: 1,
            }}
          >
            {isDragActive
              ? 'Drop the audio file here'
              : 'Drag & drop an audio file or click to select'}
          </Typography>
          <Typography
            variant="body2"
            sx={{
              color: theme.palette.primary.main,
              opacity: 0.7,
            }}
          >
            Supported formats: MP3, WAV, FLAC, OGG
          </Typography>
        </>
      )}

      {error && (
        <Typography
          color="error"
          sx={{
            mt: 2,
            textAlign: 'center',
          }}
        >
          {error}
        </Typography>
      )}
    </Box>
  );
};

export default FileUpload;

