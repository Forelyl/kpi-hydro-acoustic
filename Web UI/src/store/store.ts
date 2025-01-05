import { combineReducers, configureStore } from '@reduxjs/toolkit';
import { useSelector } from 'react-redux';
import { TypedUseSelectorHook, useDispatch } from 'react-redux';
import loadedFileReducer from './loadedFileSlice';
import { pipelineApi } from './pipelineApi';

const reducer = combineReducers({
  loadedFile: loadedFileReducer,
  [pipelineApi.reducerPath]: pipelineApi.reducer
});

const store = configureStore({
  reducer,
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        ignoredActions: ['loadedFile/setFile'],
        ignoredPaths: ['loadedFile.file']
      }
    }).concat(pipelineApi.middleware)
});

export type RootState = ReturnType<typeof reducer>;
export type AppDispatch = typeof store.dispatch;

export const useAppDispatch = useDispatch.withTypes<AppDispatch>();
export const useAppSelector: TypedUseSelectorHook<RootState> = useSelector;

export default store;
