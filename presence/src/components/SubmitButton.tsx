import React from 'react';

interface SubmitButtonProps {
  isSubmitting: boolean;
  isDisabled: boolean;
}

const SubmitButton: React.FC<SubmitButtonProps> = ({ isSubmitting, isDisabled }) => {
  return (
    <button
      type="submit"
      disabled={isDisabled || isSubmitting}
      className={`w-full flex justify-center items-center py-3 px-4 border border-transparent rounded-md shadow-sm text-base font-medium text-white transition-all duration-200 ${
        isDisabled 
          ? 'bg-gray-400 cursor-not-allowed' 
          : isSubmitting 
            ? 'bg-blue-600' 
            : 'bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500'
      }`}
    >
      {isSubmitting ? (
        <>
          <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          Enviando...
        </>
      ) : (
        'Registrar Presença'
      )}
    </button>
  );
};

export default SubmitButton;