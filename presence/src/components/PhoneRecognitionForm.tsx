import React, { useState, useEffect } from 'react';
import { ArrowLeft } from 'lucide-react';
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
  const [dataConsent, setDataConsent] = useState(false);

  useEffect(() => {
    if (submitSuccess) {
      setTimeout(() => {
        window.location.reload();
      }, 2000);
    }
  }, [submitSuccess]);

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
      setDataConsent(false);
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

        <div className="flex items-start space-x-3 py-3">
          <input
            type="checkbox"
            id="dataConsent"
            checked={dataConsent}
            onChange={(e) => setDataConsent(e.target.checked)}
            className="mt-1 h-4 w-4 text-green-600 focus:ring-green-500 border-gray-300 rounded"
          />
          <label htmlFor="dataConsent" className="text-sm text-gray-700">
            Autorizo o uso do meu número de telefone para controle de presença
          </label>
        </div>

        <SubmitButton
          isSubmitting={isSubmitting}
          isDisabled={!phoneNumber.trim() || !eventName || !dataConsent}
        />
      </form>
    </div>
  );
};

export default PhoneRecognitionForm;
