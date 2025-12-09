// Lightweight Pyodide loader and runner
// Loads the Pyodide WASM runtime from the official CDN and exposes helpers
// to run Python code in the browser and capture stdout/stderr.

declare global {
  interface Window {
    loadPyodide?: any;
    pyodide?: any;
  }
}

let pyodideInstance: any | null = null;
let loadingPromise: Promise<any> | null = null;

export async function loadPyodideIfNeeded(): Promise<any> {
  if (pyodideInstance) return pyodideInstance;
  if (loadingPromise) return loadingPromise;

  loadingPromise = (async () => {
    if (typeof window === 'undefined') {
      throw new Error('Pyodide is only available in browser environment');
    }
    if (!(window as any).loadPyodide) {
      await new Promise<void>((resolve, reject) => {
        const script = document.createElement('script');
        script.src = 'https://cdn.jsdelivr.net/pyodide/v0.23.4/full/pyodide.js';
        script.onload = () => resolve();
        script.onerror = reject;
        document.head.appendChild(script);
      });
    }

    const loadFn = (window as any).loadPyodide;
    if (!loadFn) throw new Error('loadPyodide not available');
    pyodideInstance = await loadFn({ indexURL: 'https://cdn.jsdelivr.net/pyodide/v0.23.4/full/' });
    return pyodideInstance;
  })();

  return loadingPromise;
}

export async function runPythonWithPyodide(code: string, timeoutMs = 30000): Promise<{ output: string; error: string | null }> {
  const pyodide = await loadPyodideIfNeeded();

  // Wrapper that captures stdout/stderr into a buffer and returns it.
  const wrapper = `\nimport sys, io, traceback\nbuf = io.StringIO()\nold_out = sys.stdout\nold_err = sys.stderr\nsys.stdout = buf\nsys.stderr = buf\ntry:\n    exec(${JSON.stringify(code)}, globals())\nexcept Exception:\n    traceback.print_exc()\nfinally:\n    sys.stdout = old_out\n    sys.stderr = old_err\nbuf.getvalue()`;

  const runPromise = (async () => {
    try {
      const res = await pyodide.runPythonAsync(wrapper);
      const out = typeof res === 'string' ? res : String(res ?? '');
      if (out && out.trim().length) {
        // Heuristic: if we see 'Traceback' then treat as error
        if (out.includes('Traceback')) {
          return { output: '', error: out };
        }
        return { output: out, error: null };
      }
      return { output: 'Code executed successfully (no output)', error: null };
    } catch (err: any) {
      const errStr = err?.message ?? String(err);
      return { output: '', error: errStr };
    }
  })();

  if (!timeoutMs || timeoutMs <= 0) return await runPromise;

  const timeoutPromise = new Promise<{ output: string; error: string | null }>((resolve) => {
    setTimeout(() => resolve({ output: '', error: `Execution timed out (${timeoutMs}ms)` }), timeoutMs);
  });

  return await Promise.race([runPromise, timeoutPromise]);
}

export async function unloadPyodide(): Promise<void> {
  if (!pyodideInstance) return;
  try {
    // There is no formal API to unload the WASM instance; remove references.
    (window as any).pyodide = undefined;
  } finally {
    pyodideInstance = null;
    loadingPromise = null;
  }
}
