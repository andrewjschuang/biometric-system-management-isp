import React, { createContext, useContext, useState } from 'react';
import { submitPresence } from '../services/api';

interface FormState {
  photo: string | null;
  event_name: string | null;
}

interface FormContextType {
  formState: FormState;
  updateFormState: (field: keyof FormState, value: any) => void;
  submitForm: () => Promise<void>;
  isSubmitting: boolean;
  submitError: string | null;
  submitSuccess: boolean;
}

const initialFormState: FormState = {
  photo: null,
  event_name: null,
};

const FormContext = createContext<FormContextType | undefined>(undefined);

export const FormProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [formState, setFormState] = useState<FormState>(initialFormState);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState<string | null>(null);
  const [submitSuccess, setSubmitSuccess] = useState(false);

  const updateFormState = (field: keyof FormState, value: any) => {
    setFormState((prev) => ({
      ...prev,
      [field]: value,
    }));

    if (submitError) {
      setSubmitError(null);
    }
    if (submitSuccess) {
      setSubmitSuccess(false);
    }
  };

  const submitForm = async () => {
    if (!formState.photo || !formState.event_name) {
      setSubmitError('Por favor preencha todos os campos');
      return;
    }

    setIsSubmitting(true);
    setSubmitError(null);
    setSubmitSuccess(false);

    try {
      const response = await submitPresence(formState);
      if (response.status === 202) {
        setSubmitSuccess(true);
        setFormState(initialFormState);
      }
    } catch (error) {
      console.error('Error submitting form:', error);
      setSubmitError(error instanceof Error ? error.message : 'Ocorreu um erro ao enviar o formulário. Por favor, tente novamente.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const value = {
    formState,
    updateFormState,
    submitForm,
    isSubmitting,
    submitError,
    submitSuccess,
  };

  return <FormContext.Provider value={value}>{children}</FormContext.Provider>;
};

export const useFormContext = (): FormContextType => {
  const context = useContext(FormContext);
  if (!context) {
    throw new Error('useFormContext must be used within a FormProvider');
  }
  return context;
};
