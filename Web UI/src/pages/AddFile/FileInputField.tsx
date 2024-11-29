import { ChangeEvent, useRef } from 'react';
import FileInputIcon from '../../components/icons/FileInputIcon';
import { useAppDispatch, useAppSelector } from '../../store/store';
import { setFile } from '../../store/loadedFileSlice';

const FileInputField = () => {
  const dispatch = useAppDispatch();
  const { file } = useAppSelector((state) => state.loadedFile);

  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleSelectFile = () => {
    if (fileInputRef.current) fileInputRef.current.click();
  };

  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    const newFile = e.target.files?.item(0);
    if (newFile && newFile.name !== file?.name) dispatch(setFile(newFile));
  };

  return (
    <div id="file_input" onClick={handleSelectFile}>
      <span>{file?.name ?? 'Add file'}</span>
      <input
        type="file"
        accept="audio/wav document/doc"
        style={{ display: 'none' }}
        ref={fileInputRef}
        onChange={handleFileChange}
      />
      <FileInputIcon />
    </div>
  );
};

export default FileInputField;
