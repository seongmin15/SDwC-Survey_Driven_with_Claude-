export interface SchemaOption {
  id: string;
  label: string;
  description?: string;
}

export interface SchemaField {
  id: string;
  type: 'text' | 'textarea' | 'select' | 'multi_select' | 'list' | 'number' | 'boolean' | 'repeatable_group';
  label: string;
  required?: boolean;
  placeholder?: string;
  description?: string;
  condition?: string;
  depends_on?: string;
  options?: SchemaOption[];
  options_by_parent?: Record<string, SchemaOption[]>;
  options_from?: string;
  // list type
  item_type?: string;
  min_items?: number;
  max_items?: number;
  // repeatable_group type
  item_label?: string;
  fields?: SchemaField[];
}

export interface SchemaSection {
  id: string;
  label: string;
  order: number;
  condition?: string;
  type?: string;
  item_label?: string;
  min_items?: number;
  max_items?: number;
  fields: SchemaField[];
}

export interface IntakeSchema {
  schema_version: string;
  sections: SchemaSection[];
}
