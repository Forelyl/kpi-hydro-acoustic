import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';

export const pipelineApi = createApi({
  reducerPath: 'pipelineApi',
  baseQuery: fetchBaseQuery({ baseUrl: 'http://127.0.0.1:6789' }),
  endpoints: (builder) => ({
    getAnalizeTypes: builder.query<Record<string, string>[], void>({
      query: () => `/help/`
    })
  })
});

export const { useGetAnalizeTypesQuery } = pipelineApi;
