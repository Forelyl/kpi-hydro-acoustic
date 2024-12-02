import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { FileError } from '../errors/fileErrors';

interface State {
  file: File | null;
  separateTracks: boolean;
  error: FileError | null;
}

const initialState: State = {
  file: null,
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

export const { setFile, setSeparateTracks, setFileError, resetError } =
  loadedFileSlice.actions;
export default loadedFileSlice.reducer;
