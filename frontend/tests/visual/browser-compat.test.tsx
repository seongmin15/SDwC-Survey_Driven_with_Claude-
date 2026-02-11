import { describe, it, expect } from 'vitest';
import * as fs from 'fs';
import * as path from 'path';

/**
 * V-013~V-016: Browser compatibility verification
 *
 * Since we cannot run real browsers in vitest, we verify:
 * 1. Only standard, widely-supported CSS features are used (via Tailwind)
 * 2. No vendor-prefixed CSS is hardcoded (Tailwind/PostCSS handles these)
 * 3. No experimental/non-standard APIs are used in components
 */

function readAllComponentFiles(): { file: string; content: string }[] {
  const srcDir = path.resolve(__dirname, '../../src');
  const files: { file: string; content: string }[] = [];

  function walk(dir: string) {
    const entries = fs.readdirSync(dir, { withFileTypes: true });
    for (const entry of entries) {
      const fullPath = path.join(dir, entry.name);
      if (entry.isDirectory()) {
        walk(fullPath);
      } else if (entry.name.endsWith('.tsx') || entry.name.endsWith('.ts')) {
        // Skip test files, config, and type-only files
        if (!entry.name.includes('.test.') && !entry.name.includes('.spec.')) {
          files.push({ file: fullPath, content: fs.readFileSync(fullPath, 'utf-8') });
        }
      }
    }
  }

  walk(srcDir);
  return files;
}

describe('V-013~V-016: Browser compatibility (Chrome/Firefox/Safari/Edge)', () => {
  const componentFiles = readAllComponentFiles();

  it('no inline vendor-prefixed CSS in components', () => {
    const vendorPrefixes = ['-webkit-', '-moz-', '-ms-', '-o-'];

    componentFiles.forEach(({ file, content }) => {
      // Check for inline styles with vendor prefixes
      const styleMatches = content.match(/style=\{[^}]*\}/g) || [];
      styleMatches.forEach((match) => {
        vendorPrefixes.forEach((prefix) => {
          expect(match).not.toContain(prefix);
        });
      });
    });
  });

  it('no experimental Web APIs used directly', () => {
    // APIs that are not widely supported
    const experimentalAPIs = [
      'WebGPU',
      'SharedArrayBuffer',
      'document.startViewTransition',
      'popover',
      'CSS.registerProperty',
    ];

    componentFiles.forEach(({ file, content }) => {
      experimentalAPIs.forEach((api) => {
        expect(content).not.toContain(api);
      });
    });
  });

  it('uses standard Tailwind utility classes (no custom CSS modules)', () => {
    componentFiles.forEach(({ file, content }) => {
      // Should not import .css modules (all styling via Tailwind)
      const cssImports = content.match(/import\s+.*\.module\.css/g) || [];
      expect(cssImports).toHaveLength(0);
    });
  });

  it('uses standard DOM APIs compatible with all modern browsers', () => {
    // These APIs are supported in Chrome, Firefox, Safari, and Edge
    const standardAPIs = [
      'navigator.clipboard', // Clipboard API - all modern browsers
      'fetch',               // Fetch API - all modern browsers
      'URL.createObjectURL', // URL API - all modern browsers
    ];

    // Just verify no non-standard alternatives are used
    const nonStandardAPIs = [
      'document.execCommand',  // Deprecated
      'XMLHttpRequest',        // Should use fetch instead
    ];

    componentFiles.forEach(({ file, content }) => {
      nonStandardAPIs.forEach((api) => {
        // Allow in comments, but not in executable code
        const lines = content.split('\n');
        lines.forEach((line) => {
          const trimmed = line.trim();
          if (!trimmed.startsWith('//') && !trimmed.startsWith('*')) {
            expect(trimmed).not.toContain(api);
          }
        });
      });
    });
  });

  it('all component files use React functional components (wide support)', () => {
    componentFiles
      .filter(({ file }) => file.endsWith('.tsx'))
      .forEach(({ file, content }) => {
        // Should not use class components (older pattern)
        expect(content).not.toMatch(/class\s+\w+\s+extends\s+React\.Component/);
        expect(content).not.toMatch(/class\s+\w+\s+extends\s+Component/);
      });
  });
});
