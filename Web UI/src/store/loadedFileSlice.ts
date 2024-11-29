import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface State {
  file: File | null;
  separateTracks: boolean;
}

const initialState: State = {
  file: null,
  separateTracks: false
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
    }
  }
});

export const { setFile, setSeparateTracks } = loadedFileSlice.actions;
export default loadedFileSlice.reducer;
