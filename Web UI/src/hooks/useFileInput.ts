import { ChangeEvent, DragEvent, useCallback, useRef, useState } from 'react';
import { useAppDispatch, useAppSelector } from '../store/store';
import { useDroppable } from '@dnd-kit/core';
import {
  setFile,
  setFileDuration,
  setFileError
} from '../store/loadedFileSlice';
import { fileErrors } from '../errors/fileErrors';

export const acceptedFileTypes = 'audio/wav, audio/mp3';

const useFileInput = () => {
  const dispatch = useAppDispatch();
  const { file } = useAppSelector((state) => state.loadedFile);

  const fileInputRef = useRef<HTMLInputElement>(null);
  const { setNodeRef } = useDroppable({
    id: 'droppableFileInput'
  });

  const [isDragGoing, setDragGoing] = useState<boolean>(false);

  const handleSetFile = useCallback(
    (newFile?: File | null) => {
      if (newFile && newFile.name !== file?.name) {
        if (acceptedFileTypes.includes(newFile.type)) {
          const url = URL.createObjectURL(newFile);
          const audio = new Audio(url);
          audio.addEventListener(
            'loadedmetadata',
            () => {
              dispatch(setFile(newFile));
              dispatch(setFileDuration(Math.round(audio.duration)));
              URL.revokeObjectURL(url);
            },
            { once: true }
          );
          audio.addEventListener(
            'error',
            () => {
              dispatch(setFileError(fileErrors.LOAD_FAILED));
              URL.revokeObjectURL(url);
            },
            { once: true }
          );
          return;
        }
        dispatch(setFileError(fileErrors.INVALID_FORMAT));
      }
    },
    [dispatch, file]
  );

  const handleFileSelect = useCallback(() => {
    if (fileInputRef.current) fileInputRef.current.click();
  }, []);

  const handleFileDrop = useCallback(
    (e: DragEvent<HTMLDivElement>) => {
      e.preventDefault();
      setDragGoing(false);

      if (e.dataTransfer?.files.length === 1)
        return handleSetFile(e.dataTransfer?.files.item(0));
      dispatch(setFileError(fileErrors.MANY_FILES));
    },
    [handleSetFile, dispatch]
  );

  const handleFileChange = useCallback(
    (e: ChangeEvent<HTMLInputElement>) => {
      setDragGoing(false);

      if (e.target.files?.length === 1)
        return handleSetFile(e.target.files?.item(0));
      dispatch(setFileError(fileErrors.MANY_FILES));
    },
    [handleSetFile, dispatch]
  );

  const handleDragEnter = useCallback(() => setDragGoing(true), []);

  const handleDragLeave = useCallback(() => setDragGoing(false), []);

  const handleDragEnd = useCallback(() => setDragGoing(false), []);

  const handleDragOver = useCallback(
    (e: React.DragEvent<HTMLDivElement>) => e.preventDefault(),
    []
  );

  return {
    fileInputRef,
    filename: file?.name ?? 'Add file',
    handleFileChange,
    droppableAreaProps: {
      onClick: handleFileSelect,
      onDragEnter: handleDragEnter,
      onDragLeave: handleDragLeave,
      onDragEnd: handleDragEnd,
      onDragOver: handleDragOver,
      onDrop: handleFileDrop,
      ref: setNodeRef,
      className: isDragGoing ? "dragging" : "not_dragging" 
    }
  };
};

export default useFileInput;
