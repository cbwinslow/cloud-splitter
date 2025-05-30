import React, { useEffect, useRef } from 'react';
import { useTheme } from '@mui/material/styles';

interface AudioVisualizerProps {
  data: number[];
}

const AudioVisualizer: React.FC<AudioVisualizerProps> = ({ data }) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const theme = useTheme();

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas || !data.length) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const draw = () => {
      const width = canvas.width;
      const height = canvas.height;
      const sliceWidth = width / data.length;

      // Clear canvas
      ctx.clearRect(0, 0, width, height);

      // Set line style
      ctx.lineWidth = 2;
      ctx.strokeStyle = theme.palette.primary.main;
      ctx.shadowBlur = 10;
      ctx.shadowColor = theme.palette.primary.main;

      // Begin path
      ctx.beginPath();
      ctx.moveTo(0, height / 2);

      // Draw waveform
      data.forEach((point, i) => {
        const x = i * sliceWidth;
        const y = (point * height / 2) + (height / 2);
        ctx.lineTo(x, y);
      });

      ctx.lineTo(width, height / 2);
      ctx.stroke();

      // Add glow effect
      ctx.globalCompositeOperation = 'lighter';
      ctx.strokeStyle = 'rgba(0, 255, 0, 0.3)';
      ctx.lineWidth = 4;
      ctx.stroke();
      ctx.globalCompositeOperation = 'source-over';
    };

    // Set canvas size
    canvas.width = canvas.offsetWidth;
    canvas.height = canvas.offsetHeight;

    draw();

    // Handle resize
    const handleResize = () => {
      canvas.width = canvas.offsetWidth;
      canvas.height = canvas.offsetHeight;
      draw();
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, [data, theme]);

  return (
    <div className="visualization-container">
      <canvas
        ref={canvasRef}
        className="waveform-canvas"
      />
    </div>
  );
};

export default AudioVisualizer;

