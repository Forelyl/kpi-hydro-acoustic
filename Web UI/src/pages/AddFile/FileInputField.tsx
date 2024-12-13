import FileInputIcon from '../../components/icons/FileInputIcon';
import { DndContext } from '@dnd-kit/core';
import useFileInput, { acceptedFileTypes } from '../../hooks/useFileInput';

const FileInputField = () => {
  const { fileInputRef, filename, handleFileChange, droppableAreaProps } =
    useFileInput();

  return (
    <DndContext>
      <div {...droppableAreaProps} id="file_input">
        <div></div>
        <span>{filename}</span>
        <input
          type="file"
          accept={acceptedFileTypes}
          style={{ display: 'none' }}
          ref={fileInputRef}
          onChange={handleFileChange}
        />
        <FileInputIcon />
      </div>
    </DndContext>
  );
};

export default FileInputField;
