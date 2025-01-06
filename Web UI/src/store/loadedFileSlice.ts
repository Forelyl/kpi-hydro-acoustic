import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { FileError } from '../errors/fileErrors';
import { PipelineError } from '../errors/pipelineErrors';

interface State {
  file: File | null;
  fileDuration: number;
  separateTracks: boolean;
  error: FileError | PipelineError | null;
  channels: number;
  resultZip: Blob | null;
}

const initialState: State = {
  file: null,
  fileDuration: 0,
  separateTracks: false,
  error: null,
  channels: 0,
  resultZip: null
};

const loadedFileSlice = createSlice({
  name: 'loadedFile',
  initialState,
  reducers: {
    setFile: (state, action: PayloadAction<File>) => {
      state.file = action.payload;
    },
    setFileDuration: (state, action: PayloadAction<number>) => {
      state.fileDuration = action.payload;
    },
    setSeparateTracks: (state, action: PayloadAction<boolean>) => {
      state.separateTracks = action.payload;
    },
    setError: (state, action: PayloadAction<FileError | PipelineError>) => {
      state.error = action.payload;
    },
    resetError: (state) => {
      state.error = null;
    },
    setFileChannels: (state, action: PayloadAction<number>) => {
      state.channels = action.payload;
    },
    setResultZip: (state, action: PayloadAction<Blob>) => {
      state.resultZip = action.payload;
    }
  }
});

export const {
  setFile,
  setFileDuration,
  setSeparateTracks,
  setError,
  resetError,
  setFileChannels,
  setResultZip
} = loadedFileSlice.actions;
export default loadedFileSlice.reducer;
