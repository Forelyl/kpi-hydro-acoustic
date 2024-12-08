import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { FileError } from '../errors/fileErrors';

interface State {
  file: File | null;
  fileDuration: number;
  fileDurationString: string;
  separateTracks: boolean;
  error: FileError | null;
}

const initialState: State = {
  file: null,
  fileDuration: 0,
  fileDurationString: '',
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
      const minutes = Math.floor(action.payload / 60);
      const minutesString = minutes < 10 ? `0${minutes}` : `${minutes}`;
      const seconds = action.payload % 60;
      const secondsString = seconds < 10 ? `0${seconds}` : `${seconds}`;
      state.fileDurationString = `${minutesString}:${secondsString}`;
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
