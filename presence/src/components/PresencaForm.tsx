import React, { useState, useEffect } from 'react';
import { Camera, ArrowLeft } from 'lucide-react';
import CameraInput from './CameraInput';
import RadioGroup from './RadioGroup';
import { useFormContext } from '../context/FormContext';
import SubmitButton from './SubmitButton';

interface PresencaFormProps {
  onBack?: () => void;
}

const PresencaForm: React.FC<PresencaFormProps> = ({ onBack }) => {
  const { formState, updateFormState, submitForm, isSubmitting, submitError, submitSuccess } = useFormContext();
  const [showCamera, setShowCamera] = useState(false);

  useEffect(() => {
    if (submitSuccess) {
      setTimeout(() => {
        onBack?.();
      }, 2000);
    }
  }, [submitSuccess, onBack]);

  const handleOpenCamera = () => {
    setShowCamera(true);
  };

  const handleCloseCamera = () => {
    setShowCamera(false);
  };

  const cultoOptions = [
    { id: 'ebd', label: 'EBD' },
    { id: 'culto_pt', label: 'Culto Português' },
    { id: 'culto_tw', label: 'Culto Taiwanês' },
    { id: 'culto_md', label: 'Culto Mandarim' },
    { id: 'culto_unificado', label: 'Culto Unificado' },
    { id: 'outro', label: 'Outro' },
  ];

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await submitForm();
  };

  return (
    <div className="bg-white rounded-xl shadow-md overflow-hidden transition-all duration-300 transform">
      {onBack && (
        <div className="px-6 pt-4 pb-2">
          <button
            type="button"
            onClick={onBack}
            className="flex items-center text-gray-600 hover:text-gray-900 transition-colors duration-200"
          >
            <ArrowLeft className="w-5 h-5 mr-2" />
            Voltar
          </button>
        </div>
      )}
      <form onSubmit={handleSubmit} className="px-6 py-6 space-y-6">
        <div className="space-y-4">
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Foto
          </label>

          {showCamera ? (
            <CameraInput onClose={handleCloseCamera} />
          ) : (
            <div className="flex flex-col items-center">
              {formState.photo ? (
                <div className="relative w-full">
                  <img
                    src={formState.photo}
                    alt="Foto capturada"
                    className="w-full h-64 object-cover rounded-lg"
                  />
                  <button
                    type="button"
                    onClick={handleOpenCamera}
                    className="mt-2 w-full inline-flex justify-center items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-500 hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors duration-200"
                  >
                    <Camera className="w-5 h-5 mr-2" />
                    Tirar outra foto
                  </button>
                </div>
              ) : (
                <button
                  type="button"
                  onClick={handleOpenCamera}
                  className="w-full flex flex-col items-center justify-center h-64 border-2 border-dashed border-gray-300 rounded-lg hover:border-blue-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors duration-200"
                >
                  <Camera className="w-12 h-12 text-gray-400" />
                  <span className="mt-2 text-sm font-medium text-gray-500">
                    Clique para tirar uma foto
                  </span>
                </button>
              )}
            </div>
          )}
        </div>

        <div className="space-y-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Tipo de Culto
          </label>
          <RadioGroup
            options={cultoOptions}
            selectedValue={formState.event_name}
            onChange={(value) => updateFormState('event_name', value)}
          />
        </div>

        {submitError && (
          <div className="p-3 bg-red-50 text-red-700 rounded-md text-sm">
            {submitError}
          </div>
        )}

        {submitSuccess && (
          <div className="p-3 bg-green-50 text-green-700 rounded-md text-sm">
            Enviado com sucesso!
          </div>
        )}

        <SubmitButton
          isSubmitting={isSubmitting}
          isDisabled={!formState.photo || !formState.event_name}
        />
      </form>
    </div>
  );
};

export default PresencaForm;
