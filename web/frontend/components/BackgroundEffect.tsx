import React, { useEffect, useRef } from 'react';
import { useTheme } from '@mui/material/styles';
import { Box } from '@mui/material';

interface BackgroundEffectProps {
  spectrumData: number[];
}

const BackgroundEffect: React.FC<BackgroundEffectProps> = ({ spectrumData }) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const theme = useTheme();
  const particlesRef = useRef<Array<{ x: number; y: number; speed: number; size: number }>>([]);
  const animationRef = useRef<number>();

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Initialize particles
    const initParticles = () => {
      const particles = [];
      const numParticles = 100;

      for (let i = 0; i < numParticles; i++) {
        particles.push({
          x: Math.random() * canvas.width,
          y: Math.random() * canvas.height,
          speed: 0.5 + Math.random() * 2,
          size: 1 + Math.random() * 3,
        });
      }

      particlesRef.current = particles;
    };

    // Animation function
    const animate = () => {
      ctx.fillStyle = 'rgba(0, 0, 0, 0.1)';
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      // Update and draw particles
      particlesRef.current.forEach((particle, i) => {
        // Update particle position
        particle.y += particle.speed;
        if (particle.y > canvas.height) {
          particle.y = 0;
        }

        // Modify particle properties based on spectrum data
        const spectrumIndex = Math.floor((i / particlesRef.current.length) * spectrumData.length);
        const intensity = spectrumData[spectrumIndex] || 0;

        // Draw particle
        ctx.beginPath();
        ctx.arc(particle.x, particle.y, particle.size * (1 + intensity), 0, Math.PI * 2);
        ctx.fillStyle = `rgba(0, 255, 0, ${0.3 + intensity * 0.5})`;
        ctx.fill();

        // Add glow effect
        ctx.shadowBlur = 10;
        ctx.shadowColor = theme.palette.primary.main;
        ctx.fill();
        ctx.shadowBlur = 0;
      });

      // Draw spectrum visualization
      if (spectrumData.length > 0) {
        const barWidth = canvas.width / spectrumData.length;
        
        ctx.beginPath();
        ctx.moveTo(0, canvas.height);
        
        spectrumData.forEach((value, i) => {
          const x = i * barWidth;
          const height = value * 100;
          ctx.lineTo(x, canvas.height - height);
        });
        
        ctx.lineTo(canvas.width, canvas.height);
        ctx.closePath();
        
        const gradient = ctx.createLinearGradient(0, 0, 0, canvas.height);
        gradient.addColorStop(0, 'rgba(0, 255, 0, 0.2)');
        gradient.addColorStop(1, 'rgba(0, 255, 0, 0)');
        
        ctx.fillStyle = gradient;
        ctx.fill();
      }

      animationRef.current = requestAnimationFrame(animate);
    };

    // Set canvas size
    const resize = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    };

    window.addEventListener('resize', resize);
    resize();
    initParticles();
    animate();

    return () => {
      window.removeEventListener('resize', resize);
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, [spectrumData, theme]);

  return (
    <Box
      className="matrix-background"
      sx={{
        position: 'fixed',
        top: 0,
        left: 0,
        width: '100%',
        height: '100%',
        zIndex: -1,
      }}
    >
      <canvas
        ref={canvasRef}
        style={{
          display: 'block',
          width: '100%',
          height: '100%',
        }}
      />
    </Box>
  );
};

export default BackgroundEffect;

