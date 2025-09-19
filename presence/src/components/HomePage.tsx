import React from 'react';
import { Camera, Smartphone } from 'lucide-react';

interface HomePageProps {
  onSelectFaceRecognition: () => void;
  onSelectPhoneRecognition: () => void;
}

const HomePage: React.FC<HomePageProps> = ({ onSelectFaceRecognition, onSelectPhoneRecognition }) => {
  return (
    <div className="bg-white rounded-xl shadow-md overflow-hidden transition-all duration-300 transform">
      <div className="px-6 py-8 space-y-6">
        <div className="text-center mb-8">
          <h1 className="text-2xl font-bold text-gray-900 mb-2">
            Sistema de Presença
          </h1>
          <p className="text-gray-600">
            Escolha como deseja fazer o reconhecimento
          </p>
        </div>

        <div className="space-y-4">
          <button
            type="button"
            onClick={onSelectFaceRecognition}
            className="w-full flex flex-col items-center justify-center p-6 border-2 border-gray-300 rounded-lg hover:border-blue-500 hover:bg-blue-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-all duration-200"
          >
            <Camera className="w-12 h-12 text-blue-500 mb-3" />
            <span className="text-lg font-medium text-gray-900">
              Reconhecer por Face
            </span>
            <span className="text-sm text-gray-500 mt-1">
              Use a câmera para tirar uma foto
            </span>
          </button>

          <button
            type="button"
            onClick={onSelectPhoneRecognition}
            className="w-full flex flex-col items-center justify-center p-6 border-2 border-gray-300 rounded-lg hover:border-green-500 hover:bg-green-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 transition-all duration-200"
          >
            <Smartphone className="w-12 h-12 text-green-500 mb-3" />
            <span className="text-lg font-medium text-gray-900">
              Reconhecer por Celular
            </span>
            <span className="text-sm text-gray-500 mt-1">
              Digite seu número de telefone
            </span>
          </button>
        </div>
      </div>
    </div>
  );
};

export default HomePage;