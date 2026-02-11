import { readFileSync, writeFileSync, mkdirSync } from 'fs';
import { load } from 'js-yaml';
import { resolve } from 'path';
import { fileURLToPath } from 'url';

const __dirname = fileURLToPath(new URL('.', import.meta.url));
const yamlPath = resolve(__dirname, '../../backend/resources/templates/intake-schema/intake_schema.yaml');
const outDir = resolve(__dirname, '../src/data');
const outPath = resolve(outDir, 'intake-schema.json');

mkdirSync(outDir, { recursive: true });
const yamlContent = readFileSync(yamlPath, 'utf-8');
const json = load(yamlContent);
writeFileSync(outPath, JSON.stringify(json, null, 2));
console.log(`Schema converted: ${outPath}`);
