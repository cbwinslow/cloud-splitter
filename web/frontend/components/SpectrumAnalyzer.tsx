import React, { useEffect, useRef } from 'react';
import { useTheme } from '@mui/material/styles';
import { Box } from '@mui/material';

interface SpectrumAnalyzerProps {
  data: number[];
}

const NUM_BANDS = 10;

const SpectrumAnalyzer: React.FC<SpectrumAnalyzerProps> = ({ data }) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const theme = useTheme();
  const animationRef = useRef<number>();

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas || !data.length) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const draw = () => {
      const width = canvas.width;
      const height = canvas.height;
      const barWidth = width / NUM_BANDS;
      const maxDataValue = Math.max(...data);

      // Clear canvas
      ctx.clearRect(0, 0, width, height);

      // Draw frequency bands
      data.slice(0, NUM_BANDS).forEach((value, i) => {
        const barHeight = (value / maxDataValue) * height;
        const x = i * barWidth;
        const y = height - barHeight;

        // Draw bar with gradient
        const gradient = ctx.createLinearGradient(x, y, x, height);
        gradient.addColorStop(0, 'rgba(0, 255, 0, 0.8)');
        gradient.addColorStop(1, 'rgba(0, 255, 0, 0.2)');

        ctx.fillStyle = gradient;
        ctx.fillRect(x, y, barWidth - 2, barHeight);

        // Add glow effect
        ctx.shadowBlur = 15;
        ctx.shadowColor = theme.palette.primary.main;
        ctx.fillRect(x, y, barWidth - 2, barHeight);
        ctx.shadowBlur = 0;
      });

      // Draw grid lines
      ctx.strokeStyle = 'rgba(0, 255, 0, 0.2)';
      ctx.lineWidth = 1;

      for (let i = 0; i < 5; i++) {
        const y = (height / 5) * i;
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(width, y);
        ctx.stroke();
      }

      animationRef.current = requestAnimationFrame(draw);
    };

    // Set canvas size
    canvas.width = canvas.offsetWidth;
    canvas.height = canvas.offsetHeight;

    draw();

    // Handle resize
    const handleResize = () => {
      canvas.width = canvas.offsetWidth;
      canvas.height = canvas.offsetHeight;
    };

    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, [data, theme]);

  return (
    <Box className="spectrum-analyzer">
      <canvas
        ref={canvasRef}
        style={{
          width: '100%',
          height: '100%',
        }}
      />
    </Box>
  );
};

export default SpectrumAnalyzer;

