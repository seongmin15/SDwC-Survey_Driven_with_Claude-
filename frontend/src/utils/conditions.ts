/**
 * Evaluates condition strings against form values
 *
 * Supported operators:
 * - "a == b" → formValues[a] === b
 * - "a != b" → formValues[a] !== b
 * - "a contains b" → Array.isArray(formValues[a]) && formValues[a].includes(b)
 * - "a is not empty" → formValues[a] && (Array.isArray ? length > 0 : truthy)
 * - "a AND b" → split by AND, all must be true
 */
export function evaluateCondition(
  condition: string | undefined,
  formValues: Record<string, any>
): boolean {
  if (!condition) return true;

  // Handle AND operator
  if (condition.includes(' AND ')) {
    const parts = condition.split(' AND ').map(p => p.trim());
    return parts.every(part => evaluateSingleCondition(part, formValues));
  }

  return evaluateSingleCondition(condition, formValues);
}

function evaluateSingleCondition(
  condition: string,
  formValues: Record<string, any>
): boolean {
  // "field is not empty"
  if (condition.includes(' is not empty')) {
    const field = condition.replace(' is not empty', '').trim();
    const value = formValues[field];
    if (!value) return false;
    if (Array.isArray(value)) return value.length > 0;
    return true;
  }

  // "field contains value"
  if (condition.includes(' contains ')) {
    const [field, value] = condition.split(' contains ').map(s => s.trim());
    const fieldValue = formValues[field];
    if (!Array.isArray(fieldValue)) return false;
    return fieldValue.includes(value);
  }

  // "field != value"
  if (condition.includes(' != ')) {
    const [field, value] = condition.split(' != ').map(s => s.trim());
    return formValues[field] !== value;
  }

  // "field == value"
  if (condition.includes(' == ')) {
    const [field, value] = condition.split(' == ').map(s => s.trim());
    return formValues[field] === value;
  }

  return false;
}
