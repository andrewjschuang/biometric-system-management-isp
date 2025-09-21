import React, { useState } from 'react';
import { ArrowLeft, Smartphone } from 'lucide-react';
import RadioGroup from './RadioGroup';
import SubmitButton from './SubmitButton';
import { submitPresence } from '../services/api';

interface PhoneRecognitionFormProps {
  onBack?: () => void;
}

const PhoneRecognitionForm: React.FC<PhoneRecognitionFormProps> = ({ onBack }) => {
  const [phoneNumber, setPhoneNumber] = useState('');
  const [eventName, setEventName] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState<string | null>(null);
  const [submitSuccess, setSubmitSuccess] = useState(false);

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
    setIsSubmitting(true);
    setSubmitError(null);
    setSubmitSuccess(false);

    try {
      await submitPresence({
        phone_number: parseInt(phoneNumber),
        event_name: eventName,
      });
      setSubmitSuccess(true);
      setPhoneNumber('');
      setEventName('');
    } catch (error) {
      console.error('Erro ao enviar formulário:', error);
      setSubmitError(error instanceof Error ? error.message : 'Erro desconhecido');
    } finally {
      setIsSubmitting(false);
    }
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
        <div className="text-center mb-6">
          <Smartphone className="w-12 h-12 text-green-500 mx-auto mb-3" />
          <h2 className="text-xl font-semibold text-gray-900">
            Reconhecimento por Telefone
          </h2>
        </div>

        <div className="space-y-4">
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Número do Telefone
          </label>
          <input
            type="tel"
            value={phoneNumber}
            onChange={(e) => {
              const value = e.target.value.replace(/\D/g, '');
              setPhoneNumber(value);
            }}
            placeholder="11999999999"
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500"
            required
          />
        </div>

        <div className="space-y-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Tipo de Culto
          </label>
          <RadioGroup
            options={cultoOptions}
            selectedValue={eventName}
            onChange={setEventName}
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
          isDisabled={!phoneNumber.trim() || !eventName}
        />
      </form>
    </div>
  );
};

export default PhoneRecognitionForm;
