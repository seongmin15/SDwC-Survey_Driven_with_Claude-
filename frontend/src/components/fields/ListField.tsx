import { useEffect, useRef } from 'react';

interface ListFieldProps {
  id: string;
  label: string;
  required?: boolean;
  minItems?: number;
  placeholder?: string;
  values: string[];
  error?: string;
  onChange: (values: string[]) => void;
}

export default function ListField({
  id,
  label,
  required,
  minItems,
  placeholder,
  values,
  error,
  onChange,
}: ListFieldProps) {
  const initializedRef = useRef(false);

  // Ensure at least minItems items (only on mount)
  useEffect(() => {
    if (!initializedRef.current && values.length === 0 && minItems && minItems > 0) {
      initializedRef.current = true;
      onChange(Array(minItems).fill(''));
    }
  }, [values.length, minItems, onChange]);

  const handleAdd = () => {
    onChange([...values, '']);
  };

  const handleRemove = (index: number) => {
    onChange(values.filter((_, i) => i !== index));
  };

  const handleChange = (index: number, value: string) => {
    const newValues = [...values];
    newValues[index] = value;
    onChange(newValues);
  };

  return (
    <div className="space-y-2">
      <div className="block text-sm font-medium text-gray-700">
        {label}
        {required && <span className="text-red-500 ml-1">*</span>}
      </div>
      <div className="space-y-2">
        {values.map((value, index) => (
          <div key={index} className="flex gap-2">
            <input
              type="text"
              value={value}
              onChange={(e) => handleChange(index, e.target.value)}
              placeholder={placeholder}
              aria-label={`${label} ${index + 1}`}
              className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <button
              type="button"
              onClick={() => handleRemove(index)}
              className="px-3 py-2 text-red-600 border border-red-600 rounded-md hover:bg-red-50"
            >
              X
            </button>
          </div>
        ))}
      </div>
      <button
        type="button"
        onClick={handleAdd}
        className="px-4 py-2 text-sm text-blue-600 border border-blue-600 rounded-md hover:bg-blue-50"
      >
        추가
      </button>
      {error && (
        <p id={`${id}-error`} role="alert" className="text-sm text-red-500">
          {error}
        </p>
      )}
    </div>
  );
}
