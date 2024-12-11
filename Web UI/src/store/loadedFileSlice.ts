import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { FileError } from '../errors/fileErrors';

interface State {
  file: File | null;
  fileDuration: number;
  separateTracks: boolean;
  error: FileError | null;
}

const initialState: State = {
  file: null,
  fileDuration: 0,
  separateTracks: false,
  error: null
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
    setFileError: (state, action: PayloadAction<FileError>) => {
      state.error = action.payload;
    },
    resetError: (state) => {
      state.error = null;
    }
  }
});

export const {
  setFile,
  setFileDuration,
  setSeparateTracks,
  setFileError,
  resetError
} = loadedFileSlice.actions;
export default loadedFileSlice.reducer;
