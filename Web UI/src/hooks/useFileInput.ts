import { ChangeEvent, DragEvent, useCallback, useRef, useState } from 'react';
import { useAppDispatch, useAppSelector } from '../store/store';
import { useDroppable } from '@dnd-kit/core';
import { setFile } from '../store/loadedFileSlice';

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
        if (acceptedFileTypes.includes(newFile.type))
          dispatch(setFile(newFile));
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
      if (e.dataTransfer?.files.length === 1)
        handleSetFile(e.dataTransfer?.files.item(0));
      setDragGoing(false);
    },
    [handleSetFile]
  );

  const handleFileChange = useCallback(
    (e: ChangeEvent<HTMLInputElement>) => {
      if (e.target.files?.length === 1) handleSetFile(e.target.files?.item(0));
      setDragGoing(false);
    },
    [handleSetFile]
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
      style: { opacity: isDragGoing ? 0.5 : 1 }
    }
  };
};

export default useFileInput;
