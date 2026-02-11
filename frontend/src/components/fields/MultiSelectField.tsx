import type { SchemaOption } from '../../types/schema';

interface MultiSelectFieldProps {
  id: string;
  label: string;
  required?: boolean;
  options: SchemaOption[];
  values: string[];
  error?: string;
  onChange: (values: string[]) => void;
}

export default function MultiSelectField({
  id,
  label,
  required,
  options,
  values,
  error,
  onChange,
}: MultiSelectFieldProps) {
  const handleToggle = (optionId: string) => {
    if (values.includes(optionId)) {
      onChange(values.filter((v) => v !== optionId));
    } else {
      onChange([...values, optionId]);
    }
  };

  return (
    <div className="space-y-2">
      <div className="block text-sm font-medium text-gray-700">
        {label}
        {required && <span className="text-red-500 ml-1">*</span>}
      </div>
      <div className="space-y-2">
        {options.map((opt) => (
          <div key={opt.id} className="flex items-start">
            <input
              type="checkbox"
              id={`${id}-${opt.id}`}
              checked={values.includes(opt.id)}
              onChange={() => handleToggle(opt.id)}
              aria-label={opt.label}
              className="mt-1 mr-2"
            />
            <label htmlFor={`${id}-${opt.id}`} className="text-sm">
              <span className="font-medium">{opt.label}</span>
              {opt.description && (
                <span className="text-gray-500 block">{opt.description}</span>
              )}
            </label>
          </div>
        ))}
      </div>
      {error && (
        <p id={`${id}-error`} role="alert" className="text-sm text-red-500">
          {error}
        </p>
      )}
    </div>
  );
}
