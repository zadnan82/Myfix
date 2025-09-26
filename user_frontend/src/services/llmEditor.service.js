import { apiClient } from './api';
import { getApiUrl, getEndpoint, CONFIG } from '../config/api.config';

export async function editTextFileWithLLM(file, prompt, options = {}) {
  if (!(file instanceof File)) {
    throw new Error('file must be a File');
  }
  if (!prompt || typeof prompt !== 'string') {
    throw new Error('prompt is required');
  }

  const formData = new FormData();
  formData.append('file', file);
  formData.append('prompt', prompt);
  // Match GPU server contract: model_name, prompt, system_prompt
  if (options.model_name) {
    formData.append('model_name', options.model_name);
  }
  if (options.system_prompt) {
    formData.append('system_prompt', options.system_prompt);
  }

  // Prefer public endpoint to avoid auth
  const endpointKey = 'LLM_EDITOR_EDIT_FILE_PUBLIC';
  return apiClient.postForm(getEndpoint(endpointKey), formData);
}

export async function editFileJSON({ path, content, prompt, options = {} }) {
  if (!path || !prompt) throw new Error('path and prompt are required');
  const url = getApiUrl('/api/v1/llm-editor/edit-file');
  const body = {
    path,
    prompt,
    content,
    dry_run: !!options.dryRun,
    model_name: options.model_name,
    system_prompt: options.systemPrompt,
  };
  const originalTimeout = CONFIG.API.TIMEOUT;
  try {
    apiClient.setTimeout(120000);
    return await apiClient.post(url, body);
  } finally {
    apiClient.setTimeout(originalTimeout);
  }
}

export async function browseTree(path = '/') {
  const url = getApiUrl(`/api/projects/tree?path=${encodeURIComponent(path)}`);
  return apiClient.get(url);
}

export async function readProjectFile(path) {
  const url = getApiUrl(`/api/projects/file?path=${encodeURIComponent(path)}`);
  return apiClient.get(url, { headers: { Accept: 'text/plain' } });
}

export async function writeProjectFile(path, content) {
  const url = getApiUrl('/api/projects/file');
  return apiClient.put(url, { path, content });
}

export async function createPreviewByPath(path) {
  if (!path) throw new Error('path is required');
  const url = getApiUrl('/api/v1/previews/by-path');
  return apiClient.post(url, { path });
}



