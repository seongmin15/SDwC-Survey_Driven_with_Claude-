interface BooleanFieldProps {
  id: string;
  label: string;
  required?: boolean;
  description?: string;
  value: boolean | string;
  error?: string;
  onChange: (value: boolean) => void;
}

export default function BooleanField({
  id,
  label,
  required,
  description,
  value,
  error,
  onChange,
}: BooleanFieldProps) {
  const boolValue = value === true || value === 'true';

  return (
    <div className="space-y-2">
      <div className="block text-sm font-medium text-gray-700">
        {label}
        {required && <span className="text-red-500 ml-1">*</span>}
      </div>
      {description && <p className="text-sm text-gray-500">{description}</p>}
      <div className="flex gap-4">
        <label className="flex items-center">
          <input
            type="radio"
            name={id}
            checked={boolValue === true}
            onChange={() => onChange(true)}
            aria-label="예"
            className="mr-2"
          />
          <span className="text-sm">예</span>
        </label>
        <label className="flex items-center">
          <input
            type="radio"
            name={id}
            checked={boolValue === false}
            onChange={() => onChange(false)}
            aria-label="아니오"
            className="mr-2"
          />
          <span className="text-sm">아니오</span>
        </label>
      </div>
      {error && (
        <p id={`${id}-error`} role="alert" className="text-sm text-red-500">
          {error}
        </p>
      )}
    </div>
  );
}
