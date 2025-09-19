import React from 'react';

interface RadioOption {
  id: string;
  label: string;
}

interface RadioGroupProps {
  options: RadioOption[];
  selectedValue: string | null;
  onChange: (value: string) => void;
}

const RadioGroup: React.FC<RadioGroupProps> = ({ options, selectedValue, onChange }) => {
  return (
    <div className="space-y-2">
      {options.map((option) => (
        <div 
          key={option.id}
          className={`relative rounded-lg border p-4 cursor-pointer transition-all duration-200 ${
            selectedValue === option.id 
              ? 'border-blue-500 bg-blue-50' 
              : 'border-gray-200 hover:border-gray-300'
          }`}
          onClick={() => onChange(option.id)}
        >
          <div className="flex items-center">
            <div className="flex-shrink-0 mr-3">
              <div className={`w-5 h-5 rounded-full border flex items-center justify-center ${
                selectedValue === option.id 
                  ? 'border-blue-600' 
                  : 'border-gray-400'
              }`}>
                {selectedValue === option.id && (
                  <div className="w-3 h-3 rounded-full bg-blue-600 animate-scale-in" />
                )}
              </div>
            </div>
            <div className="text-sm">
              <label htmlFor={option.id} className="font-medium text-gray-800 block cursor-pointer">
                {option.label}
              </label>
            </div>
          </div>
          <input 
            type="radio" 
            id={option.id} 
            name="cultoType" 
            value={option.id}
            checked={selectedValue === option.id}
            onChange={() => onChange(option.id)}
            className="sr-only"
          />
        </div>
      ))}
    </div>
  );
};

export default RadioGroup;