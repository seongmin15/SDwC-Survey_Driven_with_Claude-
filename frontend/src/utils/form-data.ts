/**
 * Convert flat dot-notation form values to nested object
 *
 * Example:
 * {"project.name": "x", "project.description": "y"}
 * → {project: {name: "x", description: "y"}}
 */
export function buildNestedData(flatData: Record<string, any>): any {
  const result: any = {};

  for (const [key, value] of Object.entries(flatData)) {
    if (key.includes('.')) {
      const parts = key.split('.');
      let current = result;

      for (let i = 0; i < parts.length - 1; i++) {
        const part = parts[i];
        if (!current[part]) {
          current[part] = {};
        }
        current = current[part];
      }

      const lastPart = parts[parts.length - 1];
      current[lastPart] = value;
    } else {
      result[key] = value;
    }
  }

  return result;
}
