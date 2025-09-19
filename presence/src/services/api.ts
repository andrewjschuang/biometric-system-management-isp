import { FormState } from '../types';

type RecognitionParams = FormState | { phone_number: number; event_name: string };

export const submitPresence = async (params: RecognitionParams): Promise<Response> => {
  try {
    const apiUrl = '/api/recognize';

    const data = new FormData();
    data.append('event_name', params.event_name as string);

    if ('photo' in params) {
      const photoBlob = await fetch(params.photo as string).then(r => r.blob());
      data.append('image', photoBlob, 'image.jpg');
    } else {
      data.append('phone_number', params.phone_number.toString());
    }

    const response = await fetch(apiUrl, {
        method: 'POST',
        body: data,
      });

    if (!response.ok) {
      throw new Error(`Servidor respondeu com status: ${response.status}`);
    }

    return response;
  } catch (error) {
    if (error instanceof TypeError && error.message === 'Failed to fetch') {
      throw new Error('Não foi possível conectar ao servidor. Por favor, verifique se o servidor está rodando e tente novamente.');
    }
    console.error('Erro na API:', error);
    throw error;
  }
};
