import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';

type FuncType = 'Data modifier' | 'Graphical' | 'Copy';

export interface IAnalyzeTypeArg {
  datatype: string;
  description: string;
  name: string;
  units: string;
}

export interface IAnalyzeType {
  choose_track: boolean;
  description: string;
  func_type: FuncType;
  id: number;
  name: string;
  args: IAnalyzeTypeArg[];
}

export const pipelineApi = createApi({
  reducerPath: 'pipelineApi',
  baseQuery: fetchBaseQuery({ baseUrl: 'http://127.0.0.1:6789' }),
  tagTypes: ['AnalyzeTypes'],
  endpoints: (builder) => ({
    getAnalizeTypes: builder.query<IAnalyzeType[], void>({
      query: () => `/help/`,
      providesTags: ['AnalyzeTypes']
    }),
    sendPipeline: builder.mutation({
      query: (body: FormData) => ({
        url: '/function_call/',
        method: 'POST',
        body
      })
    })
  })
});

export const { useGetAnalizeTypesQuery, useSendPipelineMutation } = pipelineApi;
