import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';

type FuncType = 'Data modifier' | 'Graphical' | 'Copy';

export interface IAnalyzeType {
  choose_track: boolean;
  description: string;
  func_type: FuncType;
  id: number;
  name: string;
  args: unknown;
}

export const pipelineApi = createApi({
  reducerPath: 'pipelineApi',
  baseQuery: fetchBaseQuery({ baseUrl: 'http://127.0.0.1:6789' }),
  tagTypes: ['AnalyzeTypes'],
  endpoints: (builder) => ({
    getAnalizeTypes: builder.query<IAnalyzeType[], void>({
      query: () => `/help/`,
      providesTags: ['AnalyzeTypes']
    })
  })
});

export const { useGetAnalizeTypesQuery } = pipelineApi;
