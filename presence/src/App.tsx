import React, { useState } from 'react';
import HomePage from './components/HomePage';
import PresencaForm from './components/PresencaForm';
import PhoneRecognitionForm from './components/PhoneRecognitionForm';
import { FormProvider } from './context/FormContext';

type Page = 'home' | 'face-recognition' | 'phone-recognition';

function App() {
  const [currentPage, setCurrentPage] = useState<Page>('home');

  const handleSelectFaceRecognition = () => {
    setCurrentPage('face-recognition');
  };

  const handleSelectPhoneRecognition = () => {
    setCurrentPage('phone-recognition');
  };

  const handleBackToHome = () => {
    setCurrentPage('home');
  };

  const renderPage = () => {
    switch (currentPage) {
      case 'home':
        return (
          <HomePage
            onSelectFaceRecognition={handleSelectFaceRecognition}
            onSelectPhoneRecognition={handleSelectPhoneRecognition}
          />
        );
      case 'face-recognition':
        return <PresencaForm onBack={handleBackToHome} />;
      case 'phone-recognition':
        return <PhoneRecognitionForm onBack={handleBackToHome} />;
      default:
        return (
          <HomePage
            onSelectFaceRecognition={handleSelectFaceRecognition}
            onSelectPhoneRecognition={handleSelectPhoneRecognition}
          />
        );
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <FormProvider>
        <div className="container max-w-md mx-auto px-4 py-8">
          {renderPage()}
        </div>
      </FormProvider>
    </div>
  );
}

export default App;