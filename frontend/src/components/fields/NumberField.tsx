interface NumberFieldProps {
  id: string;
  label: string;
  required?: boolean;
  placeholder?: string;
  value: number | string;
  error?: string;
  onChange: (value: number | string) => void;
}

export default function NumberField({
  id,
  label,
  required,
  placeholder,
  value,
  error,
  onChange,
}: NumberFieldProps) {
  return (
    <div className="space-y-1">
      <label htmlFor={id} className="block text-sm font-medium text-gray-700">
        {label}
        {required && <span className="text-red-500 ml-1">*</span>}
      </label>
      <input
        id={id}
        type="number"
        required={required}
        placeholder={placeholder}
        value={value}
        onChange={(e) => onChange(e.target.value ? Number(e.target.value) : '')}
        aria-describedby={error ? `${id}-error` : undefined}
        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
      {error && (
        <p id={`${id}-error`} role="alert" className="text-sm text-red-500">
          {error}
        </p>
      )}
    </div>
  );
}
