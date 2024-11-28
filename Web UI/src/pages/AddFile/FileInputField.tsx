import { ChangeEvent, Dispatch, SetStateAction, useRef } from 'react';
import FileInputIcon from '../../components/icons/FileInputIcon';

interface Props {
  setFile: Dispatch<SetStateAction<File | undefined>>;
}

const FileInputField = ({ setFile }: Props) => {
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleSelectFile = () => {
    if (fileInputRef.current) fileInputRef.current.click();
  };

  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.item(0);
    if (file) setFile(file);
  };

  return (
    <div onClick={handleSelectFile}>
      <span>Add file</span>
      <input
        type="file"
        accept="audio/wav"
        style={{ display: 'none' }}
        ref={fileInputRef}
        onChange={handleFileChange}
      />
      <FileInputIcon />
    </div>
  );
};

export default FileInputField;
