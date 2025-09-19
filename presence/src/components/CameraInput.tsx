import React, { useRef, useEffect, useState } from 'react';
import { X, Camera } from 'lucide-react';
import { useFormContext } from '../context/FormContext';

interface CameraInputProps {
  onClose: () => void;
}

const CameraInput: React.FC<CameraInputProps> = ({ onClose }) => {
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const streamRef = useRef<MediaStream | null>(null);
  const { updateFormState } = useFormContext();
  const [cameraReady, setCameraReady] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const stopCurrentStream = () => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => {
        track.stop();
      });
      streamRef.current = null;
    }
    if (videoRef.current) {
      videoRef.current.srcObject = null;
    }
  };

  const startCamera = async () => {
    try {
      if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        throw new Error('Câmera não suportada neste dispositivo');
      }

      stopCurrentStream();

      const constraints = {
        video: {
          facingMode: 'user',
          width: { ideal: 1920 },
          height: { ideal: 1080 }
        },
        audio: false
      };

      const stream = await navigator.mediaDevices.getUserMedia(constraints);
      streamRef.current = stream;
        
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        await new Promise((resolve) => {
          if (videoRef.current) {
            videoRef.current.onloadedmetadata = resolve;
          }
        });
        
        if (videoRef.current.readyState >= 2) {
          try {
            await videoRef.current.play();
            setCameraReady(true);
          } catch (playError) {
            console.error('Error playing video:', playError);
            throw new Error('Não foi possível iniciar a câmera');
          }
        }
      }
    } catch (err) {
      console.error('Erro ao acessar a câmera:', err);
      let errorMessage = 'Não foi possível acessar a câmera. ';
      
      if (err instanceof Error) {
        if (err.name === 'NotAllowedError' || err.name === 'PermissionDeniedError') {
          errorMessage += 'Por favor, permita o acesso à câmera nas configurações do seu dispositivo.';
        } else if (err.name === 'NotFoundError') {
          errorMessage += 'Nenhuma câmera encontrada no dispositivo.';
        } else if (err.name === 'NotReadableError' || err.name === 'AbortError') {
          errorMessage += 'Câmera está sendo usada por outro aplicativo.';
        } else if (err.name === 'NotSupportedError' || window.location.protocol === 'http:') {
          errorMessage += 'Seu navegador não suporta acesso à câmera em HTTP. Por favor, use HTTPS.';
        } else {
          errorMessage += 'Verifique suas permissões e tente novamente.';
        }
      }
      
      setError(errorMessage);
    }
  };

  useEffect(() => {
    startCamera();

    return () => {
      stopCurrentStream();
    };
  }, []);

  const capturePhoto = () => {
    if (videoRef.current && canvasRef.current && cameraReady) {
      const video = videoRef.current;
      const canvas = canvasRef.current;
      const context = canvas.getContext('2d');
      
      if (context) {
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;

        // Flip the image horizontally to match the mirrored preview
        context.scale(-1, 1);
        context.drawImage(video, -canvas.width, 0, canvas.width, canvas.height);

        const photoDataUrl = canvas.toDataURL('image/jpeg', 0.8);
        updateFormState('photo', photoDataUrl);
        onClose();
      }
    }
  };

  return (
    <div className="fixed inset-0 z-50 bg-black flex flex-col">
      <div className="relative flex-1" style={{ height: 'calc(100% - 80px)' }}>
        {error ? (
          <div className="h-full flex items-center justify-center">
            <div className="text-white text-center p-4">
              <p className="mb-4">{error}</p>
              <button
                type="button"
                onClick={onClose}
                className="px-4 py-2 bg-red-600 text-white rounded-md"
              >
                Fechar
              </button>
            </div>
          </div>
        ) : (
          <>
            <video
              ref={videoRef}
              autoPlay
              playsInline
              muted
              className="absolute inset-0 w-full h-full object-cover"
              style={{ transform: 'scaleX(-1)' }}
            />
            <canvas ref={canvasRef} className="hidden" />
          </>
        )}
      </div>
      
      {!error && (
        <div className="h-20 p-4 flex justify-between items-center bg-black relative z-10">
          <button
            type="button"
            onClick={onClose}
            className="p-2 rounded-full bg-gray-800 text-white"
          >
            <X className="w-6 h-6" />
          </button>
          
          <button
            type="button"
            onClick={capturePhoto}
            disabled={!cameraReady}
            className={`p-4 rounded-full ${
              cameraReady 
                ? 'bg-white text-black' 
                : 'bg-gray-700 text-gray-400'
            }`}
          >
            <Camera className="w-8 h-8" />
          </button>
          
          <div className="w-10" /> {/* Spacer to maintain centering */}
        </div>
      )}
    </div>
  );
};

export default CameraInput;