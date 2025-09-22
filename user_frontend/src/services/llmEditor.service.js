import { apiClient } from './api';
import { getEndpoint } from '../config/api.config';

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



